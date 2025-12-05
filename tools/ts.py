import os

step = "_"

def make_ts_name(nid, ts_name):
    return f"{nid}{step}{ts_name}"

def sort_f(a, b):
    """
    排序函数，按照分隔符前面的排序，如果没有分隔符，长度小的排前面
    :param a:
    :param b:
    :return:
    """
    al = os.path.dirname(a).split(step)
    bl = os.path.dirname(b).split(step)
    if len(al) > 1 and len(bl) > 1:
        return -1 if int(al[0]) < int(bl[0]) else 1
    if len(a) != len(b):
        return len(a) - len(b)
    return -1 if a < b else 1