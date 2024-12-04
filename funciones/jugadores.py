import random

def jugador_humano(cartas: list[tuple[int, str]]) -> tuple[int, str]:
    
    # función para que el jugador elija una carta.
    
    print('Tus cartas:', cartas)
    while True:
        try:
            eleccion: int = int(input('Elige una carta (1, 2 o 3): ')) - 1
            if 0 <= eleccion < len(cartas):
                return cartas.pop(eleccion)
        except ValueError:
            pass
        print('Selección inválida. Intenta nuevamente.')


def jugador_aleatorio(cartas: list[tuple[int, str]]) -> tuple[int, str]:
    
    # función para que un jugador aleatorio elija una carta de manera al azar.
    
    return cartas.pop(random.randint(0, len(cartas) - 1))


def jugador_estrategico(cartas: list[tuple[int, str]], mesa: list[tuple[int, str]]) -> tuple[int, str]:
    if not mesa:
        return cartas.pop(cartas.index(max(cartas, key=lambda x: x[0])))

    mejor_carta_mesa: tuple[int, str] = max(mesa, key=lambda x: x[0])
    jugables: list[tuple[int, str]] = [carta for carta in cartas if carta[0] > mejor_carta_mesa[0]]
    if jugables:
        return cartas.pop(cartas.index(min(jugables, key=lambda x: x[0])))
    else:
        return cartas.pop(cartas.index(min(cartas, key=lambda x: x[0])))


