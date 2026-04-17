import numpy as np
import pickle
import random
# Agente de Q-Learning para Connect 4
class QLAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {} # Estado -> [q_valores para las 7 columnas]
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
# El agente elige acciones basándose en la Q-table y actualiza sus valores según la experiencia
    def get_q_values(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(7)
        return self.q_table[state]
# Elige una acción usando epsilon-greedy
    def choose_action(self, state, valid_moves, training=True):
        if training and random.random() < self.epsilon:
            return random.choice(valid_moves)
# Si no, elige la acción con el mayor valor Q entre las válidas        
        q_vals = self.get_q_values(state)
        # Filtrar solo movimientos válidos
        valid_q = {m: q_vals[m] for m in valid_moves}
        max_q = max(valid_q.values())
        # Elegir aleatoriamente entre los mejores si hay empate
        best_moves = [m for m, v in valid_q.items() if v == max_q]
        return random.choice(best_moves)
# Actualiza la Q-table usando la fórmula de Q-Learning
    def learn(self, state, action, reward, next_state, done):
        old_q = self.get_q_values(state)[action]
        next_max = 0 if done else np.max(self.get_q_values(next_state))
        
        # Fórmula de Q-Learning
        new_q = old_q + self.alpha * (reward + self.gamma * next_max - old_q)
        self.q_table[state][action] = new_q
# Guardar y cargar la Q-table para persistencia entre sesiones
    def save_q_table(self, filename="q_table.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.q_table, f)
# Carga la Q-table desde un archivo, si existe
    def load_q_table(self, filename="q_table.pkl"):
        try:
            with open(filename, "rb") as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            print("No se encontró memoria previa. Iniciando desde cero.")
