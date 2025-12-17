import time


def retry(nums=3):
    def w1(f):
        def wrapper(*args, **kwargs):
            i = 1
            while i < nums:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    print(f"retry：函数{f}执行失败 {f.__dict__}，重试{i}/{nums}, args:{args}, {kwargs}, err: {e}")
                    i += 1
            raise RuntimeError("超过最大重试次数", f, args, kwargs)
        return wrapper
    return w1


def call_time(name):
    def w1(f):
        def wrapper(*args, **kwargs):
            t1 = time.time()
            res = f(*args, **kwargs)
            print(f"函数{name}耗时：{time.time() - t1}")
            return res
        return wrapper
    return w1
