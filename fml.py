__author__ = "klaplante"

import urllib2
from willie.module import commands

def get():
  rscript_fml = urllib2.urlopen("http://rscript.org/lookup.php?type=fml")
  fml = rscript_fml.read()
  for line in fml.splitlines():
    if line.startswith("ID:"):
      fml_id = line.split(":")[1].strip()
    if line.startswith("TEXT:"):
      fml_text = line.split(":")[1].strip()
  return fml_id, fml_text

@commands("fml")
def fml(bot, trigger):
  fml_id, fml_text = get()
  bot.reply("[FML#%s] %s" %(fml_id, fml_text))
