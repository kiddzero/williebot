import willie
from willie.module import commands
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': './next_data',
    'cache.lock_dir': './next_lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))
tcache = cache.get_cache("learn", type='dbm')

@commands("next")
def next(bot, trigger):
  tmp = trigger.group(2).split()
  person = tmp[0]
  msg = ' '.join(tmp[1:])
  key = "__%s" % person
  tcache.put(key, msg)
  bot.say("Next'd %s: %s" % (person, msg))

def join_msg(bot, trigger):
  key = "__%s" % trigger.nick
  if tcache.has_key(key):
    bot.reply(tcache.get(key))
    tcache.remove(key)

join_msg.event = "JOIN"
join_msg.rule = r'.*'
