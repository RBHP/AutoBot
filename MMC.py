import time
import pyupbit
import datetime

access = "your-access-key"
secret = "your-secret-key"

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

def get_macd(ticker, interval):
    """MACD 지표 계산"""
    df = pyupbit.get_ohlcv(ticker, interval=interval)
    close = df['close']
    macd, macdsignal, macdhist = talib.MACD(close)
    return macd, macdsignal, macdhist

def get_ma50(ticker, interval):
    """MA50 일선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval=interval)
    ma50 = df['close'].rolling(window=50).mean()
    return ma50.iloc[-1]

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

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1)
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            ticker = "KRW-BTC"
            macd, macdsignal, macdhist = get_macd(ticker, interval="minute15")
            ma50 = get_ma50(ticker, interval="day")
            current_price = get_current_price(ticker)

            if macdhist[-1] > 0 and macdhist[-2] < 0 and macd[-1] > 0:
                # 0선 상향돌파 시 매수
                cross_diff = macd[-2] - macdsignal[-2]
                if cross_diff > 4 and cross_diff < 6.5:
                    krw = upbit.get_balance("KRW")
                    if krw > 5000:
                        upbit.buy_market_order(ticker, krw * 0.9995, leverage=20)

            elif macdhist[-1] < 0 and macdhist[-2] > 0 and macd[-1] < 0:
                # 0선 하향돌파 시 매도
                cross_diff = macd[-2] - macdsignal[-2]
                if cross_diff > 4 and cross_diff < 6.5:
                    btc = upbit.get_balance(ticker.split('-')[1])
                    if btc > 0:
                        upbit.sell_market_order(ticker, btc * 0.9995, leverage=20)

        else:
            ticker = "KRW-BTC"
            ma50 = get_ma50(ticker, interval="day")
            current_price = get_current_price(ticker)
            if current_price < ma50:
                btc = upbit.get_balance(ticker.split('-')[1])
                if btc > 0:
                    upbit.sell_market_order(ticker, btc * 0.9995, leverage=20)

        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)