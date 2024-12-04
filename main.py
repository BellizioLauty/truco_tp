from funciones.partida import jugar_partida
from funciones.ranking import actualizar_ranking, mostrar_ranking

def elegir_puntaje_objetivo() -> int:
    'el jugador puede elegir si jugar 15 o 30 puntos.'
    while True:
        try:
            puntos: int = int(input('¿A cuantos puntos quieres jugar? (15 o 30): ').strip())
            if puntos in [15, 30]:
                return puntos
        except ValueError:
            pass
        print('numero incorrecto. Por favor, elige 15 o 30.')


def main() -> None:
    print('¡Bienvenido al Truco!')
    nombre: str = input('Ingresa tu nombre: ').strip()

    # elegir puntaje del juego
    puntaje_objetivo: int = elegir_puntaje_objetivo()

    # inicializar los puntos
    puntos_humano: int = 0
    puntos_maquina: int = 0

    # bucle principal del juego
    while puntos_humano < puntaje_objetivo and puntos_maquina < puntaje_objetivo:
        puntos_humano, puntos_maquina = jugar_partida(puntos_humano, puntos_maquina, puntaje_objetivo)
        print(f'\nPuntuación total: Tu {puntos_humano} | maquina {puntos_maquina}')

    # determinar el ganador final
    if puntos_humano >= puntaje_objetivo:
        print('\n¡Felicidades, ganaste el juego!')
        actualizar_ranking(nombre, puntos_humano) 
    else:
        print('\nLa maquina gana el juego. ¡Intenta nuevamente!')

    # mostrar el ranking al final del juego
    mostrar_ranking()


if __name__ == '__main__':
    main()
