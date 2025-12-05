import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from queue import Queue, Empty

from stores.stores import get_store


class Ctrl(object):
    queue = Queue()
    max_workers = 3
    futures = None
    pool = None
    func = None
    spiders = None
    stop_event = threading.Event()
    watch_thread = None
    main_thread = None
    def __init__(self, max_workers=3, func=None):
        self.max_workers = max_workers
        self.futures = dict()
        self.func = func
        self.spiders = dict()
        self.pool = ThreadPoolExecutor(max_workers=self.max_workers)
        self.watch_thread = threading.Thread(target=self.watch, daemon=True)
        self.main_thread = threading.Thread(target=self.run, daemon=True)

    def running_num(self):
        i = 0
        for future in self.futures.values():
            if not future.done():
                i += 1
        return i

    def dones(self):
        done_futures = []
        for uuid, future in self.futures.items():
            if future.done() and not future.cancelled():
                done_futures.append(uuid)
        return done_futures

    def watch(self):
        while not self.stop_event.is_set():
            store = get_store()
            if not store.empty() and self.running_num() < self.max_workers:
                self.queue.put(store.popitem())
            time.sleep(1)
            for future_uuid in self.dones():
                store.done(future_uuid)

    def start(self):
        self.watch_thread.start()
        self.main_thread.start()

    def run(self):
        with self.pool as executor:
            while not self.stop_event.is_set():
                try:
                    data = self.queue.get(block=True, timeout=1)
                    spider = self.func(data)
                    self.spiders[data.uuid] = spider
                    self.futures[data.uuid] = executor.submit(spider.run)
                except Empty:
                    continue

    def reset(self):
        for spider in self.spiders.values():
            spider.reset()
        self.stop_event.clear()

    def stop_one(self, uuid):
        """
        停止其中一个
        :param uuid:
        :return:
        """
        for i, spider in self.spiders.items():
            if uuid == i:
                spider.stop()
        for i, future in self.futures.items():
            if uuid == i and not future.done():
                future.cancel()

    def stop(self):
        """
        全部停止但是不结束，相当于放弃当前的，但是不能结束循环
        :return:
        """
        for spider in self.spiders.values():
            spider.stop()
        for i, future in enumerate(self.futures.values()):
            print(f"ctrl close: {i+1}/{len(self.futures.values())}, is done: {future.done()}")
            if not future.done():
                future.cancel()
            print(f"ctrl close: {i+1}/{len(self.futures.values())}, is done: {future.done()}")
            # if not future.done():
            #     raise

    def close(self):
        """
        关闭
        :return:
        """
        self.stop_event.set()
        self.watch_thread.join()
        self.stop()
