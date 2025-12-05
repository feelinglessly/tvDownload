import os
import glob
import shutil
from functools import cmp_to_key

from ffmpeg_ctrl.ffmpeg_tools import merge_video_by_file
from tools.ts import sort_f


class FfmpegVideo:
    def __init__(self, path, prefix):
        """
        :param path: ts 文件位置
        :param prefix: 哪些前缀的ts文件需要被合并
        """
        self.path = path
        self.prefix = prefix

    def ts_files(self):
        """
        拿到ts文件列表
        :return:
        """
        return sorted(glob.glob(os.path.join(self.path, f"{self.prefix}*.ts")), key=cmp_to_key(sort_f))

    def remove_ts_files(self):
        """
        把ts文件都删了
        :return:
        """
        if os.path.exists(self.path):
            print("删除文件夹及下属文件：", self.path)
            shutil.rmtree(self.path)

    def merge_to_mp4(self, output_name, output_path=""):
        """
        :param output_name: 输出文件名
        :param output_path: 输出文件位置，不传默认放到 self.path
        :return:
        """
        list_path = os.path.join(self.path, "temp_file_list.txt")
        output_path = os.path.join(self.path if output_path=="" else output_path, output_name)
        # 生成临时文件列表
        with open(list_path, "w") as f:
            for ts in self.ts_files():
                f.write(f"file '{os.path.abspath(ts)}'\n")
        merge_video_by_file(list_path, output_path)
        # # 清理临时文件
        # if os.path.exists(list_path):
        #     os.remove(list_path)