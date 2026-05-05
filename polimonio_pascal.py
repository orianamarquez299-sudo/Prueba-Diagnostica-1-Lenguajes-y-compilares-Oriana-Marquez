import time

def generate_coefficients(n: int) -> list[int]:
    """
    Genera la fila n del triángulo de Pascal usando programación dinámica.
    Estos son los coeficientes de (x+1)^n.
    """
    if n < 0:
        return []
    if n == 0:
        return [1]

    # Empezamos con la fila n=0
    prev_row = [1]
    
    # Iteramos desde n=1 hasta el n solicitado
    for i in range(1, n + 1):
        # La nueva fila empieza con 1
        current_row = [1]
        
        # Calculamos los elementos intermedios sumando los de la fila anterior
        for j in range(1, i):
            coeff = prev_row[j - 1] + prev_row[j]
            current_row.append(coeff)
            
        # La fila siempre termina con 1
        current_row.append(1)
        prev_row = current_row
        
    return prev_row

def evaluate_polynomial(coeffs: list[int], x: int):
    """
    Muestra el polinomio y calcula f(x) = (x+1)^n paso a paso.
    """
    n = len(coeffs) - 1
    total = 0
    polynomial_str = "f(x) = "
    
    print(f"\n--- Evaluando para n={n} y x={x} ---")
    
    # Construcción de la cadena del polinomio
    terms = []
    for i in range(n + 1):
        k = n - i
        coeff = coeffs[i]
        if k > 1:
            terms.append(f"{coeff}x^{k}")
        elif k == 1:
            terms.append(f"{coeff}x")
        else:
            terms.append(f"{coeff}")
    
    print(polynomial_str + " + ".join(terms))

    # Calcular paso a paso
    print(f"\nCálculo de f({x}):")
    for i in range(n + 1):
        k = n - i
        coeff = coeffs[i]
        term_value = coeff * (x ** k)
        print(f"  + Término {i}: ({coeff} * {x}^{k}) = {term_value}")
        total += term_value
        
    print(f"\nResultado Total: f({x}) = {total}")
    print(f"Verificación: ({x}+1)^{n} = {(x+1)**n}")
    print("-" * 33)

def main():
    # 1. Demostración inicial
    n_demo, x_demo = 5, 2
    print(f"Generando coeficientes para n={n_demo}...")
    coeffs_demo = generate_coefficients(n_demo)
    print(f"Coeficientes: {coeffs_demo}")
    evaluate_polynomial(coeffs_demo, x_demo)

    # 2. Medición de rendimiento
    n_test = 100
    print(f"\nCalculando tiempo de ejecución para n={n_test}...")
    
    start_time = time.perf_counter()
    _ = generate_coefficients(n_test)
    end_time = time.perf_counter()
    
    elapsed_ms = (end_time - start_time) * 1000
    print(f"Tiempo de generación: {elapsed_ms:.4f} ms")

    # 3. Persistencia de datos
    try:
        with open("tiempos.txt", "a", encoding="utf-8") as f:
            f.write(f"Python (n={n_test}): {elapsed_ms:.4f} ms\n")
        print("\n[OK] Tiempo guardado en 'tiempos.txt'")
    except IOError as e:
        print(f"\n[ERROR] No se pudo escribir en el archivo: {e}")

if __name__ == "__main__":
    main() 
