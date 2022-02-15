import ccxt, math, statistics

def yang_zhang(candles):
    normalized_open = []
    normalized_high = []
    normalized_down = []
    normalized_close = []
    rogers_satchell = []

    #Calculating normalized values
    for x in range(1,len(candles)):
        normalized_open.append(math.log(candles[x][1]/candles[x-1][4]))
        normalized_high.append(math.log(candles[x][2]/candles[x][1]))
        normalized_down.append(math.log(candles[x][3]/candles[x][1]))
        normalized_close.append(math.log(candles[x][4]/candles[x][1]))
        rogers_satchell.append(normalized_high[x-1]*(normalized_high[x-1]-normalized_close[x-1])+normalized_down[x-1]*(normalized_down[x-1]-normalized_close[x-1]))

    #Calculating volatilities
    rs_volatility = math.sqrt(sum(rogers_satchell)/(len(rogers_satchell)))
    no_volatility = statistics.stdev(normalized_open)
    nc_volatility = statistics.stdev(normalized_close)

    #Calculate constant k
    k = 0.34/(1.34+((len(candles)+1)/(len(candles)-1)))

    return math.sqrt(no_volatility**2+k*nc_volatility**2+(1-k)*rs_volatility**2)

if __name__=="__main__":
    symbol="FTM/USDT"
    samples = 288       #The amount of samples to take into account.

    exchange_id = "binance"                           
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({     
        "apiKey": "",
        "secret": "",
        "timeout": 30000,
        "enableRateLimit": True,
    })

    candles = exchange.fetch_ohlcv(symbol,timeframe="5m",limit=samples)
    print(str(round(yang_zhang(candles)*100,2))+"%")