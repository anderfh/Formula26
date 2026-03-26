import pyxel

class app:
    def __init__(self):
        pyxel.init(160, 120, title="Formula26")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(7)
        pyxel.text(50, 50, "Formula 26", 8)
        pyxel.text(50, 60, "A speed manager game", 6)

app()

