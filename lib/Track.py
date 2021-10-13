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
}

# rename to TrackSupport
class Track:
  """ a sequential notation for running pattern in a rows
  """
  def __init__(self):
    #self.current = 1
    self.init()

  def init(self):
    self.load_tracks()
    track = self.tracks[0]
    self.parse(track)

  def load_tracks(self):
    self.tracks = {}
    fn = ROOT_DIR+'/tracks/tr1.txt'
    with open(fn, 'r') as f:
      self.tracks = [line.rstrip() for line in f]
#        if line.startswith(' '): continue
#        self.tracks[c] = line

#  def reset(self):  pass

  def next_pattern(self):
    #self.current += 1
    if self.pats == {}:   # track "ended", reset it
      #self.init()
      self.pats = self.track_pats.copy()
      print("TRACK resetted", self.pats)
    pat_item = self.pats.popitem()
    pat_abbr = pat_item[0]
    repeats = pat_item[1]
    print()
    print(pat_map[pat_abbr], "playing times: ", repeats)
    self.cur_pat = pat_abbr
    self.cur_repeats = repeats
    return pat_map[pat_abbr]

  def parse(self, track):
    tmp = track.split(' - ')[1]
    track_pats = {}
    pat_list = tmp.split(" ")
    for pat in pat_list:
      name, times = pat.split(":")
      track_pats[name] = times
    self.track_pats = track_pats
    print(self.track_pats)
    self.pats = self.track_pats.copy()

  def get_current_repeats(self):
    print(self.pats)
    return int(self.cur_repeats)
