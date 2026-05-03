import re

# --- Definición de Patrones (Expresiones Regulares) ---

# 1. Notación Científica:
#    - ^[-+]?            -> Signo opcional al inicio
#    - (\d+(\.\d*)?|\.\d+) -> La mantisa (ej. 5, 5.2, 5., .2)
#    - [eE]               -> El caracter 'e' o 'E'
#    - [-+]?              -> Signo opcional del exponente
#    - \d+$               -> Los dígitos del exponente al final
REGEX_NOTACION_CIENTIFICA = re.compile(r"^[-+]?(\d+(\.\d*)?|\.\d+)[eE][-+]?\d+$")

# 2. Dirección IP (IPv4):
#    - ^ ... $           -> Asegura que la cadena completa coincida
#    - ( ... \.){3}     -> 3 bloques de (octeto + punto)
#    - ( ... )           -> 1 bloque de (octeto) final
#
#    El bloque del octeto (0-255) es:
#    - 25[0-5]           -> 250-255
#    - 2[0-4]\d          -> 200-249
#    - 1\d{2}            -> 100-199
#    - [1-9]?\d          -> 0-99 (sin ceros a la izquierda)
OCTETO = r"(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)"
REGEX_IP = re.compile(rf"^{OCTETO}\.{OCTETO}\.{OCTETO}\.{OCTETO}$")

# 3. Correo Electrónico:
#    - ^[\w._+-]+        -> "Parte local" (usuario)
#    - @                 -> El símbolo @
#    - ([\w-]+\.)+       -> Subdominios (ej. "mail.google.")
#    - [a-zA-Z]{2,}$     -> Dominio de nivel superior (ej. "com", "net", "es")
REGEX_CORREO = re.compile(r"^[\w._+-]+@([\w-]+\.)+[a-zA-Z]{2,}$")


# --- Funciones de Reconocimiento ---

def es_notacion_cientifica(cadena: str) -> bool:
    """Verifica si la cadena es una notación científica válida."""
    if REGEX_NOTACION_CIENTIFICA.fullmatch(cadena):
        return True
    return False

def es_ip_valida(cadena: str) -> bool:
    """Verifica si la cadena es una dirección IPv4 válida (0-255)."""
    if REGEX_IP.fullmatch(cadena):
        return True
    return False

def es_correo_valido(cadena: str) -> bool:
    """Verifica si la cadena tiene un formato de correo electrónico válido."""
    if REGEX_CORREO.fullmatch(cadena):
        return True
    return False

# --- Demostración ---
if __name__ == "__main__":
    
    print("--- 1. Reconocimiento de Notación Científica ---")
    cadenas_cientificas = [
        "1.23e4", "5e10", "-9.81E-5", "+1.0e+20", ".5e7", "5.e-1"
    ]
    cadenas_no_cientificas = [
        "1.23", "e10", "1.2e", "1.e-", "10e5.5", "5e 10"
    ]

    print("✅ Válidas:")
    for c in cadenas_cientificas:
        print(f"  '{c}': {es_notacion_cientifica(c)}")
        
    print("\n❌ Inválidas:")
    for c in cadenas_no_cientificas:
        print(f"  '{c}': {es_notacion_cientifica(c)}")
        
    print("\n" + "="*40 + "\n")
    
    # ---------------------------------------------------------------
    
    print("--- 2. Reconocimiento de Dirección IP (IPv4) ---")
    cadenas_ip = [
        "192.168.0.1", "127.0.0.1", "0.0.0.0", "255.255.255.255", "8.8.8.8"
    ]
    cadenas_no_ip = [
        "192.168.0.256",  # Número > 255
        "192.168.0",      # Faltan octetos
        "1.1.1.01",       # Cero a la izquierda
        "1.2.3.4.5",      # Demasiados octetos
        "texto.1.2.3",    # Contiene texto
        "192.168. 0.1"    # Contiene espacio
    ]

    print("✅ Válidas:")
    for c in cadenas_ip:
        print(f"  '{c}': {es_ip_valida(c)}")
        
    print("\n❌ Inválidas:")
    for c in cadenas_no_ip:
        print(f"  '{c}': {es_ip_valida(c)}")

    print("\n" + "="*40 + "\n")

    # ---------------------------------------------------------------

    print("--- 3. Reconocimiento de Correo Electrónico ---")
    cadenas_correo = [
        "usuario@dominio.com",
        "mi.nombre_123@sub.dominio.co.uk",
        "usuario+tag@gmail.com",
        "a@b.co"
    ]
    cadenas_no_correo = [
        "usuario@dominio",      # Sin .com/net/etc.
        "usuario@dominio.",     # Termina en punto
        "usuario@@dominio.com", # Doble @
        ".usuario@dominio.com", # Empieza con punto
        "usuario@.com",         # Dominio empieza con punto
        "sin_arroba.com"        # Sin @
    ]

    print("✅ Válidos:")
    for c in cadenas_correo:
        print(f"  '{c}': {es_correo_valido(c)}")
        
    print("\n❌ Inválidos:")
    for c in cadenas_no_correo:
        print(f"  '{c}': {es_correo_valido(c)}")