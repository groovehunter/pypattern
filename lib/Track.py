"""
also pattern xy eine weile lang hintereinander, zb in vierertakten
bzw in vielfachen von zwei -
2 x P1
4 x P2
4 x P5
2 x P8
Finale.

ein current counter
sollder track object selber mitzählen?? Oder macht das run function?
"""
import os
import logging
from settings import ROOT_DIR
pat_map = {
'SLC': 'SingleLightCycling',
'RPP': 'RotationPanelPattern',
'PLC': 'PairedLightsCycling',
'RPP': 'RotationPanelPattern',
'DPP': 'DarkPanelRotationPanelPattern',
'WM' : 'Windmill',
'MES': 'MiddleEdgeSynchronousPattern',
'AOO': 'AllOnOffPattern',
'FFP': 'FiftyFiftyPattern',
'OPS': 'OppositePanelsSwitching',
'COPS': 'CyclingOppositePanelsSwitching',
'OPB': 'OppositePanelsBlinking',
'COPB':'CyclingOppositePanelsBlinking',

}
import csv
logger = logging.getLogger()

# rename to TrackSupport
class Track:
  """ a sequential notation for running pattern in a rows
  """
  def __init__(self):
    #self.current = 1
    self.init()

  def init(self):
    self.track_requested = False
    self.tid = 1
    self.speed = 111
    self.speed_tend = 0
    self.load_tracks(self.tid)
    self.current = 0

  def load_tracks(self, tid):
    self.tracks = {}
    fn = ROOT_DIR + '/tracks/tr'+str(tid)+'.csv'
    #fn = ROOT_DIR+'/tracks/tr1.txt'
    self.lines = {}
    lc = 0
    with open(fn, 'r') as f:
      self.reader = csv.reader(f, delimiter=' ')
      self.track = self.reader #[row for row in reader]
      for line in self.reader:
        self.lines[lc] = line
        logger.debug('line of csv: %s', str(line))
        lc +=1

      self.linescopy = self.lines.copy()
      #self.tracks = [line.rstrip() for line in f]
#        if line.startswith(' '): continue
#        self.tracks[c] = line
    self.tracks[0] = self.track

  def next_pattern(self):
    if self.linescopy == {}:   # track "ended", reset it
      self.linescopy = self.lines.copy()
      logger.debug("TRACK resetted, linescopy: %s", self.linescopy)
    if self.track_requested:
      logger.debug("starting NEW track: %d", self.tid)
      self.load_tracks(self.tid)
      self.track_requested = False

    self.current += 1
    if self.current >= len(self.linescopy):
      self.current = 0

    pat_item = self.linescopy[self.current]
    logger.debug('pat_item: %s', str(pat_item))
    pat_abbr = pat_item[0]
    repeats = int(pat_item[1])
    speed = pat_item[2]
    self.speed_tend = 0
    if '-' in speed:
      si1, si2 = speed.split('-')
      logger.debug('si1-si2 : %s-%s', si1, si2)
      s1, s2 = int(si1), int(si2)

      self.speed_tend = int(abs(s1-s2))
      if s1 > s2:
        self.speed_tend = -self.speed_tend
        self.speed = s1
      else:
        self.speed = s1
    else:
      self.speed = speed
    logger.debug("set speed %d", self.speed )
    logger.debug("set speed_tend %s", self.speed_tend )
    logger.debug("playing times: %d", repeats)
    self.cur_pat = pat_abbr
    self.cur_repeats = repeats
    return pat_map[pat_abbr]

  def get_current_speed(self):
    return int(self.speed)

  def get_speed_tend(self):
    return self.speed_tend

  def get_current_repeats(self):
    #logger.debug('self.pats', self.pats)
    return int(self.cur_repeats)

  def set_track(self, tid):
    self.tid = tid
    self.track = self.tracks[self.tid]
    self.track_requested = True
    return True
