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
    'CMB': 'ComboPattern',

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

        # reset any previous kwargs
        try:
            self.last_pattern_kwargs = None
        except Exception:
            pass

        # Support a simple inline ComboPattern syntax: after the first three fields
        # the remainder is a combo spec where subpatterns are separated by '|'
        # and optional kwargs follow a ':' with comma-separated key=val pairs.
        # Example: "CMB 1 120 Chase:length=4|RotationPanelPattern"
        combo_spec = None
        if pat_abbr in ('CMB', 'COMBO') and len(pat_items) > 3:
            combo_spec = " ".join(pat_items[3:]).strip()

        self.cur_pat = pat_abbr
        self.cur_repeats = repeats

        if combo_spec:
            # parse combo_spec into pattern_configs
            configs = []
            parts = combo_spec.split('|')
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                if ':' in part:
                    pname, kvals = part.split(':', 1)
                    kwargs = {}
                    for kv in kvals.split(','):
                        if '=' in kv:
                            k, v = kv.split('=', 1)
                            k = k.strip()
                            v = v.strip()
                            # try to convert numeric values
                            if v.isdigit():
                                v = int(v)
                            else:
                                try:
                                    fv = float(v)
                                    v = fv
                                except Exception:
                                    pass
                            kwargs[k] = v
                    configs.append((pname.strip(), kwargs))
                else:
                    configs.append((part, {}))
            # store last pattern kwargs for the caller (pdc_desktop) to pick up
            try:
                self.last_pattern_kwargs = {'pattern_configs': configs, 'ticks_to_switch': repeats}
            except Exception:
                self.last_pattern_kwargs = None
            return pat_map.get(pat_abbr, pat_abbr)

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
