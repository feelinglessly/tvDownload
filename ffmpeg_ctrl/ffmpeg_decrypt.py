import subprocess

from config import config


def decrypt(key, iv, input_path, output_path):
    """
    目前不可用
    :param key:
    :param iv:
    :param input_path:
    :param output_path:
    :return:
    """
    if key == b'' or len(key) > config.common.TS_KEY_LENGTH_MAX:
        return
    cmd = [
        "ffmpeg",
        "decryption_key", key,
        "decryption_iv", iv,
        "i", input_path,
        "c", output_path,
    ]
    # 运行并捕获日志
    try:
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        print("解密成功！")
    except subprocess.CalledProcessError as e:
        print(f"解密成功！错误信息：\n{e.output}")
    except Exception as e:
        print(f"""解密失败！以外错误： 
        key: {key}
        iv: {iv}
        {e}""")



