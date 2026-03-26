import pyxel

def update():
    pass

def draw():
    pyxel.cls(0)
    pyxel.text(60, 40, "Formula 26", 8)
    pyxel.text(40, 50, "A Speed Manager Game", 6)

pyxel.init(160, 120, title="Formula26")
pyxel.run(update, draw)
