import time
import pyupbit
import datetime

access = "your-access"
secret = "your-secret"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma(ticker, days):
   def get_ma(ticker, days):
    """이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=days)
    ma = df['close'].rolling(days).mean().iloc[-1]
    return ma

# ...

def main():
    # ...

    while True:
        try:
            now = datetime.datetime.now()
            start_time = get_start_time("KRW-BTC")
            end_time = start_time + datetime.timedelta(days=1)

            if start_time < now < end_time - datetime.timedelta(seconds=10):
                ma_20 = get_ma("KRW-BTC", 20)
                ma_50 = get_ma("KRW-BTC", 50)
                ma_120 = get_ma("KRW-BTC", 120)
                current_price = get_current_price("KRW-BTC")
                
                if current_price > ma_20 and current_price > ma_50 and current_price > ma_120:
                    krw = get_balance("KRW")
                    if krw > 5000:
                        upbit.buy_market_order("KRW-BTC", krw*0.9995)
                elif current_price < ma_20 and current_price < ma_50 and current_price < ma_120:
                    btc = get_balance("BTC")
                    if btc > 0.00008:
                        upbit.sell_market_order("KRW-BTC", btc*0.9995)
            else:
                btc = get_balance("BTC")
                if btc > 0.00008:
                    upbit.sell_market_order("KRW-BTC", btc*0.9995)
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)
def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

def ma_crossed(df, ma_short=20, ma_mid=50):
    """이동평균선(MA)이 교차하는 지점 확인"""
    ma_short_series = df['close'].rolling(ma_short).mean()
    ma_mid_series = df['close'].rolling(ma_mid).mean()
    return (ma_short_series.shift(1) < ma_mid_series.shift(1)) & (ma_short_series > ma_mid_series)
    
# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        df = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=50)
        ma_cross = ma_crossed(df)
        
        if ma_cross.iloc[-1]:
            btc = get_balance("BTC")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
        else:
            target_price = get_target_price("KRW-BTC", 0.5)
            ma20 = get_ma("KRW-BTC", 20)
            ma50 = get_ma("KRW-BTC", 50)
            ma120 = get_ma("KRW-BTC", 120)
            current_price = get_current_price("KRW-BTC")
            if current_price > target_price and current_price > ma20 and current_price > ma50 and current_price > ma120:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
