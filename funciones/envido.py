def calcular_envido(cartas: list[tuple[int, str]]) -> int:
    
    # calcula los puntos del envido
    
    valores: dict[int, int] = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 10: 0, 11: 0, 12: 0}
    palos: dict[str, list[int]] = {}

    # agrupa valores de las cartas por palo
    for carta in cartas:
        numero, palo = carta 
        if palo not in palos:
            palos[palo] = []
        palos[palo].append(valores[numero])

    max_envido: int = 0

    # calcular la máxima puntuación posible para el envido
    for palo, numeros in palos.items():
        if len(numeros) >= 2:
            numeros.sort(reverse=True) 
            max_envido = max(max_envido, 20 + numeros[0] + numeros[1])
        elif len(numeros) == 1:
            max_envido = max(max_envido, numeros[0])

    return max_envido


def gestionar_envido(
    cartas_humano: list[tuple[int, str]],
    cartas_maquina: list[tuple[int, str]],
    puntos_humano: int,
    puntos_maquina: int,
    es_mano: str
) -> tuple[int, int]:
    
    # maneja los cantos y la revolucion del envido
    
    envido_humano: int = calcular_envido(cartas_humano)
    envido_maquina: int = calcular_envido(cartas_maquina)
    puntos_apuesta: int = 0
    envido_cantado: dict[str, bool] = {'Envido': False, 'Real Envido': False, 'Falta Envido': False}
    envido_iniciado: bool = False

    # indicar los puntos iniciales y la mano actual
    print(f'\nTus puntos de envido: {envido_humano}')
    print(f"{'Eres mano' if es_mano == 'humano' else 'La maquina es mano'}.")

    turno: str = es_mano  
    mano_no_canta: bool = False

    # bucle de interacción para manejar los cantos
    while True:
        if turno == 'humano':
            # opciones disponibles para el jugador humano
            print('\nOpciones:')
            print('1: Cantar Envido' if not envido_cantado['Envido'] else '')
            print('2: Cantar Real Envido' if not envido_cantado['Real Envido'] else '')
            print('3: Cantar Falta Envido' if not envido_cantado['Falta Envido'] else '')
            print('4: No cantar nada' if not envido_iniciado else '')
            print('5: Aceptar (si la maquina cantó algo)' if envido_iniciado else '')
            print('6: Rechazar (si la maquina cantó algo)' if envido_iniciado else '')
            decision_humano: str = input('¿Qué quieres hacer? ').strip()

            # manejo de decisiones del jugador humano
            if decision_humano == '4' and not envido_iniciado:
                print('Decides no cantar nada.')
                if es_mano == 'humano':
                    turno = 'maquina'
                    mano_no_canta = True
                else:
                    return 0, 0  # si nadie canta nada
                continue
            elif decision_humano == '5' and envido_iniciado:
                print('Aceptas la apuesta.')
                break
            elif decision_humano == '6' and envido_iniciado:
                print('Rechazas la apuesta. La maquina gana los puntos acumulados.')
                return 0, puntos_apuesta
            elif decision_humano == '1' and not envido_cantado['Envido']:
                print('Cantas Envido.')
                puntos_apuesta += 2
                envido_cantado['Envido'] = True
                envido_iniciado = True
            elif decision_humano == '2' and not envido_cantado['Real Envido']:
                print('Cantas Real Envido.')
                puntos_apuesta += 3
                envido_cantado['Real Envido'] = True
                envido_iniciado = True
            elif decision_humano == '3' and not envido_cantado['Falta Envido']:
                falta: int = 15 - max(puntos_humano, puntos_maquina)
                print(f'Cantas Falta Envido (vale {falta} puntos).')
                puntos_apuesta += falta
                envido_cantado['Falta Envido'] = True
                envido_iniciado = True
            else:
                print('Opción no válida o apuesta ya cantada.')
                continue
            turno = 'maquina'
        else:
            # logica de cantos y decisiones de la maquina
            if not envido_iniciado:
                if mano_no_canta:
                    if envido_maquina >= 29:
                        print('La maquina canta Real Envido.')
                        puntos_apuesta += 3
                        envido_cantado['Real Envido'] = True
                        envido_iniciado = True
                    elif envido_maquina >= 26:
                        print('La maquina canta Envido.')
                        puntos_apuesta += 2
                        envido_cantado['Envido'] = True
                        envido_iniciado = True
                    else:
                        print('La maquina decide no cantar nada.')
                        return 0, 0
                else:
                    turno = 'humano'
                    mano_no_canta = True
                    continue
            else:
                # resolver rechazos de la maquina
                if envido_cantado['Falta Envido'] and envido_maquina < 32:
                    print('La maquina rechaza la Falta Envido.')
                    return 1, 0  # 1 punto para el que canto
                elif envido_cantado['Real Envido'] and envido_maquina < 29:
                    print('La maquina rechaza el Real Envido.')
                    return 1, 0  # 1 punto para el que canto
                elif envido_cantado['Envido'] and envido_maquina < 26:
                    print('La maquina rechaza el Envido.')
                    return 1, 0  # 1 punto para el que canto
                else:
                    print('La maquina acepta la apuesta.')
                    break
            turno = 'humano'

    # resolución final del envido
    print(f'\nResolviendo el envido...')
    print(f'Tus puntos de envido: {envido_humano}')
    print(f'Puntos de envido de la maquina: {envido_maquina}')
    if envido_humano > envido_maquina:
        print('¡Ganas el envido!')
        return puntos_apuesta, 0
    elif envido_maquina > envido_humano:
        print('La maquina gana el envido.')
        return 0, puntos_apuesta
    else:
        print('Empate en el envido. Ganas por ser mano.')
        return puntos_apuesta, 0

