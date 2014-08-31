import sys
 
import redis
from willie.module import commands
 
rcache = redis.Redis(host="127.0.0.1", port="6379")
 
@commands("learn")
def learn(bot, trigger):
  tmp = trigger.group(2)
  tmp = tmp.split()
  command = tmp[0]
  key = tmp[1]
  if command == "add":
    value = ' '.join(tmp[2:])
    rcache.set(key, value)
    bot.say("Learnt that shit son> '%s': %s" % (key, value))
  elif command == "del":
    rcache.delete(key)
    bot.say("Removed that bitch ass shit> '%s'" % key)
  elif command == "find":
    found = [k for k in rcache.keys() if key in k]
    if len(found) > 0:
      bot.say("Found the following matches: %s" % ", ".join(found))
    else:
      bot.say("No matches found for %s" % key)
  else:
    bot.say("Use .learn [add|del] key <value>")
 
@commands(".")
def get(bot, trigger):
  key = trigger.group(2)
  if len(key.split()) > 1:
    learn(bot, trigger)
  else:
    if not rcache.exists(key):
      bot.say("Could not find '%s'" % key)
    else:
      bot.say("%s: %s" % (key, rcache.get(key)))
