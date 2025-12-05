from collections import defaultdict

from PySide6.QtCore import Signal, SignalInstance, QObject

from stores.data import VideoData


class PubType:
    func = None
    args = ()
    kwargs = dict()
    def __init__(self, func, *args):
        self.func = func
        self.args = args


class Sync(QObject):
    pubs = None
    signal = Signal(str)
    def __init__(self):
        QObject.__init__(self)

    def sub(self):
        self.signal.emit("sub")
        return None

    def to_connect(self, f):
        # self.pubs.append(PubType(f, *args))
        self.signal.connect(f)


class Store(Sync):
    _store = defaultdict(VideoData)
    def __init__(self, store=None):
        super().__init__()
        self._store = store or defaultdict(VideoData)

    def push(self, data: VideoData):
        if len(self._store) >= 10:
            raise ValueError("最多10个")
        if self.get(data.uuid):
            return
        self._store[data.uuid] = data
        self.sub()

    def popitem(self):
        for k, data in self._store.items():
            if not data.is_padding():
                continue
            data.set_running()
            self.sub()
            return data
        return None

    def pop(self, uuid):
        """
        标记一个为取用
        :param uuid:
        :return:
        """
        data = self._store[uuid]
        data.set_running()
        self.sub()
        return data

    def add(self, uuid):
        """
        标记一个为未取用
        :param uuid:
        :return:
        """
        data = self._store[uuid]
        data.set_running()
        self.sub()
        return data


    def get(self, uuid):
        """
        查看一个信息不取出
        :param uuid:
        :return:
        """
        return self._store.get(uuid, None)

    def done(self, uuid):
        data = self.get(uuid)
        if data is not None:
            data.done()
        self.sub()

    def list(self):
        return self._store.values()

    def empty(self):
        for uuid, data in self._store.items():
            if data.is_padding():
                return False
        return True

    def reset(self):
        for data in self._store.values():
            data.set_padding()
        self.sub()

    def stop(self):
        for data in self._store.values():
            data.stop()
        self.sub()


_store = Store()

def get_store():
    return _store