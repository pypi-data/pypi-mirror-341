#%%file /usr/local/lib/python3.11/dist-packages/git-initZ/tw50.py

from IPython.core.magic import register_line_magic, register_cell_magic, register_line_cell_magic
# 自訂單行魔法命令
@register_line_magic
def date(line):

  date_picker=None
  # 啟用元件
  from google.colab import output
  output.enable_custom_widget_manager()
  # 安裝 ipydatetime 套件
  # !pip install ipydatetime -q
  # !pip install ipywidgets -q
  ###########################
  import ipywidgets as widgets
  from IPython.display import display, Javascript
  import datetime

  if "BL" in globals():
    # globals()["BL"]
    pass
  else:
    # globals()["BL"]=datetime.date.today()
    globals()["BL"]=None
  #################

  # 創建日期選擇器
  date_picker = widgets.DatePicker(
      description='選擇日期:',
      value=globals()["BL"],
      disabled=False
  )


  ########### main_start_go
  # 定義回呼函數，當日期變更時觸發
  def on_date_change(change):
      # if "py_date" not in globals():
      #   globals()['py_date']=""
      # global py_date
      py_date = change['new']
      if py_date:
        print(f'🚀 您選擇的日期是: {py_date}')
          # 移除監聽器，這樣只會監聽一次
        date_picker.unobserve(on_date_change, names='value')
        # 重置為空，讓日期選擇器回到初始狀態
        date_picker.layout.visibility = 'hidden'  # 隱藏選擇器
        # date_picker.layout.visibility = 'visible'  # 恢復顯示
        ###############
        # globals()["BL"]=str(py_date)
        import datetime
        # 轉成 datetime.date 物件
        globals()["BL"]=datetime.datetime.strptime(str(py_date), "%Y-%m-%d").date()
        ###############
        # import IPython
        # return IPython.get_ipython().run_line_magic('tw', "")


  # 設定日期範圍
  def get_script(min_date = '2020-01-01',max_date = '2025-12-31'):

    # 使用 JavaScript 設定 min 和 max 屬性
    script = Javascript(f"""
    const date_input = document.querySelector('.widget-datepicker input');
    if (date_input) {{
        // date_input.setAttribute('min', '{min_date}');
        date_input.setAttribute('max', '{max_date}');
    }}
    """)
    return script


  # 監聽日期選擇器的值變化
  date_picker.observe(on_date_change, names='value')
  # display(date_picker, get_script())
  if line!="" and not(globals()['BL'] is None):
    return (date_picker.value).strftime("%Y-%m-%d")
  else:
    # return date_picker
    # display(date_picker)
    display(date_picker, get_script( max_date=datetime.date.today() ))
  




def csv_df(file_name="工作表1"):
  # file_id = get_list_csv( file_name)
  file_id = "1--kz-a0uXZRN04w4QlFwSTJYh_R-CvtR"
  import requests
  import pandas as pd
  from io import StringIO
  try:
    download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    return pd.read_csv(StringIO(requests.get(download_url).text))
  except:
    print("XXX")
    pass


