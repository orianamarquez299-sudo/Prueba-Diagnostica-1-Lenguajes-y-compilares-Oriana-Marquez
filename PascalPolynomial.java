import java.util.ArrayList;
import java.util.List;
import java.math.BigInteger;
import java.io.FileWriter;
import java.io.IOException;

public class PascalPolynomial {
    /**
     * Generates the n-th row of Pascal's triangle using BigInteger.
     * Uses dynamic memory with ArrayList.
     */
    public List<BigInteger> generateCoefficients(int n) {
        if (n < 0) {
            return new ArrayList<>();
        }

        // Start with row n=0
        List<BigInteger> prevRow = new ArrayList<>();
        prevRow.add(BigInteger.ONE);

        if (n == 0) {
            return prevRow;
        }

        // Iterate from n=1 up to the requested n
        for (int i = 1; i <= n; i++) {
            List<BigInteger> currentRow = new ArrayList<>();
            currentRow.add(BigInteger.ONE); // Always starts with 1

            // Compute intermediate elements
            for (int j = 1; j < i; j++) {
                // coeff = prev[j-1] + prev[j]
                BigInteger coeff = prevRow.get(j - 1).add(prevRow.get(j));
                currentRow.add(coeff);
            }

            currentRow.add(BigInteger.ONE); // Always ends with 1
            prevRow = currentRow; // Current row becomes the next "previous"
        }

        return prevRow;
    }

    /**
     * Prints the polynomial and computes f(x) = (x+1)^n step by step.
     */
    public void evaluatePolynomial(List<BigInteger> coeffs, int x) {
        int n = coeffs.size() - 1;
        BigInteger total = BigInteger.ZERO;
        BigInteger xBig = BigInteger.valueOf(x); // Convert x to BigInteger

        System.out.println("--- Evaluating for n=" + n + " and x=" + x + " ---");

        // Print the polynomial
        StringBuilder polynomialStr = new StringBuilder("f(x) = ");
        for (int i = 0; i <= n; i++) {
            int k = n - i; // Exponent
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

        // Calculate step by step
        System.out.println("\nCalculation of f(" + x + "):");
        for (int i = 0; i <= n; i++) {
            int k = n - i;
            BigInteger coeff = coeffs.get(i);
            // termValue = coeff * (x^k)
            BigInteger termValue = coeff.multiply(xBig.pow(k));
            
            System.out.println("  + Term " + i + ": (" + coeff + " * " + x + "^" + k + ") = " + termValue);
            total = total.add(termValue);
        }

        System.out.println("\nTotal Result: f(" + x + ") = " + total);
        
        // Verification
        BigInteger check = BigInteger.valueOf(x + 1).pow(n);
        System.out.println("Verification: (" + x + "+1)^" + n + " = " + check);
        System.out.println("---------------------------------");
    }

    /**
     * Main function to run tests and measure time.
     */
    public static void main(String[] args) {
        PascalPolynomial calculator = new PascalPolynomial();

        // 1. Demonstration with n=5 and x=2
        int nDemo = 5;
        int xDemo = 2;
        System.out.println("Generating coefficients for n=" + nDemo + "...");
        List<BigInteger> coeffsDemo = calculator.generateCoefficients(nDemo);
        System.out.println("Coefficients: " + coeffsDemo);
        calculator.evaluatePolynomial(coeffsDemo, xDemo);

        // 2. Timing measurement for n=100
        int nTest = 100;
        System.out.println("\nCalculating time for n=" + nTest + "...");

        long startTime = System.nanoTime();
        List<BigInteger> coefficients100 = calculator.generateCoefficients(nTest);
        long endTime = System.nanoTime();

        // nanoTime returns nanoseconds, convert to milliseconds
        double elapsedMs = (endTime - startTime) / 1_000_000.0;

        System.out.printf("Generation time (Java): %.4f ms\n", elapsedMs);
        System.out.println("Central coefficient (100 C 50): " + coefficients100.get(50));

        // 3. Write result to txt file
        // 'true' in FileWriter enables append mode
        try (FileWriter writer = new FileWriter("tiempos.txt", true)) {
            writer.write(String.format("Java (n=100): %.4f ms\n", elapsedMs));
            System.out.println("Timing result saved to 'tiempos.txt'");
        } catch (IOException e) {
            System.err.println("Error writing to file: " + e.getMessage());
        }
    }
}
