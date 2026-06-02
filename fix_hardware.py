import json
def chunk_list(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]
hardware = {
    "layouts": {
        "square": {
            "leds_per_panel": 4,
            "panels": chunk_list([13, 12, 14, 27, 26, 25, 33, 32, 2, 4, 16, 17, 5, 18, 19, 21], 4)
        },
        "triangle": {
            "leds_per_panel": 4,
            "panels": chunk_list([13, 12, 14, 27, 26, 25, 33, 32, 2, 4, 16, 17], 4)
        },
        "default": {
            "leds_per_panel": 4,
            "panels": chunk_list([13, 12, 14, 27, 26, 25, 33, 32, 2, 4, 16, 17, 5, 18, 19, 21], 4)
        },
        "hexagon_qq": {
            "leds_per_panel": 2,
            "panels": chunk_list([13, 12, 14, 27, 26, 25, 33, 32, 2, 4, 22, 23], 2)
        },
        "hexagon_rxtx": {
            "leds_per_panel": 2,
            "panels": chunk_list([13, 12, 14, 27, 26, 25, 33, 32, 2, 4, 16, 17], 2)
        },
        "hexagon_single": {
            "leds_per_panel": 1,
            "panels": chunk_list([13, 12, 14, 27, 26, 25], 1)
        },
        "hexagon_full": {
            "leds_per_panel": 3,
            "panels": chunk_list([13, 12, 14, 27, 26, 25, 33, 32, 2, 4, 16, 17, 5, 18, 19, 21, 22, 23], 3)
        }
    }
}
# we need a custom encoder to format panels on a single line
class SingleLinePanelsEncoder(json.JSONEncoder):
    def iterencode(self, o, _one_shot=False):
        yield "{\n    \"layouts\": {\n"
        layouts = list(o["layouts"].items())
        for i, (name, config) in enumerate(layouts):
            yield f'        "{name}": {{\n'
            yield f'            "leds_per_panel": {config["leds_per_panel"]},\n'
            yield '            "panels": [\n'
            panels = config["panels"]
            for j, p in enumerate(panels):
                yield '                ' + json.dumps(p)
                if j < len(panels) - 1:
                    yield ',\n'
                else:
                    yield '\n'
            yield '            ]\n'
            yield '        }'
            if i < len(layouts) - 1:
                yield ',\n'
            else:
                yield '\n'
        yield '    }\n}'
with open("hardware.json", "w") as f:
    for chunk in SingleLinePanelsEncoder().iterencode(hardware):
        f.write(chunk)
