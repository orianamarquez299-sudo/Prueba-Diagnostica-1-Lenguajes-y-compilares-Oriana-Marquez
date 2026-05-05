  import java.util.ArrayList;
import java.util.List;
import java.math.BigInteger;
import java.io.FileWriter;
import java.io.IOException;

public class PascalPolynomial {

    /**
     * Genera la n-ésima fila del triángulo de Pascal usando BigInteger.
     * Utiliza memoria dinámica con ArrayList.
     */
    public List<BigInteger> generateCoefficients(int n) {
        if (n < 0) {
            return new ArrayList<>();
        }

        // Comenzamos con la fila n=0
        List<BigInteger> prevRow = new ArrayList<>();
        prevRow.add(BigInteger.ONE);

        if (n == 0) {
            return prevRow;
        }

        // Iteramos desde n=1 hasta el n solicitado
        for (int i = 1; i <= n; i++) {
            List<BigInteger> currentRow = new ArrayList<>();
            currentRow.add(BigInteger.ONE); // Siempre empieza con 1

            // Calculamos los elementos intermedios
            for (int j = 1; j < i; j++) {
                // coeff = prev[j-1] + prev[j]
                BigInteger coeff = prevRow.get(j - 1).add(prevRow.get(j));
                currentRow.add(coeff);
            }

            currentRow.add(BigInteger.ONE); // Siempre termina con 1
            prevRow = currentRow; // La fila actual pasa a ser la anterior
        }

        return prevRow;
    }

    /**
     * Imprime el polinomio y calcula f(x) = (x+1)^n paso a paso.
     */
    public void evaluatePolynomial(List<BigInteger> coeffs, int x) {
        int n = coeffs.size() - 1;
        BigInteger total = BigInteger.ZERO;
        BigInteger xBig = BigInteger.valueOf(x); 

        System.out.println("--- Evaluando para n=" + n + " y x=" + x + " ---");

        // Imprimir el polinomio
        StringBuilder polynomialStr = new StringBuilder("f(x) = ");
        for (int i = 0; i <= n; i++) {
            int k = n - i; // Exponente
            BigInteger coeff = coeffs.get(i);
            
            if (k > 1) {
                polynomialStr.append(coeff).append("x^").append(k).append(" + ");
            } else if (k == 1) {
                polynomialStr.append(coeff).append("x + ");
            } else {
                polynomialStr.append(coeff);
            }
        }
        System.out.println(polynomialStr.toString());

        // Cálculo paso a paso
        System.out.println("\nCálculo de f(" + x + "):");
        for (int i = 0; i <= n; i++) {
            int k = n - i;
            BigInteger coeff = coeffs.get(i);
            // termValue = coeff * (x^k)
            BigInteger termValue = coeff.multiply(xBig.pow(k));
            
            System.out.println("  + Término " + i + ": (" + coeff + " * " + x + "^" + k + ") = " + termValue);
            total = total.add(termValue);
        }

        System.out.println("\nResultado Total: f(" + x + ") = " + total);
        
        // Verificación
        BigInteger check = BigInteger.valueOf(x + 1).pow(n);
        System.out.println("Verificación: (" + x + "+1)^" + n + " = " + check);
        System.out.println("---------------------------------");
    }

    public static void main(String[] args) {
        PascalPolynomial calculator = new PascalPolynomial();

        // 1. Demostración con n=5 y x=2
        int nDemo = 5;
        int xDemo = 2;
        System.out.println("Generando coeficientes para n=" + nDemo + "...");
        List<BigInteger> coeffsDemo = calculator.generateCoefficients(nDemo);
        System.out.println("Coeficientes: " + coeffsDemo);
        calculator.evaluatePolynomial(coeffsDemo, xDemo);

        // 2. Medición de tiempo para n=100
        int nTest = 100;
        System.out.println("\nCalculando tiempo para n=" + nTest + "...");

        long startTime = System.nanoTime();
        List<BigInteger> coefficients100 = calculator.generateCoefficients(nTest);
        long endTime = System.nanoTime();

        // Convertimos nanosegundos a milisegundos
        double elapsedMs = (endTime - startTime) / 1_000_000.0;

        System.out.printf("Tiempo de generación (Java): %.4f ms\n", elapsedMs);
        System.out.println("Coeficiente central (100 C 50): " + coefficients100.get(50));

        // 3. Escribir resultado en archivo txt
        try (FileWriter writer = new FileWriter("tiempos.txt", true)) {
            writer.write(String.format("Java (n=100): %.4f ms\n", elapsedMs));
            System.out.println("\n[OK] Resultado de tiempo guardado en 'tiempos.txt'");
        } catch (IOException e) {
            System.err.println("Error al escribir en el archivo: " + e.getMessage());
        }
    }
}
