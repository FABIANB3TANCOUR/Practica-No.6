import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import os
import pickle
from logica_juego import Connect4
from agente import QLAgent

#Visualización del tablero usando Matplotlib
plt.ion()
fig, ax = plt.subplots(figsize=(6, 7))

def draw_board(board):
    ax.clear()
    # Fondo del tablero
    ax.add_patch(patches.Rectangle((0, 0), 7, 6, color='blue'))
    
    for i in range(6):
        for j in range(7):
            color = 'white'
            if board[i, j] == 1: color = 'red'    # IA
            elif board[i, j] == 2: color = 'yellow' # Humano
            
            ax.add_patch(patches.Circle((j + 0.5, 5.5 - i), 0.4, fill=True, color=color))
    
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.draw()
    plt.pause(0.1)
    fig.canvas.flush_events()

#Entrenamiento del agente Q-Learning
def entrenar_agente(episodios, epsilon_valor):
    env = Connect4()
    agente = QLAgent(alpha=0.1, gamma=0.9, epsilon=epsilon_valor)
    
    if os.path.exists("q_table.pkl"):
        agente.load_q_table()

    print(f"Entrenando {episodios} partidas con epsilon={epsilon_valor}...")
    victorias = 0

    for ep in range(episodios):
        env = Connect4()
        estado = env.get_state()
        terminado = False

        while not terminado:
            movimientos_ok = env.get_valid_moves()
            
            # Verificación 1: ¿Tablero lleno antes de que mueva la IA?
            if not movimientos_ok:
                terminado = True
                break

            accion = agente.choose_action(estado, movimientos_ok)
            env.drop_piece(accion, 1)

            if env.check_winner(1):
                agente.learn(estado, accion, 100, None, True)
                victorias += 1
                terminado = True
            elif env.is_full():
                agente.learn(estado, accion, 10, None, True)
                terminado = True
            else:
                # Turno del rival aleatorio
                rival_moves = env.get_valid_moves()
                if not rival_moves: # Verificación 2: ¿Tablero lleno antes del rival?
                    terminado = True
                    break
                
                rival_move = random.choice(rival_moves)
                env.drop_piece(rival_move, 2)
                
                if env.check_winner(2):
                    agente.learn(estado, accion, -100, None, True)
                    terminado = True
                else:
                    proximo_estado = env.get_state()
                    agente.learn(estado, accion, 0, proximo_estado, False)
                    estado = proximo_estado
        
        if (ep + 1) % 1000 == 0:
            print(f"Progreso: {ep + 1}/{episodios} partidas...")

    agente.save_q_table()
    print(f"\n¡Entrenamiento completado!")
    print(f"Victorias de la IA: {victorias} ({round(victorias/episodios*100, 2)}%)")

#Jugar contra la IA entrenada
def jugar_contra_ia():
    env = Connect4()
    agente = QLAgent(epsilon=0) # IA en modo experto (no explora)
    
    if not os.path.exists("q_table.pkl"):
        print("Error: No hay archivo de memoria. Entrena al agente primero.")
        return
    
    agente.load_q_table()
    print("\n--- INICIANDO PARTIDA ---")
    draw_board(env.board)

    while True:
        # TURNO HUMANO
        movs = env.get_valid_moves()
        if not movs: break
        
        try:
            print(f"Columnas disponibles: {movs}")
            col = int(input("Tu turno (0-6): "))
            if col not in movs:
                print("Movimiento no válido.")
                continue
        except ValueError:
            print("Entrada inválida.")
            continue

        env.drop_piece(col, 2)
        draw_board(env.board)
        
        if env.check_winner(2):
            print("¡Increíble! Has ganado.")
            break
        if env.is_full():
            print("Tablero lleno. Empate.")
            break

        # TURNO IA
        print("IA pensando...")
        estado_ia = env.get_state()
        movs_ia = env.get_valid_moves()
        # La IA elige la mejor acción basada en su memoria
        accion_ia = agente.choose_action(estado_ia, movs_ia, training=False)
        env.drop_piece(accion_ia, 1)
        draw_board(env.board)

        if env.check_winner(1):
            print("La IA ha ganado.")
            break
        if env.is_full():
            print("Empate.")
            break

# Menú principal
if __name__ == "__main__":
    while True:
        print("\n--- CONECTA 4 Q-LEARNING ---")
        print("1. Entrenar Agente")
        print("2. Jugar contra IA")
        print("3. Salir")
        op = input("Opción: ")

        if op == "1":
            n = int(input("Número de juegos (ej. 10000): "))
            e = float(input("Epsilon (ej. 0.1): "))
            entrenar_agente(n, e)
        elif op == "2":
            jugar_contra_ia()
        elif op == "3":
            break
