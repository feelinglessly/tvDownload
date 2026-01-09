import locale
import os
import subprocess
import shlex

from config import get_config

system_encoding = locale.getpreferredencoding()

# 获得视频时长
def get_video_duration(input_file):
    """
    获取视频时长（秒）
    :param input_file: 视频位置
    :return:
    """
    cmd = f"{get_config().common.FFPROBE_COMMAND} -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {shlex.quote(input_file)}"
    try:
        duration = float(subprocess.check_output(cmd, shell=True).decode('utf-8').strip())
        return duration
    except subprocess.CalledProcessError as e:
        print(f"错误：无法获取视频时长 - {e}")
        return None

# 裁剪视频
def trim_video(input_file, output_file, cut_start=0, cut_end=0):
    """
    裁剪视频首尾
    :param input_file: 输入文件路径
    :param output_file: 输出文件路径
    :param cut_start: 要剪掉的开始部分（秒）
    :param cut_end: 要剪掉的结尾部分（秒）
    :return: 是否成功
    """
    duration = get_video_duration(input_file)
    if duration is None:
        return False

    # if cut_start + cut_end >= duration:
    #     print("错误：裁剪时间超过视频总时长")
    #     return False

    # 计算结束时间点（总时长 - 结尾裁剪时长）
    end_time = duration - cut_end

    # 构建FFmpeg命令（使用流复制快速处理）
    cmd = (
        f"{get_config().common.FFMPEG_COMMAND} -ss {cut_start}  -to {end_time}  -i {shlex.quote(input_file)} "
        f"-c copy -y {shlex.quote(output_file)}"
    )

    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"视频裁剪成功，保存为: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误：视频裁剪失败 - {e}")
        return False


def  merge_video_by_file(list_path, output_path):
    """
    合并视频
    :param list_path: 存放了视频列表的文件位置
    :param output_path: 合并之后输出的位置，要带文件名后后缀
    :return:
    """
    cmd = [
        get_config().common.FFMPEG_COMMAND,
        "-f", "concat",
        "-safe", "0",
        "-i", list_path,
        "-c", "copy",
        "-bsf:a", "aac_adtstoasc",
        "-fflags", "+genpts",
        "-async", "1",
        "-avoid_negative_ts", "make_zero",
        "-video_track_timescale", "90000",
        output_path
    ]

    # cmd = [
    #     get_config().common.FFMPEG_COMMAND,
    #     "-f", "concat",
    #     "-safe", "0",
    #     "-i", list_path,
    #     # "-vf", "settb=1/90000,setpts=N/30/TB",
    #     # "-af", "asetpts=N/48000/TB",
    #     "-c:v", "libx264",
    #     # "-preset", "fast",
    #     "-c:a", "aac",
    #     "-strict", "experimental",
    #     output_path
    # ]

    # 运行并捕获日志
    try:
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            # encoding=system_encoding,  # 使用系统编码解码 解决 windows gbk的问题
            encoding="UTF-8",  # 使用系统编码解码 解决 windows gbk的问题
            creationflags=subprocess.CREATE_NO_WINDOW # 隐藏合并视频时的窗口，在打包成exe之后有用
        )
        print("合并成功！", output_path)
    except subprocess.CalledProcessError as e:
        print(f"合并失败！错误信息：\n{e.output}")


def merge_video(inputs, output_file):
    """
    合并视频
    :param inputs: ts文件列表
    :param output_file: 输出文件位置，带文件名和后缀
    :return:
    """
    output = os.path.dirname(output_file)
    list_path = os.path.join(output, "temp_file_list.txt")
    # 通过管道传递concat描述
    with open(list_path, "w") as f:
        for i in inputs:
            f.write(f"file '{os.path.abspath(i)}'\n")
    merge_video_by_file(list_path, output_file)
    # # 清理临时文件
    if os.path.exists(list_path):
        os.remove(list_path)

#
def video_get_timescales(input_file):
    # 获取音频采样率
    audio_scale = int(subprocess.check_output([
        get_config().common.FFPROBE_COMMAND, "-v", "error",
        "-select_streams", "a",
        "-show_entries", "stream=sample_rate",
        "-of", "csv=p=0",
        input_file
    ]).decode())
    return audio_scale



if __name__ == '__main__':
    trim_video(
        "/Users/zcg/Projects/output/videos/yyqjw/第1集.mp4",
        "/Users/zcg/Projects/output/videos/yyqjw/第1集1.mp4",
        2,
        3
    )


