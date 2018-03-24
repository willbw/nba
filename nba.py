#!/usr/bin/env python3
import json
import urllib.request
import sys
from datetime import date, timedelta, datetime
from dateutil import parser
from time import strftime

class Team(object):
  tri = ''
  score = 0
  win_loss = ''

  def __init__(self, obj):
    self.tri = obj['triCode']
    self.score = obj['score']
    self.win_loss = obj['win'] + '-' + obj['loss']

class Game(object):
  def __init__(self, obj):
    self.h = Team(obj['hTeam'])
    self.v = Team(obj['vTeam'])
    self.period = self.format_period(obj['period'])
    self.clock = self.format_clock(obj['clock'])
    self.nugget = obj['nugget']['text']
    self.arena = obj['arena']['name']
    self.gameId = obj['gameId']
    self.start = self.format_time(obj['startTimeUTC'])
    self.data = obj


  def format_period(self, period):
    q = period['current']
    if q == 0:
      return ''
    else:
      return f'Q{q}'
  
  def format_clock(self, clock):
    if not clock:
      return '00:00'
    if ':' in clock:
      if len(clock) == 5:
        return clock
      else:
        return '0' + clock
    else:
      return clock + 's'
  
  def format_time(self, time):
    t = parser.parse(time) + timedelta(hours=TIME_AHEAD) 
    return t.strftime("%a %I:%M %p")
  
  def __str__(self):
    s = '{:5}{:4}-{:>4}{:>5}'.format(self.h.tri, self.h.score, self.v.score, self.v.tri)
    if self.data['isGameActivated']:
      s += '{:>5}{:>6}'.format(self.period, self.clock)
    elif not self.period:
      s += '   ' + self.start
    else:
      s += '   FINAL'
    s += '\n{:<9} {:>9}'.format(self.h.win_loss, self.v.win_loss)
    s += '   ' + self.nugget
    return s

    
#  print_game(self):
#   print('\n{:5}{:4}-{:>4}{:>5}'
#   .format(g.h.tri, g.h.score, g.v.score, g.v.tri), end='')
#   if g.period:
#     print('{:>5}{:>6}'.format(g.period, g.clock), end = '')
#   else:
#     print('   ' + g.start, end = '')
#   print('\n{:<9} {:>9}'.format(g.h.win_loss, g.v.win_loss))

# def main():
adj = 0
TIME_AHEAD = 11
if len(sys.argv) > 1: 
  try:
    adj = int(sys.argv[1])
  except ValueError:
    print("usage: nba [n]")
    print("where n is the optional number of days you wish to go back")
    sys.exit()

day = date.today() - timedelta(1) + timedelta(adj)
d = '{:%Y%m%d}'.format(day)

url = f'http://data.nba.net/10s/prod/v1/{d}/scoreboard.json'
with urllib.request.urlopen(url) as response:
    data = json.load(response)

print(f'Game day: {day}')

games = [Game(g) for g in data['games']] 

for g in games:
  print()
  print(g)

# if __name__ == '__main__':
#   main()