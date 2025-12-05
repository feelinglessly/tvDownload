import os.path

from Crypto.Util.Padding import unpad

from config import get_config
from Crypto.Cipher import AES


def use_decrypt(f):
    def w(this, *args, **kwargs):
        if this.is_decrypted:
            return f(this, *args, **kwargs)
        return None
    return w

class DecryptTs:
    key_b = b''
    iv = b''
    cipher = None
    is_decrypted = True

    def __init__(self, key_b=b'', iv=None):
        # 初始化向量（IV），如果未指定则使用默认值（全零）
        self.iv = iv or bytes([0] * 16)  # AES-128的IV为16字节
        if key_b == b'' or len(key_b) > get_config().common.TS_KEY_LENGTH_MAX:
            self.is_decrypted = False
        if not self.is_decrypted:
            return
        self.key_b = key_b
        self.init_cipher()

    @use_decrypt
    def init_cipher(self):
        self.cipher = AES.new(self.key_b, AES.MODE_CBC, iv=self.iv)

    @use_decrypt
    def decrypt(self, encrypted_ts_path, output_path=""):
        with open(encrypted_ts_path, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = self.decrypt_ts(encrypted_data)
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)

    @use_decrypt
    def decrypt_ts(self, ts_data):
        decrypted_data = unpad(self.cipher.decrypt(ts_data), AES.block_size)
        return decrypted_data
