import streamlit as st
import pandas as pd
import pandas_datareader.data as web
import datetime
from backtesting import Backtest, Strategy # バックテスト、ストラテジー
from backtesting.lib import crossover
from backtesting.test import SMA # SMAインジケータ

st.title('単純移動平均戦（SMA）を用いた株の分析')


 
date1=st.date_input('開始日を選んでください',datetime.date(2020,1,1))

date2=st.date_input('終了日を選んでください')

stock = st.text_input("ティッカーシンボルを入力してください", value='AAPL')

short_period = st.number_input('短期SMA', value=10)
long_period=st.number_input('長期SMA', value=30)




data = web.DataReader(stock, 'yahoo', date1, date2)

class SmaCross(Strategy):
    n1 = short_period # 短期SMA
    n2 = long_period # 長期SMA

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1) 
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self): #チャートデータの行ごとに呼び出される
        if crossover(self.sma1, self.sma2): #sma1がsma2を上回った時
            self.buy() # 買い
        elif crossover(self.sma2, self.sma1):
            self.position.close() #ポジション降りる


bt = Backtest(
    data, # チャートデータ
    SmaCross, # 売買戦略
    cash=10000000, # 最初の所持金
    commission=0.00495, # 取引手数料
    margin=1, # レバレッジ倍率の逆数（0.5で2倍レバレッジ）
    trade_on_close=True # True：現在の終値で取引，False：次の時間の始値で取引
)

output = bt.run() # バックテスト実行
print(output) # 実行結果(データ)
st.plot() # 実行結果（グラフ）

st.write("【結果】 最初の所持金　1000000 手数料　0.00495 チャートはHtmlを別途参照ください")
st.write(output)

output2=bt.optimize(n1=range(2, 50, 10),n2=range(2, 50, 10), maximize='Equity Final [$]')
print(output2)
st.plot(output2)

st.write("最適化")
st.write(output2)




