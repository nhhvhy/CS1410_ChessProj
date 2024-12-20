import chess
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window


Builder.load_file('KVchess.kv')

class MenuScreen(Screen):
    pass

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.layout = self.ids.get('playArea', GridLayout)
        
        # Create the tiles with proper coordinates
        for y in range(1, 9):
            for x in range(1, 9):
                letter = chr(96 + x)  # Convert column index to letter (a-h)
                tile = self.createTile(letter, y)
                self.layout.add_widget(tile)

        self.selected_piece = None
        self.boardSetup()
        self.resetColors()
        self.updateBoard()

    # Reset board each time the play screen is opened
    def on_pre_enter(self):
        self.resetScreen()

    # Reset everything to the initial state
    def resetScreen(self):
        self.selected_piece = None
        self.boardSetup()
        self.resetColors()
        self.updateBoard()

    def updateBoard(self):
        # Correct piece placement to account for Kivy gridlayout quirks
        for space, tile in zip(chess.SQUARES[::-1], self.layout.children):
            piece = self.board.piece_at(space)
            if piece:
                tile.text = str(piece).lower()
                if piece.color:
                    tile.color = (1, 1, 1, 1)
                else:
                    tile.color = (0, 0, 0, 1)
            else:
                tile.text = ""

    def setStatus(self):
        status = self.ids.get('statusIndicator', Button)
        if self.board.is_check():
            arg = 'Check'
            if self.board.is_checkmate():
                arg = 'Checkmate'
        elif self.board.is_fifty_moves():
            arg = 'Draw'
        else:
            arg = 'Rotate'

        if arg == 'Rotate':
            if status.text == 'White\'s Turn' or status.text == 'Check! White\'s Turn':
                status.text = 'Black\'s Turn'
            else:
                status.text = 'White\'s Turn'

        if arg == 'Check':
            if status.text == 'White\'s Turn' or status.text == 'Check! White\'s Turn':
                status.text = 'Check! Black\'s Turn'
            else:
                status.text = 'Check! White\'s Turn' 

        if arg == 'Checkmate':
            if status.text == 'White\'s Turn' or status.text == 'Check! White\'s Turn':
                status.text = 'Checkmate! Black wins'
            else:
                status.text = 'Checkmate! White wins'

        if arg == 'Draw':
            status.text = '50 move limit reached! It\'s a draw'

    def createTile(self, letter, number):
        tile = Button()
        tile.coords = (letter, number)
        tile.bind(on_press=lambda instance: self.onTileSelect(tile.coords))
        tile.font_name = 'CHESSFONT.TTF'
        tile.font_size = Window.size[0] * 0.05
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
        self.resetColors()

        square = chess.parse_square(f"{coords[0].lower()}{coords[1]}")
        
        # If there's a selected piece, try to make a move. Reset if piece is clicked twice.
        if self.selected_piece:
            if self.selected_piece == coords:
                self.resetColors()
                self.selected_piece = None
                return
            # Construct move from selected piece and current square
            move = chess.Move.from_uci(self.selected_piece[0] + str(self.selected_piece[1]) + coords[0] + str(coords[1]))
            
            # Check if it's a pawn promotion move
            from_square = chess.parse_square(f"{self.selected_piece[0].lower()}{self.selected_piece[1]}")
            piece = self.board.piece_at(from_square)
            if piece and piece.piece_type == chess.PAWN:
                if (piece.color and coords[1] == 8) or (not piece.color and coords[1] == 1):
                    move = chess.Move(from_square, square, promotion=chess.QUEEN)
            
            # If the move is legal, push the move and reset the selected piece
            if move in self.board.legal_moves:
                self.board.push(move)
                self.updateBoard()
                self.selected_piece = None
                self.resetColors()
                self.setStatus()
                return
        
        # If no piece is selected, select the current piece
        if coords != self.selected_piece:  # Only highlight if no piece is already selected
            self.selected_piece = coords
            piece = self.board.piece_at(square)
            if piece:
                piece_moves = [move for move in self.board.legal_moves if move.from_square == square]
                for move in piece_moves:
                    self.highlightTile(str(move)[2:])
                self.highlightTile(coords, (0.8, 0.6, 0.6, 1))
        else:
            # Deselect piece if clicked again (nothing happens if same piece is clicked)
            self.selected_piece = None
            self.resetColors()

    def highlightTile(self, coords, color=(0.6, 0.8, 0.6, 1)):
        tile = self.getTileByCoords(coords)
        if tile:
            tile.background_color = color
    
    def getTileByCoords(self, coords):
        for tile in self.layout.children:
            if tile.coords == (coords[0], int(coords[1])):
                return tile
    
    def boardSetup(self):
        self.board = chess.Board()

class Main(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='MenuScreen'))
        sm.add_widget(GameScreen(name='GameScreen'))
        
        return sm
    
if __name__ == '__main__':
    Main().run()
