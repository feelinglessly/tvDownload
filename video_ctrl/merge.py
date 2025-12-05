import glob
import os
from pathlib import Path
from functools import cmp_to_key

from ffmpeg_ctrl.ffmpeg_tools import trim_video, merge_video
from tools.ts import sort_f


def merge_video2(path, step, cut_start=0, cut_end=0, prefix="", suffix=".mp4"):
    """
    :param path: 视频文件夹
    :param step: 每几个视频拼接到一起
    :param cut_start: 片头裁剪多少
    :param cut_end: 片尾裁剪多少
    :param prefix: 匹配前缀
    :param suffix: 匹配后缀
    :return:
    """
    l = sorted(glob.glob(os.path.join(path, f"{prefix}*{suffix}")), key=cmp_to_key(sort_f))
    print("开始裁剪")
    output = os.path.join(path, "output")
    merge_list = []
    for i in l:
        output_file = os.path.join(output, os.path.basename(i))
        print(f"裁剪{i} -> {output}")
        trim_video(
            i,
            output_file,
            cut_start=cut_start,
            cut_end=cut_end,
        )
        merge_list.append(output_file)
    print("开始合并")
    for j in [merge_list[i: i+step] for i in range(0, len(merge_list), step) ]:
        ol = [
            os.path.basename(j[0]).replace(suffix, ""),
            os.path.basename(j[-1]).replace(suffix, "")
        ]
        output_file = f"{'-'.join(ol)}{suffix}"
        print(output_file)
        merge_video(j, os.path.join(output, output_file))
        for i in j:
            if os.path.exists(i):
                os.remove(i)



if __name__ == "__main__":
    merge_video2("/Users/zcg/Projects/output/videos/yyqjw/", 2, 2, 3, "")


