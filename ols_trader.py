#
# OLS Trader
#
import tpqoa
import numpy as np
import pandas as pd

lags = 5
reg = np.array([-0.07225306,  0.00535411, -0.03310044, -0.00846038, -0.03408458])

class OLSTrader(tpqoa.tpqoa):
    def __init__(self, creds_file):
        super().__init__(creds_file)
        self.tick_data = pd.DataFrame()
        self.position = 0
        self.min_bars = lags + 2
    def on_success(self, time, bid, ask):
        # 1. collect the tick data
        mid = (bid + ask) / 2
        df = pd.DataFrame({'bid': bid, 'mid': mid, 'ask': ask},
                          index=[pd.Timestamp(time)])
        self.tick_data = pd.concat((self.tick_data, df))
        # 2. resample the tick data
        self.data = self.tick_data.resample('3s', label='right').last().ffill()
        self.data['r'] = np.log(self.data['mid'] / self.data['mid'].shift(1))
        # 3. generate signals/check for trades
        print(self.ticks, end=' ')
        if len(self.data) > self.min_bars:
            self.min_bars += 1
            signal = np.sign(np.dot(self.data['r'].iloc[-(lags + 1):-1], reg))
            if self.position in [0, -1] and signal == 1:
                # go long
                print(f'signal={signal} | going long')
                self.position = 1
            elif self.position in [0, 1] and signal == -1:
                # go short
                print(f'signal={signal} | going short')
                self.position = -1
        # 4. place trades

ols = OLSTrader('../oanda.cfg')
ols.stream_data('BCO_USD', stop=75)
print(ols.tick_data.info())
