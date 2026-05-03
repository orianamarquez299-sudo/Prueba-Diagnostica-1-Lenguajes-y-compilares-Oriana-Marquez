import re

def validar_fen(cadena_fen: str) -> (bool, str):

    
    # 1. Verificar que hay 6 campos
    campos = cadena_fen.split()
    if len(campos) != 6:
        return (False, f"Error: FEN debe tener 6 campos (encontrados {len(campos)}).")

    pieza, turno, enroque, al_paso, media_jugada, jugada_completa = campos

    # 2. Validar Campo 1: Posición de piezas
    filas = pieza.split('/')
    if len(filas) != 8:
        return (False, "Error Campo 1: Debe haber 8 filas separadas por 7 '/'.")

    for i, fila in enumerate(filas):
        if not fila:
            return (False, f"Error Campo 1: Fila {8-i} está vacía.")
        
        suma_fila = 0
        for char in fila:
            if char.isdigit():
                if '1' <= char <= '8':
                    suma_fila += int(char)
                else:
                    return (False, f"Error Campo 1: Fila {8-i} contiene un dígito inválido '{char}'.")
            elif char in "pnbrqkPNBRQK":
                suma_fila += 1
            else:
                return (False, f"Error Campo 1: Fila {8-i} contiene un caracter inválido '{char}'.")
        
        if suma_fila != 8:
            return (False, f"Error Campo 1: Fila {8-i} ('{fila}') no suma 8 (suma {suma_fila}).")

    # 3. Validar Campo 2: Turno
    if turno not in ('w', 'b'):
        return (False, f"Error Campo 2: Turno debe ser 'w' o 'b' (encontrado '{turno}').")

    # 4. Validar Campo 3: Enroque
    # Regex para: '-' O (al menos una de KQkq) Y (en el orden K?Q?k?q?)
    if not re.match(r"^-$|^(?=.*[KQkq])K?Q?k?q?$", enroque):
        return (False, f"Error Campo 3: Enroque '{enroque}' inválido (orden K, Q, k, q).")

    # 5. Validar Campo 4: Captura al paso
    if not re.match(r"^-$|^[a-h][36]$", al_paso):
        return (False, f"Error Campo 4: 'Al paso' ('{al_paso}') debe ser '-' o una casilla en fila 3 ó 6.")

    # 6. Validar Campo 5: Contador de medias jugadas
    if not media_jugada.isdigit() or int(media_jugada) < 0:
        return (False, f"Error Campo 5: 'Media jugada' ('{media_jugada}') debe ser un entero >= 0.")

    # 7. Validar Campo 6: Número de jugada completa
    if not jugada_completa.isdigit() or int(jugada_completa) < 1:
        return (False, f"Error Campo 6: 'Jugada completa' ('{jugada_completa}') debe ser un entero >= 1.")

    return (True, "FEN Válido.")

# --- Ejemplos de uso ---
fen_valido = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
fen_invalido_fila = "rnbqkbnr/ppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" # Fila 7 suma 7
fen_invalido_turno = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1" # Turno 'x'
fen_invalido_jugada = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0" # Jugada 0

print(f"'{fen_valido}':\n{validar_fen(fen_valido)}\n")
print(f"'{fen_invalido_fila}':\n{validar_fen(fen_invalido_fila)}\n")
print(f"'{fen_invalido_turno}':\n{validar_fen(fen_invalido_turno)}\n")
print(f"'{fen_invalido_jugada}':\n{validar_fen(fen_invalido_jugada)}\n")