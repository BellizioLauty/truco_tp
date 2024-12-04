def generar_carta() -> list[tuple[int, str]]:

    # generacion de cartas

    palos: tuple[str, str, str, str] = ('espadas', 'bastos', 'oros', 'copas')
    numeros: tuple[int, int, int, int, int, int, int, int, int, int] = (1, 2, 3, 4, 5, 6, 7, 10, 11, 12)
    return [(numero, palo) for palo in palos for numero in numeros]


def puntaje_carta(carta: tuple[int, str]) -> int:
    
    # calcula el valor de cada carta
    
    numero, palo = carta
    valores_truco: dict[tuple[int, str], int] = {
        (1, 'espadas'): 31,
        (1, 'bastos'): 30,
        (7, 'espadas'): 29,
        (7, 'oros'): 28,
        (3, 'espadas'): 27, (3, 'bastos'): 27, (3, 'oros'): 27, (3, 'copas'): 27,
        (2, 'espadas'): 26, (2, 'bastos'): 26, (2, 'oros'): 26, (2, 'copas'): 26,
        (1, 'oros'): 25, (1, 'copas'): 25,
        (12, 'espadas'): 24, (12, 'bastos'): 24, (12, 'oros'): 24, (12, 'copas'): 24,
        (11, 'espadas'): 23, (11, 'bastos'): 23, (11, 'oros'): 23, (11, 'copas'): 23,
        (10, 'espadas'): 22, (10, 'bastos'): 22, (10, 'oros'): 22, (10, 'copas'): 22,
        (7, 'copas'): 21, (7, 'bastos'): 21,
        (6, 'espadas'): 20, (6, 'bastos'): 20, (6, 'oros'): 20, (6, 'copas'): 20,
        (5, 'espadas'): 19, (5, 'bastos'): 19, (5, 'oros'): 19, (5, 'copas'): 19,
        (4, 'espadas'): 18, (4, 'bastos'): 18, (4, 'oros'): 18, (4, 'copas'): 18,
    }
    return valores_truco.get((numero, palo), 0)


