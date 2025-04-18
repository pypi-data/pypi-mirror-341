def remove(path):
  try:
      import shutil;shutil.rmtree(path)
  except Exception as e:
    pass
# 使用範例
# remove("/content/git-init")
def get_HH():
  import subprocess
  # 設定 Git 記憶憑證並設定 URL
  # subprocess.run("git config --global credential.helper 'cache --timeout=3600'", shell=True, check=True)
  import os,subprocess
  if os.getenv("HOME",False):
    HH = os.getenv("HOME")+"/.git-credentials"
    subprocess.run(f"git config --global credential.helper 'store --file={HH}'", shell=True)
  elif os.getenv('USERPROFILE', False):
    HH = os.getenv("USERPROFILE")+"/.git-credentials"
    subprocess.run(f"git config --global credential.helper 'store --file={os.getenv('USERPROFILE', False)}'", shell=True)
  else:
    os._exit(0)
  return HH

# 哈希函數：使用 SHA-256 將密碼加密
def hash_password(password):
    import hashlib
    sha256_hash = hashlib.sha256()  # 創建一個 SHA-256 對象
    sha256_hash.update(password.encode('utf-8'))  # 將密碼轉換為字節，並加密
    return sha256_hash.hexdigest()  # 返回十六進制的哈希值

# 解密函數：使用位移解密
def decrypt(encrypted_text, password):
    # 生成一個基於密碼的位移量（簡單示範，您可以根據需要修改）
    def from_password(password):
        shift = 0
        for char in password:
            shift += ord(char)  # 使用字元的 Unicode 值來生成位移量
        return shift % 256  # 保證位移量在 0 到 255 之間
    shift = from_password(password)
    decrypted_text = ''.join(chr((ord(char) - shift) % 65536) for char in encrypted_text)  # 使用 Unicode 編碼
    return decrypted_text
