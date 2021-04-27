from cryptofeed import FeedHandler
from cryptofeed.exchanges import HITBTC,HitBTC
from cryptofeed.callback import BookUpdateCallback, BookCallback
from cryptofeed.feed import L2_BOOK

# not all imports shown for clarity

fh = FeedHandler()
def call(mes):
    print(mes)
# ticker, trade, and book are user defined functions that
# will be called when ticker, trade and book updates are received
# ticker_cb = {TICKER: TickerCallback(ticker)}
# trade_cb = {TRADES: TradeCallback(trade)}
#binance_cb = { L2_BOOK: BookCallback(book)}
#

fh.add_feed(HitBTC(symbols=['BTC-USD'], channels=[L2_BOOK], callbacks={L2_BOOK:call}))

fh.run()