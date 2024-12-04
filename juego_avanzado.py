
import pygame
from funciones.ranking import mostrar_ranking, actualizar_ranking
from funciones.carta import generar_carta
from funciones.envido import gestionar_envido
from funciones.truco import gestionar_truco
import os
import random

# inicialización de Pygame
pygame.init()

# configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Truco Argentino')

COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_AZUL = (70, 130, 180)
COLOR_ROJO = (220, 20, 60)
COLOR_VERDE = (34, 139, 34)

fuente = pygame.font.Font(None, 36)

# función para dibujar un botón
def dibujar_boton(texto, x, y, ancho, alto, color, color_texto):
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto))
    texto_superficie = fuente.render(texto, True, color_texto)
    pantalla.blit(
        texto_superficie,
        (x + (ancho - texto_superficie.get_width()) // 2,
         y + (alto - texto_superficie.get_height()) // 2)
    )

# cargar imágenes de cartas
def cargar_imagenes_cartas():
    CARPETA_CARTAS = 'imagenes/cartas'
    imagenes = {}
    for palo in ['espadas', 'bastos', 'oros', 'copas']:
        for numero in [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]:
            nombre_archivo = f'{numero}_{palo}.jpg'
            ruta = os.path.join(CARPETA_CARTAS, nombre_archivo)
            if os.path.exists(ruta):
                imagenes[(numero, palo)] = pygame.image.load(ruta)
            else:
                print(f'Falta la imagen: {nombre_archivo}')
    return imagenes

# función para generar cartas aleatorias
def repartir_cartas_aleatorias():
    baraja = generar_carta()
    random.shuffle(baraja)
    cartas_jugador = baraja[:3]
    cartas_maquina = baraja[3:6]
    return cartas_jugador, cartas_maquina

# mostrar cartas en pantalla
def mostrar_cartas(cartas, imagenes, posicion_y):
    espacio = 10
    ancho_carta = 100
    x_inicial = (ANCHO - (len(cartas) * (ancho_carta + espacio) - espacio)) // 2
    posiciones = []
    for i, carta in enumerate(cartas):
        x = x_inicial + i * (ancho_carta + espacio)
        if carta in imagenes:
            pantalla.blit(pygame.transform.scale(imagenes[carta], (ancho_carta, 150)), (x, posicion_y))
        posiciones.append((x, posicion_y, ancho_carta, 150))
    return posiciones

# pantalla inicial
def pantalla_inicial():
    while True:
        pantalla.fill(COLOR_NEGRO)
        dibujar_boton('JUGAR', ANCHO // 2 - 100, ALTO // 2 - 50, 200, 50, COLOR_AZUL, COLOR_BLANCO)
        dibujar_boton('VER RANKING', ANCHO // 2 - 100, ALTO // 2 + 50, 200, 50, COLOR_ROJO, COLOR_BLANCO)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()  # Salir del programa

            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if ANCHO // 2 - 100 <= x <= ANCHO // 2 + 100:
                    if ALTO // 2 - 50 <= y <= ALTO // 2:
                        return 'JUGAR'
                    elif ALTO // 2 + 50 <= y <= ALTO // 2 + 100:
                        return 'RANKING'

# pantalla de selección de puntaje y nombre
def pantalla_seleccion():
    pantalla.fill(COLOR_NEGRO)
    dibujar_boton('15 PUNTOS', ANCHO // 2 - 100, ALTO // 2 - 50, 200, 50, COLOR_AZUL, COLOR_BLANCO)
    dibujar_boton('30 PUNTOS', ANCHO // 2 - 100, ALTO // 2 + 50, 200, 50, COLOR_ROJO, COLOR_BLANCO)
    pygame.display.flip()
    puntaje_objetivo = None
    while puntaje_objetivo is None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None, None
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if ANCHO // 2 - 100 <= x <= ANCHO // 2 + 100:
                    if ALTO // 2 - 50 <= y <= ALTO // 2:
                        puntaje_objetivo = 15
                    elif ALTO // 2 + 50 <= y <= ALTO // 2 + 100:
                        puntaje_objetivo = 30

    pantalla.fill(COLOR_NEGRO)
    texto = fuente.render('Ingresa tu nombre: ', True, COLOR_BLANCO)
    pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 50))
    pygame.display.flip()
    nombre = ''
    ingresando_nombre = True
    while ingresando_nombre:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None, None
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre:
                    ingresando_nombre = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre += evento.unicode
        pantalla.fill(COLOR_NEGRO)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 50))
        texto_nombre = fuente.render(nombre, True, COLOR_BLANCO)
        pantalla.blit(texto_nombre, (ANCHO // 2 - texto_nombre.get_width() // 2, ALTO // 2))
        pygame.display.flip()

    return nombre, puntaje_objetivo

# juego principal
def juego_principal(nombre_jugador, puntaje_objetivo):
    imagenes_cartas = cargar_imagenes_cartas()
    jugando = True

    cartas_jugador, cartas_maquina = repartir_cartas_aleatorias()

    carta_jugada_jugador = None
    carta_jugada_maquina = None

    puntos_jugador, puntos_maquina = 0, 0
    botones = [
        {'texto': 'ENVIDO', 'x': ANCHO - 200, 'y': 200, 'ancho': 150, 'alto': 50, 'color': COLOR_AZUL},
        {'texto': 'TRUCO', 'x': ANCHO - 200, 'y': 300, 'ancho': 150, 'alto': 50, 'color': COLOR_ROJO},
    ]
    posiciones_cartas = []

    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos

                for boton in botones:
                    if boton['x'] <= x <= boton['x'] + boton['ancho'] and boton['y'] <= y <= boton['y'] + boton['alto']:
                        if boton['texto'] == 'ENVIDO':
                            puntos_jugador, puntos_maquina, _ = gestionar_envido(
                                cartas_jugador, cartas_maquina, puntos_jugador, puntos_maquina, 'jugador'
                            )
                        elif boton['texto'] == 'TRUCO':
                            gestionar_truco()

                for i, (pos_x, pos_y, ancho, alto) in enumerate(posiciones_cartas):
                    if pos_x <= x <= pos_x + ancho and pos_y <= y <= pos_y + alto:
                        carta_jugada_jugador = cartas_jugador.pop(i)
                        print(f'Jugador juega: {carta_jugada_jugador}')

                        if cartas_maquina:
                            carta_jugada_maquina = cartas_maquina.pop(random.randint(0, len(cartas_maquina) - 1))
                            print(f'maquina juega: {carta_jugada_maquina}')
                        break

        pantalla.fill(COLOR_VERDE)

        posiciones_cartas = mostrar_cartas(cartas_jugador, imagenes_cartas, 400)

        for boton in botones:
            dibujar_boton(boton['texto'], boton['x'], boton['y'], boton['ancho'], boton['alto'], boton['color'], COLOR_BLANCO)

        if carta_jugada_jugador:
            pantalla.blit(pygame.transform.scale(imagenes_cartas[carta_jugada_jugador], (100, 150)),
                          ((ANCHO - 200) // 2 - 100, ALTO // 2 - 50))

        if carta_jugada_maquina:
            pantalla.blit(pygame.transform.scale(imagenes_cartas[carta_jugada_maquina], (100, 150)),
                          ((ANCHO + 200) // 2 - 100, ALTO // 2 - 50))

        pygame.display.flip()

# función principal
def main():
    opcion = pantalla_inicial()
    if opcion == 'RANKING':
        mostrar_ranking()
    elif opcion == 'JUGAR':
        nombre, puntaje_objetivo = pantalla_seleccion()
        if nombre and puntaje_objetivo:
            juego_principal(nombre, puntaje_objetivo)

if __name__ == '__main__':
    main()
