import json
import requests
from willie.module import commands

@commands('urban')
def urban(bot, trigger):
  url = "http://urbanscraper.herokuapp.com/define/%s" % trigger.group(2)
  response = json.loads(requests.get(url).content)
  bot.say("%s: %s" % (response['term'], response['definition']))
  bot.say("url: %s" % response['url'])
