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
        for y in range(1, 9):
            for x in range(1, 9):
                letter = chr(96 + x)  # Convert column index to letter (a-h)
                tile = self.createTile(letter, y)
                layout.add_widget(tile)

        self.boardSetup()
        self.resetColors(layout)
        
        # Reverse the order of tiles in layout to match board orientation
        for space, tile in zip(chess.SQUARES[::-1], self.ids['playArea'].children):
            piece = self.board.piece_at(space)
            if piece:
                tile.text = str(piece)
        
    def createTile(self, letter, number):
        tile = Button()
        tile.coords = (letter, number)
        tile.bind(on_press=lambda instance: self.onTileSelect(tile.coords))
        return tile
    
    tileColors = [(0.94, 0.85, 0.71, 1), # Light Brown
                  (0.71, 0.53, 0.39, 1)] # Dark Brown
        
    def resetColors(self, layout):
        iterator = 1
        tiles = layout.children
        for x in range(8):
            iterator += 1
            for y in range(8):
                tiles[(x * 8) + y].background_color = self.tileColors[iterator % 2]
                iterator += 1

    def onTileSelect(self, coords):
        print(f"Selected coords: {coords}")
        try:
            # Convert coords (letter, number) to chess square notation
            square = chess.parse_square(f"{coords[0].lower()}{coords[1]}")
            print(f"Parsed square: {square}")
        except ValueError:
            print(f"Invalid chess square: {coords}")
            return

        # Check if a piece is at the square and show legal moves
        piece = self.board.piece_at(square)
        if piece:
            print(f"Piece at {coords}: {piece}")
            piece_moves = [move for move in self.board.legal_moves if move.from_square == square]
            for move in piece_moves:
                print(move.uci())
        else:
            print(f"No piece at {coords}.")
    
    def boardSetup(self):
        self.board = chess.Board()
        print("Initial board setup:")
        print(self.board)

class Main(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='MenuScreen'))
        sm.add_widget(GameScreen(name='GameScreen'))
        
        return sm
    
if __name__ == '__main__':
    Main().run()
