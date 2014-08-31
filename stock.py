import ystockquote
from willie.module import commands

@commands('stock')
def stock(bot, trigger):
  if not trigger.group(2):
    bot.reply("Please enter a stock ticker. Ex. TWTR")
  else:
    ticker = trigger.group(2).upper()
    s = ystockquote.get_all(ticker)
    bot.reply("%s %s, Price: $%s, Change: %s, Volume: %s, 52 Week High: $%s. " % (ticker, s['stock_exchange'], s['price'], s['change'], s['volume'], s['52_week_high']))

