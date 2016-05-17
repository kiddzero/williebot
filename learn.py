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
    str_value = ' '.join(tmp[2:])
    # if the key already exists determine if its already a list,
    # if it is not a list then make a list of the existing value + the new value
    # if it is already a list simply add the new value to the list.
    # if the key does not exist make the value a list of the string value
    if rcache.exists(key):
      existing = rcache.get(key)
      if not isinstance(existing, list):
        rcache.set(key, [existing, str_value])
      else:
        rcache.lpush(key, str_value)
    else:
      rcache.set(key, [str_value])
    bot.say("Learnt that shit son> '%s': %s" % (key, str_value))
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
      value = rcache.get(key)
      if isinstance(value, list):
        for v in value:
          bot.say(v)
      else:
        bot.say("%s: %s" % (key, value))
