#
# OLS Trader
#
# To trade an instrument on https://oanda.com
#
import tpqoa
import numpy as np
import pandas as pd

lags = 5
reg = np.array([-0.25315629, -0.16066948,  0.00659208, -0.09456194, -0.16094345]) 

class OLSTrader(tpqoa.tpqoa):
    def __init__(self, creds_file, units):
        super().__init__(creds_file)
        self.trading_units = units
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
        self.data = self.tick_data.resample('5s', label='right').last().ffill()
        self.data['r'] = np.log(self.data['mid'] / self.data['mid'].shift(1))
        # 3. generate signals/check for trades/place trades
        print(self.ticks, end=' ')
        if len(self.data) > self.min_bars:
            self.min_bars += 1
            signal = np.sign(np.dot(self.data['r'].iloc[-(lags + 1):-1], reg))
            if self.position in [0, -1] and signal == 1:
                # go long
                print(f'signal={signal} | going long')
                self.create_order(self.stream_instrument,
                                  units=(1 - self.position) * self.trading_units)
                self.position = 1
            elif self.position in [0, 1] and signal == -1:
                # go short
                print(f'signal={signal} | going short')
                self.create_order(self.stream_instrument,
                                  units=-(1 + self.position) * self.trading_units)
                self.position = -1
if __name__ == '__main__':
    ols = OLSTrader('../oanda.cfg', units=10)
    print('*** GETTING STARTED STREAMING ***')
    ols.stream_data('BCO_USD', stop=125)
    print('*** CLOSING OUT FINAL POSITION ***')
    ols.create_order(ols.stream_instrument, units=-ols.position * ols.trading_units)
    # print(ols.tick_data.info())
