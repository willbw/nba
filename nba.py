#!/usr/bin/env python3
import json
import urllib.request
import sys
from datetime import date, timedelta

class Team(object):
  tri = ''
  score = 0
  win_loss = ''

  def __init__(self, obj):
    self.tri = obj['triCode']
    self.score = obj['score']
    self.win_loss = obj['win'] + '-' + obj['loss']

adj = 0
if len(sys.argv) > 1: 
  try:
    adj = abs(int(sys.argv[1]))
  except ValueError:
    print("usage: nba [n]")
    print("where n is the optional number of days you wish to go back")
    sys.exit()

day = date.today() - timedelta(1 + adj)
d = '{:%Y%m%d}'.format(day)

url = f'http://data.nba.net/10s/prod/v1/{d}/scoreboard.json'
with urllib.request.urlopen(url) as response:
    data = json.load(response)

print(f'Game day: {day}')

for g in data['games']:
  txt = g['nugget']['text']
  vTeam, hTeam = Team(g['vTeam']), Team(g['hTeam'])
  print('\n{} {:3} - {:>3} {} {}'.format(
        hTeam.tri, hTeam.score, vTeam.score, vTeam.tri, txt))
  print('{:<8} {:>8}'.format(hTeam.win_loss, vTeam.win_loss))
