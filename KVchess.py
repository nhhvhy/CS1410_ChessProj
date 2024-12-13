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
        self.layout = self.ids.get('playArea', GridLayout)
        
        # Create the tiles with proper coordinates
        for y in range(1, 9):  # Row goes from 1 to 8 (bottom to top)
            for x in range(1, 9):  # Column goes from 1 to 8 (left to right)
                letter = chr(96 + x)  # Convert column index to letter (a-h)
                tile = self.createTile(letter, y)
                # Add the tile at the correct position
                self.layout.add_widget(tile)

        self.selected_piece = None

        self.boardSetup()
        self.resetColors()
        
        # Correct the placement of pieces in chess notation, row-by-row
        for space, tile in zip(chess.SQUARES[::-1], self.layout.children):
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
        
    def resetColors(self):
        iterator = 1
        tiles = self.layout.children
        for x in range(8):
            iterator += 1
            for y in range(8):
                tiles[(x * 8) + y].background_color = self.tileColors[iterator % 2]
                iterator += 1

    def onTileSelect(self, coords):
        square = chess.parse_square(f"{coords[0].lower()}{coords[1]}")

        # Clear highlighted tiles if the same piece is selected again
        if coords == self.selected_piece:
            self.resetColors()
            self.selected_piece = None
            return True
        self.selected_piece = coords

        # Check if a piece is at the square and show legal moves
        piece = self.board.piece_at(square)
        if piece:
            print(f"Piece at {coords}: {piece}")
            piece_moves = [move for move in self.board.legal_moves if move.from_square == square]
            for move in piece_moves:
                print(move)
                self.highlightTile(str(move)[2:])
        else:
            print('No piece here')

    def highlightTile(self, coords):
        tile = self.getTileByCoords(coords)
        tile.background_color = (0.6, 0.8, 0.6, 1)
    
    def getTileByCoords(self, coords):
        print((coords[0], int(coords[1])))
        for tile in self.layout.children:
            print(tile.coords)
            if tile.coords == (coords[0], int(coords[1])):
                return tile
    
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
