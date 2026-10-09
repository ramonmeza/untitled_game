from .app import App
from .game import Game
from .raylib import RaylibRenderer, RaylibWindow


app: App = App(RaylibWindow(), RaylibRenderer(), Game())
app.run()
