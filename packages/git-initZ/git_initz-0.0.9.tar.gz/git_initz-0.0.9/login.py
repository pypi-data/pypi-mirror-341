from IPython.core.magic import register_line_magic, register_cell_magic, register_line_cell_magic
def   load_ipython_extension(ipython):
  """这个函数在扩展加载时被调用"""
  print(" [[colab XXX 模組已加载]]！！")
  ###############################
  ## 單行魔法註冊
  # ipython.register_magic_function( text, 'line')
  # ipython.register_magic_function( get_colab, 'line')
  @register_line_magic
  # 自訂單行魔法命令
  def XXX( name=None ):
    from google.colab import auth
    auth.authenticate_user()

# print(123)

from google.colab import auth
auth.authenticate_user()
# !gcloud auth list
#################################
from google.colab import drive
drive.mount('/content/drive')

