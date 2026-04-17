# Práctica 6: Conecta 4 - IA Q-Learning
##### Fabián Betancourt Fernández 22760578 8SF 

Esta práctica implementa un agente de aprendizaje por refuerzo para jugar Conecta 4.

(Este proyecto fue generado con la ayuda de una IA).

### Reglas del Juego
1. El objetivo es alinear **4 fichas** (Horizontal, Vertical o Diagonal).
2. Se juega en un tablero de **6 filas x 7 columnas**.
3. Las fichas caen hasta la posición más baja disponible.

### Cómo ejecutar
1. Entrenar al agente:
   -Ejecute el archivo `main.py`
   
   -Escriba 1 (la opción para entrenar a la IA)
   
   -Escriba la cantidad de partidas que desee (ejemplo 10,000)
   
   -Eliga una cantidad de epsilon para jugar con su comportamiento (puede ser 0.1 o 0.03 hasta 1)
   
3. Jugar contra la IA:
   -Ejecuta el archivo `main.py `
   
   -Ecriba 2 (opción para jugar contra la IA)
   
   -Diviertase

## Estructura de la practica
Practica-6/

├── main.py              # Orquestador del juego y visualización (Matplotlib)

├── agente.py            # Lógica de Q-Learning (Ecuación de Bellman)

├── logica_juego.py      # Reglas del juego y gestión del tablero

├── q_table.pkl          # Archivo de memoria (se genera al entrenar)

└── README.md            # Documentación e instrucciones

## Explicación de cada archivo
1. main.py
   
Coordina los dos modos de ejecución:

Entrenamiento: Ejecuta miles de partidas a alta velocidad sin gráficos. Aquí el agente juega contra un rival aleatorio para recibir "castigos" (recompensa negativa) si pierde o "premios" (recompensa positiva) si gana.

Juego: Activa matplotlib para que tú puedas interactuar.

2. agente.py
   
Aquí reside la Ecuación de Bellman.

Q-Table: Es un diccionario donde la "llave" es el estado del tablero y el "valor" es una lista de 7 números (uno por columna).

Exploración vs. Explotación: Mediante Epsilon (ϵ), el agente decide si probar un movimiento al azar para aprender (exploración) o usar el mejor movimiento que ya conoce (explotación).

3. logica_juego.py

Su función principal es gestionar la matriz de $6 \times 7$.

get_valid_moves: Crucial para evitar que el código intente meter fichas en columnas llenas.

check_winner: Escanea el tablero en 4 direcciones. Es el "árbitro" que detiene el entrenamiento cuando alguien gana.

## Uso del epsilon y Ecuación De Bellman
Epsilon sirve para recolectar datos (probar todo el tablero).

Bellman sirve para procesar esos datos y asignarles un puntaje de "calidad" a cada celda del tablero.

## Dificultades En la Práctica
Durante el desarrollo, hubo ciertas dficultades técnicas y teóricas:

1. Explosión de Estados: Conecta 4 tiene billones de estados posibles. Aprenderlos todos con Q-Learning básico es imposible, por lo que el agente solo es "sabio" en las situaciones que ha visto muchas veces.
   
2. Manejo de la Interfaz Gráfica: matplotlib tiende a congelarse si no se gestionan correctamente los eventos de la ventana (flush_events) o si se detiene el código con un input() de consola.
   
3. Error de Lista Vacía: El agente intentaba buscar el mejor movimiento en tableros ya llenos (empate), lo que causaba un fallo en la función max(). Se solucionó con validaciones preventivas
   
4. Asignación de Recompensas (Credit Assignment): Determinar que un movimiento hecho al principio del juego fue el causante de perder 20 turnos después es el mayor reto del aprendizaje por refuerzo.

## Análisis de Parámetros
0.01,"El agente es muy ""rígido"". Si encuentra una estrategia que funciona una vez, deja de buscar otras mejores."

0.50,"Aprende mucho porque intenta muchas cosas locas, pero su tasa de victorias durante el entrenamiento es baja porque comete muchos errores a propósito."

1.0,"Caos total. Es puro azar. No sirve para jugar en serio, solo para llenar la memoria de experiencias aleatorias."

## Conclusión Final
El agente de Q-Learning logró desarrollar una estrategia defensiva y ofensiva básica tras 10,000 partidas. A diferencia de un algoritmo tradicional basado en reglas fijas, este agente 'entiende' el valor de las posiciones a través de la experiencia acumulada. Se observa que el rendimiento mejora drásticamente cuando se equilibra el factor de exploración, permitiendo que la IA descubra que el control de las columnas centrales aumenta sus probabilidades de éxito


