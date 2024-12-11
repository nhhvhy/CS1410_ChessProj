import chess

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('KVchess.kv')

class MenuScreen(Screen):
    pass

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        layout = self.ids.get('playArea', GridLayout)
        
        # Messy loop because colors must alternate between rows
        color_incr = 1
        for x in range(8):
            letter = chr(97 + x)
            color_incr += 1
            for y in range(8):
                tile = self.createTile(color_incr % 2, letter, y)
                color_incr += 1
                layout.add_widget(tile)
        
        self.boardSetup()
        for space, tile in zip(chess.SQUARES, self.ids['playArea'].children):
            piece = self.board.piece_at(space)
            if piece:
                tile.text = str(piece)
        
        # Use this to display tile position values instead of symbols
        ''' testIter = 0
            for item in self.ids['playArea'].children:
                item.text = str(testIter)
                testIter += 1 '''
                
    tileColors = [(0.94, 0.85, 0.71, 1), # Light Brown
                  (0.71, 0.53, 0.39, 1)] # Dark Brown
        
    def createTile(self, color, x, y):
        tile = self.ids.get('Tile', Button)(background_color = self.tileColors[color])
        tile.id = (x, y)
        tile.bind(on_press=lambda instance: self.onTileSelect(tile.id))
        return tile

    def onTileSelect(self, coords):
        print(coords)
    
    # Used to reset board to starting position
    def boardSetup(self):
        self.board = chess.Board()
        print(self.board)


class Main(App):
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='MenuScreen'))
        sm.add_widget(GameScreen(name='GameScreen'))
        
        return sm
    
if __name__ == '__main__':
    Main().run()