def get_0050(start="2023-01-01",end=None,id=None):
# def get_0050(start_date = "2010-01-01"):
  ######################## 自訂的 0050
  start_date,end_date = start,end
  if id:
    # if not name in df['股票代碼'].to_list():
      # print("@ 沒有在50大內 @")
      # return None
    # KK50 = [str(name)+".TW"]
      #  df =csv_df()
      ########################
      # !pip install yfinance
      import yfinance as yf
      import datetime
      import pandas as pd
      # 設定歷史資料範圍
      # start_date = "2010-01-01"
      # start_date = (dt.strptime("2010-01-01","%Y-%m-%d")-td(days=(N))).strftime("%Y-%m-%d")
      if end_date:
        end_date = datetime.datetime.now()

      # 抓取歷史股價資料
      # df.loc[:,"股票代碼"] = df["股票代碼"].str.upper() ##df["股票代碼"].astype(str).str.upper()
      # KK50 = df['股票代碼'].to_list()
      # print(KK50)

      data = yf.download( str(id)+".TW" , start=start_date, end=end_date, multi_level_index=False , auto_adjust= False )
      # ,rounding=True ### 自動四捨五入
      data.insert(0, 'id',id)
      return data
  else:
      df =csv_df()
      ########################
      # !pip install yfinance
      import yfinance as yf
      import datetime
      import pandas as pd
      # 設定歷史資料範圍
      # start_date = "2010-01-01"
      # start_date = (dt.strptime("2010-01-01","%Y-%m-%d")-td(days=(N))).strftime("%Y-%m-%d")
      if end_date:
        end_date = datetime.datetime.now()

      # 抓取歷史股價資料
      df.loc[:,"股票代碼"] = df["股票代碼"].str.upper() ##df["股票代碼"].astype(str).str.upper()
      KK50 = df['股票代碼'].to_list()
      # print(KK50)

      data = yf.download( KK50 , start=start_date, end=end_date, group_by='ticker',auto_adjust= False)
      # 合併所有股票的資料
      ddd = pd.concat([data[ticker] for ticker in KK50 ], axis=0, keys= KK50 )
      # ddd = ddd.reset_index(level=1)
      # ddd = ddd.reset_index(level=0)
      # ddd.index.names
      ddd = (ddd.reset_index(level=1).reset_index(level=0)).rename(columns={'index':'tickers'})
      # 指定欄位順序
      ddd[['tickers', 'Date', 'Open', 'High', 'Low', 'Close','Adj Close', 'Volume']]
      # #儲存檔案
      # ddd.to_csv('/content/drive/MyDrive/Colab Notebooks/data/股票/0050股票.csv', index=False)
      # ddd
      #2# 新增一個中文欄位名稱 如:下載 ETF0050 五十檔 (含tickers, tickersName, Date, Open, High, Low, Close, AdjClose, Volume)
      ######################
      ddd2 = ddd.copy()
      # 使用 join 根據索引合併，只選擇 股票名稱 欄位
      ddd2 = ddd.set_index('tickers').join( df.set_index('股票代碼')[['股票名稱']] ).reset_index(level='tickers')
      # ddd2[['tickers', 'tickersName', 'Date', 'Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']]

      # 移動欄位
      N=ddd2.columns.get_loc('tickers') ## 索引位置
      ddd2.insert(N+1,'tickersName', ddd2.pop('股票名稱')) ## 插入
      return ddd2.copy()
  ########################
# get_0050(id=2330)
# get_0050()


