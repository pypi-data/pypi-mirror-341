import pandas as pd
import numpy as np
import ta
from collections import deque

def kst(data):
    kst = pd.to_datetime(data, unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Seoul').dt.strftime('%Y-%m-%d %H:%M:%S')
    return kst

def rsi(data, length=14):
    return ta.momentum.RSIIndicator(close=data, window=length).rsi().fillna(0)

def atr(df, length=14):
    _df = df.copy()
    _df['HL'] = _df['high'] - _df['low']  # 고가와 저가의 차이
    _df['HC'] = abs(_df['high'] - _df['close'].shift())  # 고가와 이전 종가의 차이
    _df['LC'] = abs(_df['low'] - _df['close'].shift())  # 저가와 이전 종가의 차이
    
    _df['TR'] = _df[['HL', 'HC', 'LC']].max(axis=1)
    return _df['TR'].ewm(alpha=1/length, adjust=False).mean()

def ema(df, length=9):
    return df.ewm(span=length, adjust=False).mean()

def sma(df, length=9):
    return df.rolling(window=length).mean()

def rma(series, period):
    alpha = 1 / period
    return series.ewm(alpha=alpha, adjust=False).mean()

def dirmov(df, length):
    high, low = df['high'], df['low']
    
    up = high.diff()
    down = -low.diff()

    plusDM = np.where((up > down) & (up > 0), up, 0)
    minusDM = np.where((down > up) & (down > 0), down, 0)
    
    tr = atr(df)

    smoothed_tr = rma(tr, length)
    smoothed_plusDM = rma(pd.Series(plusDM), length)
    smoothed_minusDM = rma(pd.Series(minusDM), length)
    
    plus = 100 * smoothed_plusDM / smoothed_tr
    minus = 100 * smoothed_minusDM / smoothed_tr

    return plus, minus

def adx(df, dilen=14, adxlen=14):

    plus, minus = dirmov(df, dilen)
    sum_dm = plus + minus
    dx = abs(plus - minus) / (sum_dm.replace(0, 1))
    adx = rma(dx, adxlen)
    adx = 100 * adx
    return adx

def line_cross(df, src='close', short_length=9, long_length=21, uptext='up', downtext='down'):
    _df = df.copy()
    _df['short'] = _df[src].rolling(window=short_length).mean()
    _df['long'] = _df[src].rolling(window=long_length).mean()

    return np.where((_df['short'] > _df['long']) & (_df['short'].shift(1) <= _df['long'].shift(1)), uptext,
        np.where((_df['short'] < _df['long']) & (_df['short'].shift(1) >= _df['long'].shift(1)), downtext, ''))

def stoch_rsi(df, src='close', length=14):
    _df = df.copy()
    _df['K'] = ta.momentum.StochRSIIndicator(close=df[src], window=length).stochrsi_k()
    _df['D'] = ta.momentum.StochRSIIndicator(close=df[src], window=length).stochrsi_d()
    _df['K'] = (_df['K'].fillna(0) * 100)
    _df['D'] = (_df['D'].fillna(0) * 100)
    return (_df['K'], _df['D'])

def wma(df, length):
    weights = np.arange(1, length + 1)
    return df.rolling(length).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

def hull(df, src='close', length=9):
    wma_half = wma(df[src], int(length / 2))
    wma_full = wma(df[src], length)
    return wma(2 * wma_half - wma_full, int(np.sqrt(length)))

def macd(df, src='close', fast_length=12, slow_length=26, signal_length=9):
    _df = df.copy()
    _df['fast'] = ema(_df[src], length=fast_length)
    _df['slow'] = ema(_df[src], length=slow_length)
    _df['MACD'] = _df['fast'] - _df['slow']
    _df['signal'] = ema(_df['MACD'], length=signal_length)
    _df['histogram'] = _df['MACD'] - _df['signal']
    return _df[['MACD', 'signal', 'histogram']]

def impulse_macd(df, ma=34, signal=9):
    _df = df.copy()
    close = _df['close']
    high = _df['high']
    low = _df['low']

    _df['hlc3'] = (high + low + close) / 3
    _df['hlc3'] = _df['hlc3']
    _df['hi'] = high.ewm(alpha=1/ma, adjust=False).mean()
    _df['lo'] = low.ewm(alpha=1/ma, adjust=False).mean()

    ema1 = _df['hlc3'].ewm(span=ma, adjust=False).mean()
    ema2 = ema1.ewm(span=ma, adjust=False).mean()
    d = ema1 - ema2
    _df['mi'] = ema1 + d

    # Impulse MACD Value
    _df['ImpulseMACD'] = np.where(_df['mi'] > _df['hi'], _df['mi'] - _df['hi'],
                          np.where(_df['mi'] < _df['lo'], _df['mi'] - _df['lo'], 0))

    # Signal Line
    _df['ImpulseMACDSignal'] = _df['ImpulseMACD'].rolling(window=signal).mean()

    # Histogram
    _df['Histo'] = _df['ImpulseMACD'] - _df['ImpulseMACDSignal']

    _df['ImpulseMACD'] = _df['ImpulseMACD'].fillna(0)
    _df['ImpulseMACDSignal'] = _df['ImpulseMACDSignal'].fillna(0)
    _df['Histo'] = _df['Histo'].fillna(0)
    
    return _df[['ImpulseMACD', 'ImpulseMACDSignal', 'Histo']]

def ha_candle(df):
    _df = df.copy()
    _df['HA_Close'] = (_df['open'] + _df['high'] + _df['low'] + _df['close']) / 4
    
    # open
    for i in range(len(_df)):
        if i == 0:
            _df['HA_Open'] = (_df['open'].iloc[0] + _df['close'].iloc[0]) / 2
        else :
            _df.loc[i,'HA_Open'] = (_df['HA_Open'].iloc[i-1] + _df['HA_Close'].iloc[i-1]) / 2
   
    _df['HA_Open'] = _df['HA_Open'] # open
    _df['HA_High'] = _df[['high', 'HA_Open', 'HA_Close']].max(axis=1) # high
    _df['HA_Low'] = _df[['low', 'HA_Open', 'HA_Close']].min(axis=1) # low
    _df['HA_Close'] = _df['HA_Close'] # close
    return _df[['HA_Open','HA_High','HA_Low','HA_Close']]

def bband(df, src='close', length=20, factor=2.0, ddof=0):
    _df = df.copy()
    moving_average = _df[src].rolling(window=length).mean()
    
    std_dev = _df[src].rolling(window=length).std(ddof=ddof) * factor
    upper_band = moving_average + std_dev
    lower_band = moving_average - std_dev

    _df['basis'] = moving_average
    _df['upper'] = upper_band
    _df['lower'] = lower_band
    return _df[['basis','upper','lower']]

def ut_bot_alert(df, src='close', key_value=1, atr_period=10):

    _df = df.copy()
    src = _df[src]
    _df['ATR'] = atr(_df, atr_period)
    _df['nLoss'] = key_value * _df['ATR']
    _df['xATRTrailingStop'] = np.nan

    for i in range(len(_df)):
        prev_stop = _df['xATRTrailingStop'].iloc[i - 1] if i > 0 else 0
        prev_close = src.iloc[i - 1] if i > 0 else 0

        if src.iloc[i] > prev_stop and prev_close > prev_stop:
            _df.loc[i, 'xATRTrailingStop'] = max(prev_stop, src.iloc[i] - _df['nLoss'].iloc[i])
        elif src.iloc[i] < prev_stop and prev_close < prev_stop:
            _df.loc[i, 'xATRTrailingStop'] = min(prev_stop, src.iloc[i] + _df['nLoss'].iloc[i])
        else:
            _df.loc[i, 'xATRTrailingStop'] = (
                src.iloc[i] - _df['nLoss'].iloc[i]
                if src.iloc[i] > prev_stop
                else src.iloc[i] + _df['nLoss'].iloc[i]
            )

    _df['Buy'] = (
        (src > _df['xATRTrailingStop']) &
        (src.shift(1) <= _df['xATRTrailingStop'].shift(1))
    )
    _df['Sell'] = (
        (src < _df['xATRTrailingStop']) &
        (src.shift(1) >= _df['xATRTrailingStop'].shift(1))
    )

    return _df.apply(lambda row: 'Buy' if row['Buy'] else ('Sell' if row['Sell'] else ''), axis=1)

def ema_trend_meter(df, src='close', base=1, ema1=7, ema2=14, ema3=21):
    _df = df.copy()
    _df[f"EMA0"] = df[src].ewm(span=base, adjust=False).mean()
    _df[f"EMA1"] = df[src].ewm(span=ema1, adjust=False).mean()
    _df[f"EMA2"] = df[src].ewm(span=ema2, adjust=False).mean()
    _df[f"EMA3"] = df[src].ewm(span=ema3, adjust=False).mean()

    _df['Bull1'] = _df['EMA1'] < _df['EMA0']
    _df['Bull2'] = _df['EMA2'] < _df['EMA0']
    _df['Bull3'] = _df['EMA3'] < _df['EMA0']

    return _df[['Bull1','Bull2','Bull3']]

def williams_r(df, length=14):
    _df = df.copy()
    highest_high = _df['high'].rolling(window=length).max()
    lowest_low = _df['low'].rolling(window=length).min()
    _df['R'] = 100 * (_df['close'] - highest_high) / (highest_high - lowest_low)
    return _df['R']

def dc(df, length=20):
    _df = df.copy()
    _df['upper'] = _df['high'].rolling(window=length).max()
    _df['lower'] = _df['low'].rolling(window=length).min()
    _df['basis'] = ((_df['upper'] + _df['lower']) / 2)

    return _df[['basis','upper','lower']]

def mfi(df, length=14):
    _df = df.copy()
    _df['hlc3'] = (_df['high'] + _df['low'] + _df['close']) / 3
    delta = _df['hlc3'].diff()

    upper = (_df['volume'] * np.where(delta > 0, _df['hlc3'], 0)).rolling(window=length).sum()
    lower = (_df['volume'] * np.where(delta < 0, _df['hlc3'], 0)).rolling(window=length).sum()

    _df['MFI'] = 100.0 - (100.0 / (1.0 + (upper / lower)))
    return _df['MFI']

def hull(df, src='close', length=9):
    _df = df.copy()
    wma_half = wma(_df[src], int(length / 2))
    wma_full = wma(_df[src], length)
    _df['hull'] = wma(2 * wma_half - wma_full, int(np.sqrt(length)))
    return _df['hull']

def ema_trend_meter(df, src='close', base=1, ema1=7, ema2=14, ema3=21):

    _df = df.copy()
    _df[f"EMA0"] = df[src].ewm(span=base, adjust=False).mean()
    _df[f"EMA1"] = df[src].ewm(span=ema1, adjust=False).mean()
    _df[f"EMA2"] = df[src].ewm(span=ema2, adjust=False).mean()
    _df[f"EMA3"] = df[src].ewm(span=ema3, adjust=False).mean()

    _df['Bull1'] = _df['EMA1'] < _df['EMA0']
    _df['Bull2'] = _df['EMA2'] < _df['EMA0']
    _df['Bull3'] = _df['EMA3'] < _df['EMA0']
    _df['etm_signal'] = _df.apply(lambda row: 'LONG' if row['Bull1'] and row['Bull2'] and row['Bull3'] else ('SHORT' if not row['Bull1'] and not row['Bull2'] and not row['Bull3'] else ''), axis=1)

    return _df[['Bull1','Bull2','Bull3', 'etm_signal']]

def psar(df, step=0.02, max_step=0.2):
    _df = df.copy()
    sar = ta.trend.PSARIndicator(high=_df['high'], low=_df['low'], close=_df['close'], step=step, max_step=max_step).psar()
    _df['PSAR'] = sar
    _df['PSAR_TREND'] = np.where(_df['close'] > _df['PSAR'], '1', np.where(_df['close'] < _df['PSAR'], '-1', '0'))
    return _df[['PSAR', 'PSAR_TREND']]

def ichimoku(df, conversion=9, base=26, spanb=52):
    _df = df.copy()
    data = ta.trend.IchimokuIndicator(high=_df['high'], low=_df['low'], window1=conversion, window2=base, window3=spanb)
    _df['conversion_line'] = data.ichimoku_conversion_line()
    _df['base_line'] = data.ichimoku_base_line()
    _df['lag'] = _df['close']
    _df['spanA'] = data.ichimoku_a()
    _df['spanB'] = data.ichimoku_b()
    return _df[['conversion_line','base_line', 'lag', 'spanA', 'spanB']]

def trix(df, len=18):
    _df = df.copy()
    close = np.log(_df['close'])
    ema1 = ema(close, len)
    ema2 = ema(ema1, len)
    ema3 = ema(ema2, len)
    _df['TRIX'] = (10000 * np.diff(ema3, prepend=ema3[0]))
    return _df['TRIX']

def ultimate_oscillator(df, fast=7, middle=14, slow=28):
    _df = df.copy()
    uo = ta.momentum.ultimate_oscillator(
        high=_df['high'], 
        low=_df['low'], 
        close=_df['close'], 
        window1=fast, 
        window2=middle, 
        window3=slow
    )
    _df['UO'] = uo
    return _df['UO']

def rate_of_change(df, src='close', len=9):
    _df = df.copy()
    close = df[src]
    roc = (close - close.shift(len)) / close.shift(len)
    _df['ROC'] = (roc * 100)
    return _df['ROC']

def aroon(df, len=14):
    _df = df.copy()
    data = ta.trend.AroonIndicator(high=_df['high'], low=_df['low'], window=len)
    _df['aroon_up'] = data.aroon_up()
    _df['aroon_down'] = data.aroon_down()
    return _df[['aroon_up', 'aroon_down']]

def mass_index(df, len=10):
    _df = df.copy()
    data = ta.trend.MassIndex(high=_df['high'], low=_df['low'], window_slow=len)
    _df['MASS'] = data.mass_index()
    return _df['MASS']

def ppo(df, fast=12, slow=26, signal=9):
    _df = df.copy()
    data = ta.momentum.PercentagePriceOscillator(
        close=_df['close'], 
        window_fast=fast, 
        window_slow=slow, 
        window_sign=signal
    )
    _df['ppo_histo'] = data.ppo_hist()
    _df['ppo'] = data.ppo()
    _df['ppo_signal'] = data.ppo_signal()
    return _df[['ppo_histo', 'ppo', 'ppo_signal']]

def awesome_oscillator(df, len1=5, len2=34):
    _df = df.copy()
    hl2 = (_df['high'] + _df['low']) / 2
    _df['AO'] = (sma(hl2,len1) - sma(hl2,len2))
    _df['AO_TREND'] = np.where(_df['AO'].diff() <= 0, 'down', 'up')
    return _df[['AO', 'AO_TREND']]

def kc(df, len=20, mult=2):
    _df = df.copy()
    data = ta.volatility.KeltnerChannel(
        high=_df['high'], 
        low=_df['low'], 
        close=_df['close'], 
        window=len,
        multiplier=mult,
        original_version=False
    )
    _df['KC_H'] = data.keltner_channel_hband()
    _df['KC_M'] = data.keltner_channel_mband()
    _df['KC_L'] = data.keltner_channel_lband()
    return _df[['KC_H', 'KC_M', 'KC_L']]

def know_sure_thing(df):
    _df = df.copy()
    data = ta.trend.KSTIndicator(close=_df['close'])
    _df['KST'] = data.kst()
    _df['KST_SIGNAL'] = data.kst_sig()
    return _df[['KST', 'KST_SIGNAL']]

def tsi(df, src='close', slow=25, fast=13):
    _df = df.copy()
    data = ta.momentum.TSIIndicator(
        close=_df[src], 
        window_slow=slow, 
        window_fast=fast
    )
    _df['TSI'] = data.tsi()
    _df['TSI_SIGNAL'] = ema(df=_df['TSI'], length=fast)
    return _df[['TSI', 'TSI_SIGNAL']]

def cci(df, len=20, sma_len=14):
    _df = df.copy()
    _df['CCI'] = ta.trend.cci(high=_df['high'], low=_df['low'], close=_df['close'], window=len)
    _df['CCI_SIGNAL'] = sma(df=_df['CCI'], length=sma_len)
    return _df[['CCI', 'CCI_SIGNAL']]

def vortex(df, len=14):
    _df = df.copy()
    data = ta.trend.VortexIndicator(
        high=_df['high'], 
        low=_df['low'], 
        close=_df['close'], 
        window=len
    )
    _df['VI_P'] = data.vortex_indicator_pos()
    _df['VI_M'] = data.vortex_indicator_neg()
    return _df[['VI_P', 'VI_M']]

def np_shift(array: np.ndarray, offset: int = 1, fill_value=np.nan):
    result = np.empty_like(array)
    if offset > 0:
        result[:offset] = fill_value
        result[offset:] = array[:-offset]
    elif offset < 0:
        result[offset:] = fill_value
        result[:offset] = array[-offset:]
    else:
        result[:] = array
    return result

def linreg(source: np.ndarray, length: int, offset: int = 0):
    size = len(source)
    linear = np.zeros(size)

    for i in range(length, size):

        sumX = 0.0
        sumY = 0.0
        sumXSqr = 0.0
        sumXY = 0.0

        for z in range(length):
            val = source[i-z]
            per = z + 1.0
            sumX += per
            sumY += val
            sumXSqr += per * per
            sumXY += val * per

        slope = (length * sumXY - sumX * sumY) / (length * sumXSqr - sumX * sumX)
        average = sumY / length
        intercept = average - slope * sumX / length + slope

        linear[i] = intercept

    if offset != 0:
        linear = np_shift(linear, offset)

    return pd.Series(linear, index=source.index)

def pda(df, length=14):
    true_range = atr(df, length)
    high, low = df['high'], df['low']

    dm_plus = high - high.shift(1)
    dm_minus = low.shift(1) - low
    dm_plus = np.where(dm_plus > dm_minus, np.maximum(dm_plus, 0), 0)
    dm_minus = np.where(dm_minus > dm_plus, np.maximum(dm_minus, 0), 0)
    
    smoothed_dm_plus = pd.Series(dm_plus, index=df.index).ewm(alpha=1/length, adjust=False).mean()
    smoothed_dm_minus = pd.Series(dm_minus, index=df.index).ewm(alpha=1/length, adjust=False).mean()
    
    di_plus = (smoothed_dm_plus / true_range) * 100
    di_minus = (smoothed_dm_minus / true_range) * 100

    _df = df.copy()
    _df['DIPlus'] = di_plus.fillna(0)
    _df['DIMinus'] = di_minus.fillna(0)
    _df['ADX'] = adx(df=df).fillna(0)
    _df[['PSAR','PSAR_TREND']] = psar(df=df).fillna(0)
    _df['DIPlus_prev'] = _df['DIPlus'].shift(1)
    _df['DIMinus_prev'] = _df['DIMinus'].shift(1)
    _df['ADX_prev'] = _df['ADX'].shift(1)

    _df['DI_TREND'] = np.where(_df['DIPlus'] > _df['DIMinus'], '1', np.where(_df['DIPlus'] < _df['DIMinus'], '-1', '0'))
    _df['DI_CROSS'] = np.where(
        (_df['DIPlus_prev'] < _df['DIMinus_prev']) & (_df['DIPlus'] > _df['DIMinus']) & (_df['ADX'] >= 20),
        '1',
        np.where(
            (_df['DIPlus_prev'] > _df['DIMinus_prev']) & (_df['DIPlus'] < _df['DIMinus']) & (_df['ADX'] >= 20),
            '-1',
            '')
    )

    _df['ADX_ON'] = np.where( (_df['ADX_prev'] < 20) & (_df['ADX'] >= 20), 1, 0)

    return _df[['DIPlus', 'DIMinus', 'DI_TREND', 'DI_CROSS', 'ADX', 'ADX_ON', 'PSAR', 'PSAR_TREND']]

def clean_deque(i, k, deq, df, key, isHigh):
    if deq and deq[0] == i - k:
        deq.popleft()
    if isHigh:
        while deq and df.iloc[i][key] > df.iloc[deq[-1]][key]:
            deq.pop()
    else:
        while deq and df.iloc[i][key] < df.iloc[deq[-1]][key]:
            deq.pop()

def pivot(data=None, pivot=10):

    data['pivot_high'] = False
    data['pivot_high_Value'] = np.nan
    data['pivot_low'] = False
    data['pivot_low_value'] = np.nan
    keyHigh = 'high'
    keyLow = 'low'
    win_size = pivot * 2 + 1
    deqHigh = deque()
    deqLow = deque()
    max_idx = 0
    min_idx = 0
    i = 0
    j = pivot
    pivot_low = None
    pivot_high = None
    for index, row in data.iterrows():
        if i < win_size:
            clean_deque(i, win_size, deqHigh, data, keyHigh, True)
            clean_deque(i, win_size, deqLow, data, keyLow, False)
            deqHigh.append(i)
            deqLow.append(i)
            if data.iloc[i][keyHigh] > data.iloc[max_idx][keyHigh]:
                max_idx = i
            if data.iloc[i][keyLow] < data.iloc[min_idx][keyLow]:
                min_idx = i
            if i == win_size-1:
                if data.iloc[max_idx][keyHigh] == data.iloc[j][keyHigh]:
                    data.at[data.index[j], 'pivot_high'] = True
                    pivot_high = data.iloc[j][keyHigh]
                if data.iloc[min_idx][keyLow] == data.iloc[j][keyLow]:
                    data.at[data.index[j], 'pivot_low'] = True
                    pivot_low = data.iloc[j][keyLow]
        if i >= win_size:
            j += 1
            clean_deque(i, win_size, deqHigh, data, keyHigh, True)
            clean_deque(i, win_size, deqLow, data, keyLow, False)
            deqHigh.append(i)
            deqLow.append(i)
            pivot_val = data.iloc[deqHigh[0]][keyHigh]
            if pivot_val == data.iloc[j][keyHigh]:
                data.at[data.index[j], 'pivot_high'] = True
                pivot_high = data.iloc[j][keyHigh]
            if data.iloc[deqLow[0]][keyLow] == data.iloc[j][keyLow]:
                data.at[data.index[j], 'pivot_low'] = True
                pivot_low = data.iloc[j][keyLow]

        data.at[data.index[j], 'pivot_high_Value'] = pivot_high
        data.at[data.index[j], 'pivot_low_value'] = pivot_low
        i = i + 1
    
    return data

def qqe_signal(df, rsi_length=14, smoothing_factor=5, fast_qqe_factor=4.238):
    _rsi = rsi(df['close'], rsi_length)
    rsi_ma = ema(_rsi, length=smoothing_factor)
    
    wilders_period = rsi_length * 2 - 1
    atr_rsi = abs(rsi_ma.shift(1) - rsi_ma)
    ma_atr_rsi = ema(atr_rsi, wilders_period)
    dar = ema(ma_atr_rsi, wilders_period) * fast_qqe_factor
    
    new_short_band = (rsi_ma + dar).tolist()
    new_long_band = (rsi_ma - dar).tolist()
    long_band = [0] * len(df) 
    short_band = [0] * len(df)
    trend = [0] * len(df)
    fast_atr_rsi_tl = [0] * len(df)
    rsi_index = rsi_ma.tolist()
    
    for i in range(1, len(df)):
        long_band[i] = max(long_band[i - 1], new_long_band[i]) if rsi_index[i - 1] > long_band[i - 1] and rsi_index[i] > long_band[i - 1] else new_long_band[i]
        short_band[i] = min(short_band[i - 1], new_short_band[i]) if rsi_index[i - 1] < short_band[i - 1] and rsi_index[i] < short_band[i - 1] else new_short_band[i]

        cross_1 = long_band[i - 2] < rsi_index[i - 1] and long_band[i - 1] > rsi_index[i]
        if rsi_index[i - 1] < short_band[i - 2] and rsi_index[i] > short_band[i - 1]:
            trend[i] = 1
        else :
            if cross_1:
                trend[i] = -1
            else:
                trend[i] = trend[i - 1] if not np.isnan(trend[i - 1]) else 1

        fast_atr_rsi_tl[i] = long_band[i] if trend[i] == 1 else short_band[i]
    
    qqe_xlong = [0] * len(df)
    qqe_xshort = [0] * len(df)
    qqe_long = [None] * len(df)
    qqe_short = [None] * len(df)

    for i in range(1, len(df)):
        qqe_xlong[i] = qqe_xlong[i - 1]
        qqe_xshort[i] = qqe_xshort[i - 1]
        
        if fast_atr_rsi_tl[i] < rsi_ma[i]:
            qqe_xlong[i] += 1
        else:
            qqe_xlong[i] = 0
        
        if fast_atr_rsi_tl[i] > rsi_ma[i]:
            qqe_xshort[i] += 1
        else:
            qqe_xshort[i] = 0
        
        # QQE Long & Short 조건 반영
        if qqe_xlong[i] == 1:
            qqe_long[i] = fast_atr_rsi_tl[i - 1] - 50
        if qqe_xshort[i] == 1:
            qqe_short[i] = fast_atr_rsi_tl[i - 1] - 50

    # 6. 롱/숏 시그널 생성
    signal = [''] * len(df)
    for i in range(len(df)):
        if qqe_xlong[i] == 1:
            signal[i] = 'Long'
        elif qqe_xshort[i] == 1:
            signal[i] = 'Short'

    df['QQE_Signal'] = signal
    _df = df.copy()
    return _df[['QQE_Signal']]

def swma(series):
    return series.rolling(window=4).apply(lambda x: (x[0]*1 + x[1]*2 + x[2]*2 + x[3]*1) / 6, raw=True)

def updown(series):
    ud = np.zeros(len(series))
    if len(series) > 0:
        ud[0] = 0  # 초기값 설정
    for i in range(1, len(series)):
        prev = series.iat[i - 1]
        prev_ud = ud[i - 1] if not np.isnan(ud[i - 1]) else 0  # nz 기능 적용
        
        ud[i] = (
            0 if series.iat[i] == prev else
            1 if series.iat[i] > prev and prev_ud <= 0 else
            prev_ud + 1 if series.iat[i] > prev else
            -1 if prev_ud >= 0 else
            prev_ud - 1
        )
    return pd.Series(ud, index=series.index)

def percent_rank(series, length):
    return series.rolling(window=length).apply(lambda x: (np.sum(x < x[-1]) / (len(x) - 1) * 100) if len(x) > 1 else 0, raw=True).round()

def rvi(df, length=10):
    _df = df.copy()
    num = swma(_df['close'] - _df['open']).rolling(window=length).mean()
    den = swma(_df['high'] - _df['low']).rolling(window=length).mean()
    _df['RVI'] = (num / den)
    _df['SIG'] = swma(_df['RVI'])
    
    return _df[['RVI', 'SIG']]

def connors_rsi(df, lenrsi=3, lenupdown=2, lenroc=100):
    _df = df.copy()
    src = _df['close']
    _rsi = rsi(src, lenrsi)
    updown_rsi = rsi(updown(src), lenupdown)
    percentrank = percent_rank((100 * (src - src.shift(1)) / src.shift(1)), lenroc)
    _df['crsi'] = ((_rsi + updown_rsi + percentrank) / 3)
    
    return _df[['crsi']]

def rci(df, length=10, ma_length=14):
    _df = df.copy()
    rci = np.full_like(_df['close'], np.nan)
    idx = np.arange(length)
    close_values = _df['close'].to_numpy()
    
    for i in range(length - 1, len(close_values)):
        rci[i] = (1 - 6 * np.sum((idx - np.argsort(np.argsort(close_values[i - length + 1:i + 1]))) ** 2) / (length * (length**2 - 1))) * 100
    
    rci = pd.Series(rci)
    _df['rci'] = rci
    _df['rci_ma'] = sma(rci, length=ma_length)

    return _df[['rci', 'rci_ma']]

def coppock_curve(df, wma_length=10, long_roc_length=14, short_roc_length=11):
    _df = df.copy()
    long_roc = rate_of_change(df, len=long_roc_length)
    short_roc = rate_of_change(df, len=short_roc_length)
    curve = wma(long_roc + short_roc, length=wma_length)
    _df['coppock_curve'] = curve

    return _df[['coppock_curve']]

def smi(df, lengthK=10, lengthD=3, lengthEMA=3):
    _df = df.copy()
    highest_high = _df['high'].rolling(lengthK).max()
    lowest_low = _df['low'].rolling(lengthK).min()
    mid_range = (highest_high + lowest_low) / 2
    range_diff = highest_high - lowest_low
    
    smi = 200 * (ema(ema(_df['close'] - mid_range, lengthD), lengthD) /
                 ema(ema(range_diff, lengthD), lengthD))
    
    _df['smi'] = smi
    _df['smi_ema'] = ema(smi, lengthEMA)
    
    return _df[['smi', 'smi_ema']]

def chop(df, length=14):
    _df = df.copy()
    atr_sum = _df['high'].sub(_df['low']).rolling(window=length).sum()
    high_max = _df['high'].rolling(window=length).max()
    low_min = _df['low'].rolling(window=length).min()
    
    ci = 100 * np.log10(atr_sum / (high_max - low_min)) / np.log10(length)
    _df['chop'] = ci.round(2)
    
    return _df[['chop']]