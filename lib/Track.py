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
from flowpy.simplelogger import SimpleLogger

logger = SimpleLogger(path=__name__+'.log', level='DEBUG')

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
#import csv

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
            lines = f.readlines()
            for line in lines:
                self.lines[lc] = line
                logger.debug('line of csv: %s', str(line))
                lc +=1

            self.linescopy = self.lines.copy()
            #self.tracks = [line.rstrip() for line in f]
#        if line.startswith(' '): continue
#        self.tracks[c] = line

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

        pat_items = self.linescopy[self.current].split(" ")
        #logger.debug('pat_items: %s', str(pat_items))
        #print(pat_items)
        pat_abbr = pat_items[0]
        repeats = int(pat_items[1])
        speed = pat_items[2]
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