# get_0050(name=3300)
# import pandas as pd
# def calculate_indicators(group):
def tablib_group(group):
    import talib
    group['K'], group['D'] = talib.STOCH(group['High'], group['Low'], group['Close'], fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    group['RSI'] = talib.RSI(group['Close'], timeperiod=14)
    group['MACD'], group['MACD_signal'], group['MACD_hist'] = talib.MACD(group['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    group['MA5'] = talib.SMA(group['Close'], timeperiod=5)
    group['MA10'] = talib.SMA(group['Close'], timeperiod=10)
    group['MA20'] = talib.SMA(group['Close'], timeperiod=20)
    group['MA60'] = talib.SMA(group['Close'], timeperiod=60)
    group['MA120'] = talib.SMA(group['Close'], timeperiod=120)
    group['MA240'] = talib.SMA(group['Close'], timeperiod=240)
    group['MA5乖離率'] = (group['Close'] - group['MA5']) / group['MA5']
    group['MA20乖離率'] = (group['Close'] - group['MA20']) / group['MA20']
    group['William%R'] = talib.WILLR(group['High'], group['Low'], group['Close'], timeperiod=14)
    group['ROC'] = talib.ROC(group['Close'], timeperiod=10)
    group['ATR'] = talib.ATR(group['High'], group['Low'], group['Close'], timeperiod=14)
    group['CCI'] = talib.CCI(group['High'], group['Low'], group['Close'], timeperiod=14)
    group['MFI'] = talib.MFI(group['High'], group['Low'], group['Close'], group['Volume'], timeperiod=14)
    group['ADX'] = talib.ADX(group['High'], group['Low'], group['Close'], timeperiod=14)
    group['OBV'] = talib.OBV(group['Close'], group['Volume'])

    # 布林通道
    group['upperband'], group['middleband'], group['lowerband'] = talib.BBANDS(group['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    return group
    ######  排除特定的列
    # return  group.drop(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
    # return  group.drop(columns=['Open', 'High', 'Low', 'Close',  'Volume'])



# 定义另一个方法，接受函数作为参数
def df_data(Z,N=12,func=tablib_group,id=None):
    print(Z,N)
    from datetime import datetime as dt;
    from dateutil.relativedelta import relativedelta
    # timeZ = ( dt.strptime( Z , "%Y-%m-%d")-relativedelta(months= N*2 )).strftime("%Y-%m-%d")
    # ##########################################
    # df = get_0050( start=timeZ )
    # df = func(df)
    # df = df.loc[df['Date'] >= f'{Z}']
    # ###########################################
    # df,sum = None,0
    import time
    UU=1
    # # while (df is None) or df.isna().any().any():
    while func:
      time.sleep(1)
      # sum+=1
      timeZ = ( dt.strptime( Z , "%Y-%m-%d")-relativedelta( months =UU*N )).strftime("%Y-%m-%d")
      print( timeZ )
      ##########################################
      df = get_0050( start=timeZ ,id=id)
      df = func(df)
      ################ 當[不是]單一股票
      if id is None:
        df = df.loc[df['Date'] >= f'{Z}']
        ###########################################
        # dff = df.copy() # 修改索引
        df.set_index('tickers',inplace=True)
        df.index = df.index.str.replace('.TW', '').astype(int)
        # dff.loc[2330]
        ###########################################
      else:
        # 假设 df 的索引是 'Date'
        df = df.loc[df.index >= f'{Z}']
        ###########################################


      if not(df.isna().any().any()):
        break
      else:
        UU+=1
        pass
      ###########################################
      print(df.isna().any())
    ##########################################
    ###########################
    # dd.isna().any()#.any()  #### 可以查看是哪一個欄位
    # dd.isna().any().any()  #### np.False_ 才代表沒有 nan
    ############################################
    globals()["df_all"]=df.copy()
    ###########################################
    return df
# 2021-12-01

# df = df_data("2023-01-01",12)
# df = df_data("2023-01-01")


##############################################
def check_talib():
  try:
    import talib
    return True
  except:
    return False
if not(check_talib()):
  ##############################################
  import subprocess
  url = 'https://anaconda.org/conda-forge/libta-lib/0.4.0/download/linux-64/libta-lib-0.4.0-h166bdaf_1.tar.bz2'
  commands = [
  f"curl -s -L {url} | tar xj -C /usr/lib/x86_64-linux-gnu/ lib --strip-components=1",
  "pip install -q conda-package-handling",
  "wget -q https://anaconda.org/conda-forge/ta-lib/0.5.1/download/linux-64/ta-lib-0.5.1-py311h9ecbd09_0.conda",
  "cph x ta-lib-0.5.1-py311h9ecbd09_0.conda",
  "mv ./ta-lib-0.5.1-py311h9ecbd09_0/lib/python3.11/site-packages/talib /usr/local/lib/python3.11/dist-packages/  >/dev/null 2>&1",
  # !wget -O TaipeiSansTCBeta-Regular.ttf https://drive.google.com/uc?id=1eGAsTN1HBpJAkeVM57_C7ccp7hbgSz3_&export=download
  ]
  for command in commands:
      subprocess.run(command, shell=True)
      print(123456)
  ##############################################
  import gdown
  url = "https://drive.google.com/uc?id=1eGAsTN1HBpJAkeVM57_C7ccp7hbgSz3_"
  output = "TaipeiSansTCBeta-Regular.ttf"
  gdown.download(url, output, quiet=False)
  import matplotlib as mpl
  from matplotlib.font_manager import fontManager
  fontManager.addfont('TaipeiSansTCBeta-Regular.ttf')
  mpl.rc('font', family='Taipei Sans TC Beta')
##############################################


# dd
from IPython.core.magic import register_line_magic, register_cell_magic, register_line_cell_magic
def  load_ipython_extension(ipython):
    ##############################################
    # for name in list(set(df.index.to_list())):
    # def func(line):
    #   dff = df.loc[int(line)].copy() ## 先複製--以免修改到原本的
    #   dff.set_index('Date', inplace=True) ## 取代!!
    #   return dff
    #   # # 將 'Date' 欄位轉換為日期格式，並設為索引
    #   # df3['Date'] = pd.to_datetime(df3['Date'])
    #   # df3.set_index('Date', inplace=True)


    # # 將生成的函數名稱註冊為魔法命令
    # globals()["df"+str(name)] = func  # 使用 `globals()` 註冊到全局命名空間
    # register_line_magic(globals()["df"+str(name)])  # 註冊魔法命令
    #############################################
    # 自訂單行魔法命令
    @register_line_magic
    def dff(line):
      # text=''''''
      # return exec(text,globals())
      # print(line in globals()  )
      # return eval(line,globals())
      global df_all
      df = df_all.loc[int(line)].copy() ## 避免覆蓋
      df.set_index('Date', inplace=True) ## 取代!!
      df = df.sort_index()        # 確保::確保索引按日期排序
      # df.loc['2025-01-01':'2025-01-03']# 否者::無法這樣讀取時間
      return df

    # dff = %tw50 2023-01-01
    # 自訂單行魔法命令
    @register_line_magic
    def tw(line):
      print("股票:",line)
      import IPython
      SS = IPython.get_ipython().run_line_magic('date', line)

      if line!="" and not(globals()['BL'] is None):
        
        # print(3)
        return df_data(str(SS),id=line) ### 單一股票!?  
      
      # elif line!="" and (globals()['BL'] is None):
        
      #   print(2)
      #   return IPython.get_ipython().run_line_magic('date',"")
      else:
        # print(1)
        return SS ### 這樣才會顯示[視窗]  



    # 自訂單行魔法命令
    @register_line_magic
    def tw50(line):
      if line == "load":
        from IPython import get_ipython
        get_ipython().magic('load /usr/local/lib/python3.11/dist-packages/git-initZ/tw50.py')
        return None

      if line == "exit":
        text='''
from google.colab import runtime
runtime.unassign()  # 斷開當前會話並重新連接'''
        return exec(text,globals())

      # import re
      # if re.match(r'^\d{4}$', line):
      #   print(f"4位數字檢查成功，輸入的數字是: {line}")



      ######  排除特定的列
      # return  group.drop(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

      ##################
      RR = line.split()
      # RR = [ datetime(*map(int,i.split("-"))) if i.find("-")!=-1 else i  for i in RR]
      RR = [ int(i) if i.find("-")==-1 else i if i.find("-")!=-1 else i  for i in RR]

      # # # print( [f'"{i}"' if i.find("-")!=-1 else i  for i in RR] )
      # import os
      # dd = os.path.dirname(__file__)
      # print(dd)
      # text=open(dd+os.path.sep+"df_data.py").read()
      # exec(text,globals())
      # globals()['dff'] = df_data(*RR)

      ##########################################################################
      import gdown
      url = "https://drive.google.com/uc?id=1eGAsTN1HBpJAkeVM57_C7ccp7hbgSz3_"
      output = "TaipeiSansTCBeta-Regular.ttf"
      gdown.download(url, output, quiet=False)
      import matplotlib as mpl
      from matplotlib.font_manager import fontManager
      fontManager.addfont('TaipeiSansTCBeta-Regular.ttf')
      mpl.rc('font', family='Taipei Sans TC Beta')
      ###########################################################################
      return df_data(*RR)


    # RR = ['2023-01-01', 12]
    # df_data(*RR,tablib_group)
