from LightPattern import LightPattern

"""
### symmetry : FIXED AS A RAUTE in the view!!!
"""

class SymmetryPattern(LightPattern):
  """ all states keep symmetry """
  pass

class X_SymmetryPattern(SymmetryPattern):
  pass

class SymNegativPattern(LightPattern):
  """ sym.opposite lights are negation """
  pass

class XaxisNegativPattern(SymNegativPattern):
  """ upper half lights are negated lights of lower half """
  def subclass_init(self):
    # make pairs of lights?
    pass

class XaxisNegativAllPattern(XaxisNegativPattern):
  states_count = 2
  def next_state(self):
    pass

class UpperLowerSwitching(X_SymmetryPattern):
  def next_state(self):
    pass
