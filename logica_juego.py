import numpy as np
# Lógica del juego Connect 4
class Connect4:
    def __init__(self):
        # Tablero de 6 filas x 7 columnas lleno de ceros
        self.board = np.zeros((6, 7), dtype=int)
        
    def get_state(self):
        # Convierte el tablero en una tupla (necesario para la Q-table)
        return tuple(self.board.flatten())

    def get_valid_moves(self):
        # Retorna las columnas que no están llenas (fila superior es 0)
        return [j for j in range(7) if self.board[0, j] == 0]

    def drop_piece(self, col, player):
        # Busca la primera fila vacía de abajo hacia arriba
        for row in range(5, -1, -1):
            if self.board[row, col] == 0:
                self.board[row, col] = player
                return True
        return False

    def check_winner(self, player):
        b = self.board
        # Horizontal
        for r in range(6):
            for c in range(4):
                if all(b[r, c+k] == player for k in range(4)): return True
        # Vertical
        for r in range(3):
            for c in range(7):
                if all(b[r+k, c] == player for k in range(4)): return True
        # Diagonal /
        for r in range(3, 6):
            for c in range(4):
                if all(b[r-k, c+k] == player for k in range(4)): return True
        # Diagonal \
        for r in range(3):
            for c in range(4):
                if all(b[r+k, c+k] == player for k in range(4)): return True
        return False

    def is_full(self):
        return len(self.get_valid_moves()) == 0
