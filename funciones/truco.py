from funciones.carta import puntaje_carta
from typing import Tuple, Optional

def gestionar_truco(cartas_maquina: list, ronda_actual: int, turno: str, truco_cantado: Optional[str]) -> Tuple[int, int, Optional[str]]:
    '''
    gestiona los cantos del Truco, Retruco y Vale Cuatro
    si se rechaza un canto, se otorgan los puntos correspondientes al oponente y se termina la mano.
    '''
    valores_truco = {'Truco': 1, 'Retruco': 2, 'Vale Cuatro': 3}  # puntos por rechazar
    canto_actual = truco_cantado  
    truco_aceptado = False  # indica si el truco fue aceptado

    while True:
        if turno == 'humano':
            print('\nOpciones:')
            print('1: Jugar una carta sin cantar')
            print('2: Cantar Truco' if canto_actual is None else '')
            print('3: Cantar Retruco' if canto_actual == 'Truco' else '')
            print('4: Cantar Vale Cuatro' if canto_actual == 'Retruco' else '')
            print('5: Aceptar (si la máquina cantó algo)' if canto_actual and not truco_aceptado else '')
            print('6: Rechazar (si la máquina cantó algo)' if canto_actual and not truco_aceptado else '')
            decision_humano = input('¿Qué quieres hacer? ').strip()

            if decision_humano == '1':
                print('Juegas una carta sin cantar.')
                return 0, 0, canto_actual
            elif decision_humano == '2' and canto_actual is None:
                print('Cantas Truco.')
                canto_actual = 'Truco'
            elif decision_humano == '3' and canto_actual == 'Truco':
                print('Cantas Retruco.')
                canto_actual = 'Retruco'
            elif decision_humano == '4' and canto_actual == 'Retruco':
                print('Cantas Vale Cuatro.')
                canto_actual = 'Vale Cuatro'
            elif decision_humano == '5' and canto_actual and not truco_aceptado:
                print('Aceptas la apuesta.')
                truco_aceptado = True
                break
            elif decision_humano == '6' and canto_actual and not truco_aceptado:
                print(f'Rechazas la apuesta. La máquina gana {valores_truco[canto_actual]} puntos.')
                return 0, valores_truco[canto_actual], None  # termina la mano
            else:
                print('Opción no válida o canto ya realizado.')
                continue
            turno = 'maquina'
        else:
            # inteligencia de la máquina para cantar o rechazar
            if canto_actual is None:
                if ronda_actual >= 2 and any(puntaje_carta(carta) >= 25 for carta in cartas_maquina):
                    print('La máquina canta Truco.')
                    canto_actual = 'Truco'
                else:
                    print('La máquina juega una carta sin cantar.')
                    return 0, 0, canto_actual
            elif canto_actual == 'Truco':
                if any(puntaje_carta(carta) >= 27 for carta in cartas_maquina):
                    print('La máquina canta Retruco.')
                    canto_actual = 'Retruco'
                else:
                    print('La máquina acepta el Truco.')
                    truco_aceptado = True
                    break
            elif canto_actual == 'Retruco':
                if any(puntaje_carta(carta) >= 29 for carta in cartas_maquina):
                    print('La máquina canta Vale Cuatro.')
                    canto_actual = 'Vale Cuatro'
                else:
                    print(f'La máquina rechaza el Retruco. Ganas {valores_truco[canto_actual]} puntos.')
                    return valores_truco[canto_actual], 0, None  # termina la mano
            elif canto_actual == 'Vale Cuatro':
                print(f'La máquina rechaza el Vale Cuatro. Ganas {valores_truco[canto_actual]} puntos.')
                return valores_truco[canto_actual], 0, None  # termina la mano
            turno = 'humano'

    # resolución del truco si es aceptado
    puntos = valores_truco[canto_actual]
    print(f'\nResolviendo el canto: {canto_actual} (vale {puntos} puntos).')
    return (puntos, 0, canto_actual) if turno == 'humano' else (0, puntos, canto_actual)

