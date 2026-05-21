from lib.LightPattern import LightPattern

class AlternatingGroups(LightPattern):
    """
    A pattern that toggles between two predefined light groups, 'A' and 'B'.
    These groups are defined in the board's geometry.
    """
    render_mode = 'group' # This pattern uses group-based rendering.

    def __init__(self, board, **kwargs):
        super().__init__(board)
        # kwargs werden ignoriert, aber akzeptiert

    def initialize(self):
        """Starts with group A on and B off."""
        self.count = 0
        self.next_state()

    def next_state(self):
        """Toggles the state between group A and group B."""
        self.count = (self.count + 1) % 2

        # The actual rendering is handled by GenericGeometry's `enlighten_group` method.
        # This pattern only needs to set its internal state.
        # We can use the `count` for this: 0 for Group A, 1 for Group B.

