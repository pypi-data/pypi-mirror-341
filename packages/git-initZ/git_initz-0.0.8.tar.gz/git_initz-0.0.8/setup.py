
from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
from exeOP import *  # 引用 exe.py 中的 需要的方法
import sys,site,os
 
 
class new_class(install):
    # 設定類別屬性 name
    name = "git-initZ"  # 自定義名稱
    version = "0.0.8"  # 你想要安裝的版本
    base_dir = [i for i in sys.path if i.endswith('packages') if "pip" in os.listdir(i)][0]


    def run(self):
      ####################################################################################
      ####################################################################################
      def check_install(package_name):
          import subprocess
          result = subprocess.run(
              ['pip', 'show', package_name],
              capture_output=True,  # 捕获标准输出和标准错误
              text=True  # 确保输出是文本格式
          )
          return result.returncode == 0
      ####################################################################################
      ####################################################################################
      # 动态生成 .pth 文件
      def create_pth_file(self):
        # 動態生成 .pth 文件內容，假設你要將當前目錄添加到 sys.path
        import os
        clone_dir = os.path.join( self.base_dir, self.name );###remove(clone_dir)
        pth_file_path = os.path.join( self.base_dir, f"{self.name}.pth")
        with open( pth_file_path , 'w') as f:
            f.write( clone_dir )
        return f'{self.name}.pth'
      # 生成 .pth 文件
      pth_file_path = create_pth_file(new_class)
      print(f"⚠️ {pth_file_path}！")
      #####################################
      # # 需要先驗證帳戶  ---彈出視窗-##
      # from google.colab import auth
      # auth.authenticate_user()
      # ################################### ##### 需要對話:::無法使用
      print("✅ 開始安裝模組",get_HH())
      ####################################################################################
      ####################################################################################
      import os
      # 讀取密碼或令牌，如果環境變數未設置則使用預設值
      KEY = os.getenv("KEY", "False")
      if KEY == "False":
          print("⚠️ 請設置 KEY 環境變數！")
          exit(1)
      else:
          # content = "ȁȆȊǻȎǇǰǒȒȌǌǞǻǠǼǝǞǱȒȓǓǯȁǜǽǨ"
          # access_token = decrypt( decrypt( content  ,KEY), hash_password(KEY)[0:32] )
          access_token = "glpat-3G5j3n4a9ma1TMbkzmL1"
          print("✅ Token 已輸入（不會顯示）")



  
      #############--------------------------################
      # 示例：检查 "requests" 是否已安装
      HH = get_HH()
      clone_dir = os.path.join( self.base_dir, self.name );###remove(clone_dir)
      print("@ HH @",HH)
      if not(check_install('git-initZ')):  ### 尚未安裝!?not
        import subprocess
        result = subprocess.run(
            ['pip', 'install', '--force-reinstall', f"git+https://oauth2:{access_token}@gitlab.com/moon-start/{self.name}.git@{self.version}"],
            capture_output=True,  # 捕获标准输出和标准错误
            text=True  # 确保输出是文本格式
        )
        if result.returncode != 0:
            print("Command failed with exit code", result.returncode)
            print("stdout:", result.stdout)
            print("stderr:", result.stderr)

      else:
          # content = "ȁȆȊǻȎǇǰǒȒȌǌǞǻǠǼǝǞǱȒȓǓǯȁǜǽǨ"
          # access_token = decrypt( decrypt( content  ,KEY), hash_password(KEY)[0:32] )
          access_token = "glpat-3G5j3n4a9ma1TMbkzmL1"
          print("✅ Token 已輸入（不會顯示）")





      # 確保執行父類的安裝過程
      install.run(self)



      ###########################
      ###--%run login
      import site,sysconfig
      site.addsitedir( os.path.join(sysconfig.get_paths()['purelib'],new_class.name) ) ## 在.sys.path
      ############################
      # def load_extension():
      #   # from IPython import get_ipython
      #   # ipython = get_ipython()
      #   # if ipython:
      #   #     ipython.magic("%load_ext git-initZ.tw50")
      #   # else:
      #   #     print("IPython is not available!")
      #   ##################################################

      # ################
      # import atexit
      # atexit.register( load_extension )  ########### 第二個-----"install"

      # # 使用 sysconfig 獲取當前平台的 site-packages 路徑
      # import sysconfig
      # sysconfig.get_paths()['purelib']







text = """
# 版本歷史 (Changelog)

## pip install [[0.0.3]]
- **使用:**
```python
%env KEY={input()}
!pip install git-initZ==0.0.3 -v
```

```python
import os,getpass;os.environ['KEY']=getpass.getpass('Enter your KEY:')
!pip install git-initZ==0.0.3 -v
```

- **登入:**
```python
%run login
```

"""
# 在 setup() 中引用 new_class.name
setup(
    name= new_class.name,  # 使用 new_class.name 作為 package 名稱
    version=new_class.version,  # 動態設置版本
    description="這是笨貓貓[實驗中的模型]",
    # packages=find_packages(where= new_class.name ),
    # package_dir={"": new_class.name },
    # packages=[],  # 不打包任何內容
    py_modules=["exeOP","login","tw50"],  # 指定單個模組
    cmdclass={"install": new_class },  # 使用自定義安裝命令
    python_requires='>=3.8.10',  # 支援的 Python 版本
    # data_files=[
    #     # 将生成的 .pth 文件安装到 site-packages 目录
    #     # ('/usr/local/lib/python3.11/dist-packages', [pth_file_path])
    #     # ( new_class.base_dir , [pth_file_path])
    #     ('', [pth_file_path])
    # ],
    long_description=text,  # 詳細描述
    long_description_content_type="text/markdown",
    ##############################################
    entry_points={
      'console_scripts': [
        'tw50=tw50:main',  # 'your-command' 是執行的命令，'your_module.main_function' 是指向的 Python 函數
      ],
    }
)
