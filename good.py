import time
import pyupbit
import datetime

access = "your- access"
secret = "your- secret"

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

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_ma50(ticker):
    """50일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=50)
    ma50 = df['close'].rolling(50).mean().iloc[-1]
    return ma50

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
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.5)
            ma15 = get_ma15("KRW-BTC")
            ma50 = get_ma50("KRW-BTC")
            current_price = get_current_price("KRW-BTC")
            if current_price > target_price and current_price > ma15:
                krw = get_balance("KRW")
                if krw > 5000:
                    buy_price = min(current_price, target_price)  # Adjusted buy price
                    upbit.buy_market_order("KRW-BTC", krw * 0.9995, price=buy_price)  # Specify buy price
                    bought_price = buy_price  # Store the bought price for trailing stop loss
            elif current_price < bought_price * 0.95:  # Implement trailing stop loss at 5%
                btc = get_balance("BTC")
                if btc > 0:
                    sell_price = get_current_price("KRW-BTC")  # Adjusted sell price
                    upbit.sell_market_order("KRW-BTC", btc * 0.9995, price=sell_price)  # Specify sell price
        else:
            btc = get_balance("BTC")
            if btc > 0:
                ma50 = get_ma50("KRW-BTC")  # Get ma50 value
                if current_price <= ma50:  # Sell all assets if price is below ma50
                    sell_price = get_current_price("KRW-BTC")  # Adjusted sell price
                    upbit.sell_market_order("KRW-BTC", btc * 0.9995, price=sell_price)  # Specify sell price
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
