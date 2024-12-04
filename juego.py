import pygame
from funciones.ranking import mostrar_ranking, actualizar_ranking, cargar_ranking
from funciones.partida import jugar_partida
from funciones.carta import generar_carta
import os

# inicialización de Pygame
pygame.init()

# configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Truco Argentino')

# colores
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_AZUL = (70, 130, 180)
COLOR_ROJO = (220, 20, 60)
COLOR_VERDE = (34, 139, 34)

# fuente
fuente = pygame.font.Font(None, 36)

# función para dibujar un botón
def dibujar_boton(texto, x, y, ancho, alto, color, color_texto):
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto))
    texto_superficie = fuente.render(texto, True, color_texto)
    pantalla.blit(
        texto_superficie,
        (x + (ancho - texto_superficie.get_width()) // 2,
         y + (alto - texto_superficie.get_height()) // 2),
    )

# función para cargar imágenes de cartas
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

# mostrar cartas en la pantalla
def mostrar_cartas(cartas, imagenes, posicion_y):
    espacio = 10
    ancho_carta = 100
    x_inicial = (ANCHO - (len(cartas) * (ancho_carta + espacio) - espacio)) // 2
    for i, carta in enumerate(cartas):
        x = x_inicial + i * (ancho_carta + espacio)
        if carta in imagenes:
            pantalla.blit(pygame.transform.scale(imagenes[carta], (ancho_carta, 150)), (x, posicion_y))
    return x_inicial, ancho_carta, espacio

# pantalla inicial con opciones
def pantalla_inicial():
    while True:
        pantalla.fill(COLOR_NEGRO)
        dibujar_boton('JUGAR', ANCHO // 2 - 100, ALTO // 2 - 50, 200, 50, COLOR_AZUL, COLOR_BLANCO)
        dibujar_boton('VER RANKING', ANCHO // 2 - 100, ALTO // 2 + 50, 200, 50, COLOR_ROJO, COLOR_BLANCO)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if ANCHO // 2 - 100 <= x <= ANCHO // 2 + 100:
                    if ALTO // 2 - 50 <= y <= ALTO // 2:
                        return 'JUGAR'
                    elif ALTO // 2 + 50 <= y <= ALTO // 2 + 100:
                        return 'RANKING'
        pygame.display.flip()

# pantalla de selección de puntaje objetivo
def seleccionar_puntaje():
    while True:
        pantalla.fill(COLOR_NEGRO)
        dibujar_boton('15 PUNTOS', ANCHO // 2 - 100, ALTO // 2 - 50, 200, 50, COLOR_AZUL, COLOR_BLANCO)
        dibujar_boton('30 PUNTOS', ANCHO // 2 - 100, ALTO // 2 + 50, 200, 50, COLOR_ROJO, COLOR_BLANCO)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if ANCHO // 2 - 100 <= x <= ANCHO // 2 + 100:
                    if ALTO // 2 - 50 <= y <= ALTO // 2:
                        return 15
                    elif ALTO // 2 + 50 <= y <= ALTO // 2 + 100:
                        return 30
        pygame.display.flip()

# función para pedir el nombre del jugador
def pedir_nombre():
    while True:
        pantalla.fill(COLOR_NEGRO)
        texto = fuente.render('Ingresa tu nombre: ', True, COLOR_BLANCO)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 50))
        pygame.display.flip()

        nombre = ''
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        return nombre
                    elif evento.key == pygame.K_BACKSPACE:
                        nombre = nombre[:-1]
                    else:
                        nombre += evento.unicode
            pantalla.fill(COLOR_NEGRO)
            pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 50))
            texto_nombre = fuente.render(nombre, True, COLOR_BLANCO)
            pantalla.blit(texto_nombre, (ANCHO // 2 - texto_nombre.get_width() // 2, ALTO // 2))
            pygame.display.flip()

# juego principal
def juego_principal(puntaje_objetivo, nombre_jugador):
    imagenes_cartas = cargar_imagenes_cartas()
    jugando = True
    cartas_jugador = generar_carta()[:3]  # tres cartas de prueba
    cartas_jugadas = []
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                x_inicial, ancho_carta, espacio = mostrar_cartas(cartas_jugador, imagenes_cartas, ALTO - 200)
                for i, carta in enumerate(cartas_jugador):
                    x_carta = x_inicial + i * (ancho_carta + espacio)
                    if x_carta <= x <= x_carta + ancho_carta and ALTO - 200 <= y <= ALTO - 50:
                        cartas_jugadas.append(carta)
                        cartas_jugador.pop(i)
                        break

            # detectar clic en los botones de Truco y Envido

        pantalla.fill(COLOR_VERDE)
        mostrar_cartas(cartas_jugador, imagenes_cartas, ALTO - 200)
        for i, carta in enumerate(cartas_jugadas):
            x = (ANCHO - 100) // 2 + i * 110
            if carta in imagenes_cartas:
                pantalla.blit(pygame.transform.scale(imagenes_cartas[carta], (100, 150)), (x, ALTO // 2 - 75))
        pygame.display.flip()

# función principal del programa
def main():
    opcion = pantalla_inicial()
    if opcion == 'RANKING':
        mostrar_ranking()
    elif opcion == 'JUGAR':
        puntaje_objetivo = seleccionar_puntaje()
        if puntaje_objetivo:
            nombre_jugador = pedir_nombre()
            if nombre_jugador:
                juego_principal(puntaje_objetivo, nombre_jugador)

if __name__ == '__main__':
    main()

