import os
from typing import Dict

ARCHIVO_RANKING = 'ranking.txt'

def cargar_ranking() -> Dict[str, int]:
    
    # carga el ranking desde un archivo.

    if not os.path.exists(ARCHIVO_RANKING):
        return {}

    ranking = {}
    with open(ARCHIVO_RANKING, 'r') as archivo:
        for linea in archivo:
            nombre, puntaje = linea.strip().split(',')
            ranking[nombre] = int(puntaje)
    return ranking

def guardar_ranking(ranking: Dict[str, int]) -> None:
    
    # guarda el ranking en un archivo.

    with open(ARCHIVO_RANKING, 'w') as archivo:
        for nombre, puntaje in ranking.items():
            archivo.write(f'{nombre},{puntaje}\n')

def actualizar_ranking(nombre: str, puntaje: int) -> None:
    
    # actualiza el ranking con el puntaje del jugador. Si el jugador ya existe, actualiza su puntaje.

    ranking = cargar_ranking()
    if nombre in ranking:
        ranking[nombre] = max(ranking[nombre], puntaje)  # mantiene el puntaje mas alto
    else:
        ranking[nombre] = puntaje
    guardar_ranking(ranking)

def mostrar_ranking() -> None:
    
    # muestra el ranking en orden de puntaje.
    
    ranking = cargar_ranking()
    print('\n--- Ranking ---')
    ranking_ordenado = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    for i, (nombre, puntaje) in enumerate(ranking_ordenado, 1):
        print(f'{i}. {nombre}: {puntaje} puntos')
