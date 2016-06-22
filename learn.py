import sys

import redis
import sopel

rcache = redis.Redis(host="127.0.0.1", port="6379")

@sopel.module.commands("learn2")
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
      try:
        # its a string
        existing = rcache.get(key)
        new = [existing, str_value]
        rcache.delete(key)
        try:
          rcache.lpush(key, *new)
          bot.say("Learnt that shit son> '%s': %s" % (key, str_value))
        except redis.ResponseError:
          bot.say("Error trying to write {0} to key {1}".format(new, key))
          rcache.set(key, existing)
      except redis.ResponseError:
        # its a list
        try:
          rcache.lpush(key, str_value)
          bot.say("Learnt that shit son> '%s': %s" % (key, str_value))
        except redis.ResponseError:
          bot.say("Error trying to write {0} to key {1}".format(str_value, key))
    else:
      rcache.lpush(key, str_value)
      bot.say("Learnt that shit son> '%s': %s" % (key, str_value))
  elif command == "del":
    if len(tmp) == 2:
      rcache.delete(key)
      bot.say("Removed that bitch ass shit> '%s'" % key)
    elif len(tmp) == 3:
      index = tmp[2]
      current = rcache.lrange(key, 0, -1)
      try:
        # items are displayed in reverse for cronological ordering
        index_to_remove = len(current) - 1 - int(index)
        to_remove = current[index_to_remove]
        rcache.lrem(key, to_remove)
        bot.say("Removed the shit from the ass> dookie #%s" % index)
      except Exception as e:
        bot.say(str(e))
  elif command == "find":
    found = [k for k in rcache.keys() if key in k]
    if len(found) > 0:
      bot.say("Found the following matches: %s" % ", ".join(found))
    else:
      bot.say("No matches found for %s" % key)
  else:
    bot.say("Use .learn [add|del] key <value>")

@sopel.module.commands("\.\.")
def get(bot, trigger):
  key = trigger.group(2)
  if len(key.split()) > 1:
    learn(bot, trigger)
  else:
    if not rcache.exists(key):
      bot.say("Could not find '%s'" % key)
    else:
      try:
        value = rcache.get(key)
        bot.say("%s: %s" % (key, value))
      except redis.ResponseError:
        value = rcache.lrange(key, 0, -1)
        for i, v in enumerate(value[::-1]):
          bot.say("{0}: {1}".format(i, v))
