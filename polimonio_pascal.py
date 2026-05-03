import time

def generate_coefficients(n: int) -> list[int]:
    """
    Genera la fila n del triángulo de Pascal usando memoria dinámica.
    Estos son los coeficientes de (x+1)^n.
    """
    if n < 0:
        return []
    if n == 0:
        return [1]

    # Empezamos con la fila n=0
    # Usamos solo la fila anterior para calcular la actual
    prev_row = [1]
    
    # Iteramos desde n=1 hasta el n solicitado
    for i in range(1, n + 1):
        # La nueva fila empieza con 1
        current_row = [1]
        
        # Calculamos los elementos intermedios sumando los de la fila anterior
        # (Esto implementa la memoria dinámica, solo necesitamos la fila n-1)
        for j in range(1, i):
            coeff = prev_row[j - 1] + prev_row[j]
            current_row.append(coeff)
            
        # La fila siempre termina con 1
        current_row.append(1)
        
        # La fila actual se convierte en la "anterior" para la sig. iteración
        prev_row = current_row
        
    return prev_row

def evaluate_polynomial(coeffs: list[int], x: int):
    """
    Muestra el polinomio y calcula f(x) = (x+1)^n paso a paso.
    """
    n = len(coeffs) - 1
    total = 0
    polynomial_str = "f(x) = "
    
    print(f"--- Evaluando para n={n} y x={x} ---")
    
    # Imprimir el polinomio
    for i in range(n + 1):
        k = n - i  # Exponente (de n a 0)
        coeff = coeffs[i]
        if k > 1:
            polynomial_str += f"{coeff}x^{k} + "
        elif k == 1:
            polynomial_str += f"{coeff}x + "
        else:
            polynomial_str += f"{coeff}"
    print(polynomial_str)

    # Calcular paso a paso
    print(f"\nCálculo de f({x}):")
    for i in range(n + 1):
        k = n - i
        coeff = coeffs[i]
        term_value = coeff * (x ** k)
        print(f"  + Término {i}: ({coeff} * {x}^{k}) = {term_value}")
        total += term_value
        
    print(f"\nResultado Total: f({x}) = {total}")
    # Verificación
    print(f"Verificación: ({x}+1)^{n} = {(x+1)**n}")
    print("---------------------------------")


# --- Función Principal ---
def main():
    # 1. Demostración con n=5 y x=2 (como en el ejemplo)
    n_demo = 5
    x_demo = 2
    print(f"Generando coeficientes para n={n_demo}...")
    coeffs_demo = generate_coefficients(n_demo)
    print(f"Coeficientes: {coeffs_demo}")
    evaluate_polynomial(coeffs_demo, x_demo)

    # 2. Medición de tiempo para n=100
    n_test = 100
    print(f"\nCalculando tiempo para n={n_test}...")
    
    start_time = time.perf_counter()
    coefficients_100 = generate_coefficients(n_test)
    end_time = time.perf_counter()
    
    # perf_counter da el tiempo en segundos, lo convertimos a milisegundos
    elapsed_ms = (end_time - start_time) * 1000
    
    print(f"Tiempo de generación (Python): {elapsed_ms:.4f} ms")
    # print(f"Coeficientes (n=100, primer y último): {coefficients_100[0]}, ..., {coefficients_100[-1]}")
    # print(f"Coeficiente central (100 C 50): {coefficients_100[50]}")


    # 3. Escribir resultado en archivo txt
    try:
        # 'a' (append) para añadir al archivo sin borrar lo que ponga Java
        with open("tiempos.txt", "a") as f:
            f.write(f"Python (n=100): {elapsed_ms:.4f} ms\n")
        print("Resultado de tiempo guardado en 'tiempos.txt'")
    except IOError as e:
        print(f"Error al escribir en el archivo: {e}")

if __name__ == "__main__":
    main()