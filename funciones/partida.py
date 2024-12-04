import random
from funciones.carta import generar_carta, puntaje_carta  # Importar funciones de carta.py
from funciones.jugadores import jugador_humano, jugador_aleatorio  # Funciones para las decisiones de los jugadores
from funciones.envido import gestionar_envido  # Función para manejar el envido
from funciones.truco import gestionar_truco  # Función para manejar el truco
from typing import List, Tuple  # Para definir los tipos de las listas y tuplas

def repartir_cartas(carta: List[Tuple[int, str]]) -> Tuple[List[Tuple[int, str]], List[Tuple[int, str]]]:
    
    # reparte 3 cartas a cada jugador y retorna las manos.    
    random.shuffle(carta)  # mezclar las cartas
    return carta[:3], carta[3:6]  # repartir las primeras 3 cartas a cada jugador


def jugar_partida(
    puntos_humano: int, 
    puntos_maquina: int, 
    puntaje_objetivo: int = 15
) -> Tuple[int, int]:
    '''
    Ejecuta una partida de truco entre el jugador y la maquina.
    Maneja el envido, los cantos del truco y las rondas de juego.
    '''
    mano_actual: str = 'humano'  # determina quien es mano en cada ronda

    while puntos_humano < puntaje_objetivo and puntos_maquina < puntaje_objetivo:
        # generar y reparte las cartas
        carta: List[Tuple[int, str]] = generar_carta()
        cartas_humano, cartas_maquina = repartir_cartas(carta)

        print(f'\n{'Eres mano' if mano_actual == 'humano' else 'La maquina es mano'}.')
        print('\nTus cartas son:', cartas_humano)

        # jugar el envido
        puntos_envido_humano, puntos_envido_maquina = gestionar_envido(
            cartas_humano, cartas_maquina, puntos_humano, puntos_maquina, mano_actual
        )
        puntos_humano += puntos_envido_humano
        puntos_maquina += puntos_envido_maquina

        print(f'\nPuntuación tras el envido: Tú {puntos_humano} | maquina {puntos_maquina}')

        # inicializar el estado del truco y las rondas
        truco_cantado: str = None
        turno: str = mano_actual
        rondas_ganadas_humano: int = 0
        rondas_ganadas_maquina: int = 0
        rechazo: bool = False

        for ronda in range(3):
            print(f'\nRonda {ronda + 1}')

            if turno == 'humano':
                # el jugador juega primero
                puntos_truco_humano, puntos_truco_maquina, truco_cantado = gestionar_truco(
                    cartas_maquina, ronda, turno, truco_cantado
                )
                puntos_humano += puntos_truco_humano
                puntos_maquina += puntos_truco_maquina

                if truco_cantado is None and (puntos_truco_humano > 0 or puntos_truco_maquina > 0):
                    rechazo = True
                    break

                carta_humano = jugador_humano(cartas_humano)
                carta_maquina = jugador_aleatorio(cartas_maquina)
                print(f'Tú juegas: {carta_humano} | La maquina responde: {carta_maquina}')
            else:
                # la maquina juega primero
                carta_maquina = jugador_aleatorio(cartas_maquina)
                print(f'La maquina juega: {carta_maquina}')  # mostrar la carta que juega la maquina

                # permitir al jugador cantar después de ver la carta de la maquina
                puntos_truco_humano, puntos_truco_maquina, truco_cantado = gestionar_truco(
                    cartas_maquina, ronda, turno, truco_cantado
                )
                puntos_humano += puntos_truco_humano
                puntos_maquina += puntos_truco_maquina

                if truco_cantado is None and (puntos_truco_humano > 0 or puntos_truco_maquina > 0):
                    rechazo = True
                    break

                carta_humano = jugador_humano(cartas_humano)
                print(f'Tú respondes: {carta_humano}')

            # comparar el valor de las cartas
            puntaje_humano = puntaje_carta(carta_humano)
            puntaje_maquina = puntaje_carta(carta_maquina)

            if puntaje_humano > puntaje_maquina:
                rondas_ganadas_humano += 1
                print('Ganas esta ronda.')
                turno = 'humano'  # el ganador toma el turno
            elif puntaje_humano < puntaje_maquina:
                rondas_ganadas_maquina += 1
                print('La maquina gana esta ronda.')
                turno = 'maquina'  
            else:
                print('Empate en esta ronda.') 

        if rechazo:
            continue

        # determinar el ganador de las rondas
        if rondas_ganadas_humano > rondas_ganadas_maquina:
            puntos_humano += 1
            print('\n¡Ganas las rondas del truco!')
        elif rondas_ganadas_maquina > rondas_ganadas_humano:
            puntos_maquina += 1
            print('\nLa maquina gana las rondas del truco.')
        else:
            print('\nLas rondas terminan en empate.')

        print(f'\nPuntuación tras la partida: Tú {puntos_humano} | maquina {puntos_maquina}')

        # alternar quién es mano para la próxima mano
        mano_actual = 'humano' if mano_actual == 'maquina' else 'maquina'

    return puntos_humano, puntos_maquina


