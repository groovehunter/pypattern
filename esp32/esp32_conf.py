
# esp32 pins:
# physically, on the sheet, TOP to DOWN:
# L: 32, 33, 25, 26, 27, 14, 12, 13
# R: 21, 19, 18,  5, 23, 22,  4,  2


# From bottom (usb port) left, wie use these GPIO pins clockwise:
# Four pins together is a quart (q)

# left side upwards
q1 = [13, 12, 14, 27]

q2a = [26, 25]
q2b = [33, 32]
q2 = q2a + q2b

# right side upwards
q3a = [2, 4]
q3b = [16, 17]  # RxTx ports but can use it for digi changes
q3 = q3a + q3b
#
q4a = [5, 18]
q4b = [19, 21]

# These pins at upper right version on orig boards are redirected  to the place where 16+17 are.
qq = [22, 23]

def make_pinmap(*groups):
    """Erzeugt ein {index: gpio}-Dict aus beliebigen Gruppen."""
    pins = []
    for group in groups:
        pins.extend(group)
    return {i+1: pin for i, pin in enumerate(pins)}

# Beispiele für verschiedene Pinmaps:
pinmap = {
    'hexagon_qq': make_pinmap(q1, q2, q3a, qq),
    'hexagon_rxtx': make_pinmap(q1, q2, q3a, q3b),
    'hexagon_single': make_pinmap(q1, q2a),
    #'hexagon_single': make_pinmap(q3a, q3b, q4a),
    #'hexagon_full': make_pinmap(q1, q2, q3a, q3b, q4a, q4b, qq),
    #'test': make_pinmap(q1, q2, q3a, qq),
    # beliebige weitere Kombinationen möglich
}
