#!/usr/bin/env python3
import json
import urllib.request
import sys
import os
from datetime import date, timedelta, datetime
from dateutil import parser
from time import strftime

dir = os.path.dirname(os.path.abspath(__file__))

with open(dir + '/players.json', 'r') as file:
  data = json.load(file)['league']['standard']
  players = {}
  for p in data:
    players[p['personId']] = p['firstName'] + ' ' + p['lastName'] 

with open(dir + '/teams.json', 'r') as file:
  data = json.load(file)['league']['standard']
  teams = {}
  for t in data:
    teams[t['teamId']] = t['fullName']

class Team(object):
  def __init__(self, obj):
    self.tri = obj['triCode']
    self.score = obj['score']
    self.win_loss = obj['win'] + '-' + obj['loss']
    self.teamId = obj['teamId']

class Game(object):
  def __init__(self, obj):
    self.h = Team(obj['hTeam'])
    self.v = Team(obj['vTeam'])
    self.period = self.format_period(obj['period'])
    self.clock = self.format_clock(obj['clock'])
    self.nugget = obj['nugget']['text']
    self.arena = obj['arena']['name']
    self.id = obj['gameId']
    self.start = self.format_time(obj['startTimeUTC'])
    self.date = self.game_date(obj['startTimeUTC'])
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
  
  def game_date(self, time):
    t = parser.parse(time) + timedelta(hours=-5) 
    return t.strftime("%Y%m%d")
  
  def format_time(self, time):
    t = parser.parse(time) + timedelta(hours=TIME_AHEAD) 
    return t.strftime("%a %I:%M %p")

  def get_boxscore(self):
    url = f'http://data.nba.net/10s/prod/v1/{self.date}/{self.id}_boxscore.json'
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
    players = data['stats']['activePlayers']
    return players

  def print_boxscore(self):
    WIDTH = 117
    if not self.box:
      self.box = self.get_boxscore
    print("-" * WIDTH)
    print(f"{teams[self.v.teamId]:^117}")
    print("-" * WIDTH)
    print(f"{'Name':^25} | {'Min':^5} | {'FG':^5} | {'3P':^5} | {'FT':^5} | OREB | DREB | REB | AST | STL | BLK | TO | PF | +/- | PTS ")
    print("-" * WIDTH)
    for p in self.box:
      if p['teamId'] == self.v.teamId:
        print(f"{players[p['personId']]:<25} | {p['min']:>5} | {p['fgm']:>2}/{p['fga']:<2} | {p['tpm']:>2}/{p['tpa']:<2} | {p['ftm']:>2}/{p['fta']:<2} | "
        f"{p['offReb']:>4} | {p['defReb']:>4} | {p['totReb']:>3} | {p['assists']:>3} | {p['steals']:>3} | {p['blocks']:>3} | {p['turnovers']:>2} | "
        f"{p['pFouls']:>2} | {p['plusMinus']:>3} | {p['points']:>3}")
    print("-" * WIDTH)
    print(f"{teams[self.h.teamId]:^117}")
    print("-" * WIDTH)
    print(f"{'Name':^25} | {'Min':^5} | {'FG':^5} | {'3P':^5} | {'FT':^5} | OREB | DREB | REB | AST | STL | BLK | TO | PF | +/- | PTS ")
    print("-" * WIDTH)
    for p in self.box:
      if p['teamId'] == self.h.teamId:
        print(f"{players[p['personId']]:<25} | {p['min']:>5} | {p['fgm']:>2}/{p['fga']:<2} | {p['tpm']:>2}/{p['tpa']:<2} | {p['ftm']:>2}/{p['fta']:<2} | "
        f"{p['offReb']:>4} | {p['defReb']:>4} | {p['totReb']:>3} | {p['assists']:>3} | {p['steals']:>3} | {p['blocks']:>3} | {p['turnovers']:>2} | "
        f"{p['pFouls']:>2} | {p['plusMinus']:>3} | {p['points']:>3}")
    
  
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
  
def print_scores(games):
  for i, g in enumerate(games, 1):
    print()
    print(f'GAME {i}')
    print(g)

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

print_scores(games)

for g in games:
  try:
    g.box = g.get_boxscore()
  except:
    pass


while True:
  print()
  print('Enter a game number to see the box score or "s" to see the scores again, or q to quit')
  action = str(input(' > '))
  if action == 's':
    print_scores(games)
  elif action == 'q':
    sys.exit()
  else:
    try:
      action = int(action)
      games[action-1].print_boxscore()
    except:
      print('Invalid selection.')
