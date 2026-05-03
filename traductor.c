#include <stdio.h>    
#include <stdlib.h>   
#include <string.h>   
#include <ctype.h>    

/**
 * @brief Define el par de traducci�n de palabras clave.
 */
typedef struct {
    const char* c_keyword;
    const char* es_translation;
} KeywordPair;

/**
 * @brief Diccionario de palabras clave de C (C99/C11) y sus traducciones.
 */
KeywordPair keyword_dictionary[] = {
    {"auto", "automatico"},
    {"break", "romper"},
    {"case", "caso"},
    {"char", "caracter"},
    {"const", "constante"},
    {"continue", "continuar"},
    {"default", "defecto"},
    {"do", "hacer"},
    {"double", "doble"},
    {"else", "si_no"},
    {"enum", "enumeracion"},
    {"extern", "externo"},
    {"float", "flotante"},
    {"for", "para"},
    {"goto", "ir_a"},
    {"if", "si"},
    {"inline", "en_linea"},
    {"int", "entero"},
    {"long", "largo"},
    {"register", "registro"},
    {"restrict", "restringido"},
    {"return", "retornar"},
    {"short", "corto"},
    {"signed", "con_signo"},
    {"sizeof", "tamano_de"},
    {"static", "estatico"},
    {"struct", "estructura"},
    {"switch", "segun"},
    {"typedef", "definir_tipo"},
    {"union", "union"},
    {"unsigned", "sin_signo"},
    {"void", "vacio"},
    {"volatile", "volatil"},
    {"while", "mientras"},
    {"_Bool", "_Booleano"},
    {"_Complex", "_Complejo"},
    {"_Imaginary", "_Imaginario"},
    {NULL, NULL} // Centinela para marcar el final del array
};

/**
 * @brief Carga un archivo completo en un b�fer de memoria din�mica.
 * @param filename El nombre del archivo a cargar.
 * @return Un puntero al b�fer alocado din�micamente (debe ser liberado con free()).
 */
char* load_file_to_memory(const char* filename) {
    FILE* file = fopen(filename, "rb");
    if (!file) {
        perror("Error critico al abrir el archivo");
        return NULL;
    }

    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET); 

    // Alocar memoria din�mica
    char* buffer = (char*)malloc(file_size + 1);
    if (!buffer) {
        fprintf(stderr, "Error critico al alocar %ld bytes de memoria\n", file_size + 1);
        fclose(file);
        return NULL;
    }

    // Leer el archivo completo en el b�fer
    size_t bytes_read = fread(buffer, 1, file_size, file);
    if (bytes_read != file_size) {
        fprintf(stderr, "Error de lectura del archivo (se esperaban %ld, se leyeron %zu)\n", file_size, bytes_read);
        fclose(file);
        free(buffer);
        return NULL;
    }

    buffer[file_size] = '\0'; // Asegurar terminaci�n nula
    
    fclose(file);
    printf("--- Archivo '%s' cargado exitosamente en memoria dinamica (%ld bytes) ---\n\n", filename, file_size);
    return buffer;
}

/**
 * @brief Busca un token en el diccionario de palabras clave.
 * @return El string de la traduccion si se encuentra, o NULL si no es una palabra clave.
 */
const char* translate_keyword(const char* token) {
    for (int i = 0; keyword_dictionary[i].c_keyword != NULL; i++) {
        if (strcmp(keyword_dictionary[i].c_keyword, token) == 0) {
            return keyword_dictionary[i].es_translation;
        }
    }
    return NULL;
}

/**
 * @brief Analiza el bufer de codigo, identifica palabras clave y las traduce.
 * Este es un analizador simple que maneja comentarios y cadenas.
 */
void verify_and_translate(char* code) {
    printf("--- Iniciando Analisis y Traduccion ---\n");
    
    int in_line_comment = 0;
    int in_block_comment = 0;
    int in_string = 0;
    int in_char = 0;
    
    char* p = code;
    char current_token[100];
    int token_index = 0;
    
    while (*p != '\0') {
        // --- Manejo de Estados (Comentarios y Cadenas) ---

        if (in_line_comment && *p == '\n') {
            in_line_comment = 0;
            p++;
            continue;
        }
        
        if (in_block_comment && *p == '*' && *(p+1) == '/') {
            in_block_comment = 0;
            p += 2; // Saltar '*/'
            continue;
        }
        
        if (in_line_comment || in_block_comment) {
            p++;
            continue;
        }

        if (in_string && *p == '"' && *(p-1) != '\\') {
            in_string = 0;
            p++;
            continue;
        }

        if (in_char && *p == '\'' && *(p-1) != '\\') {
            in_char = 0;
            p++;
            continue;
        }
        
        if (in_string || in_char) {
            p++;
            continue;
        }

        // --- Deteccion de Inicio de Estados ---
        
        if (*p == '/' && *(p+1) == '/') {
            in_line_comment = 1;
            p += 2;
            continue;
        }

        if (*p == '/' && *(p+1) == '*') {
            in_block_comment = 1;
            p += 2;
            continue;
        }
        
        if (*p == '"') {
            in_string = 1;
            p++;
            continue;
        }
        
        if (*p == '\'') {
            in_char = 1;
            p++;
            continue;
        }

        // --- Logica de Tokenizacion (Armado de palabras) ---
        
        if (isalpha(*p) || *p == '_') {
            if (token_index < 99) {
                current_token[token_index++] = *p;
            }
        } 
        else if (isalnum(*p) && token_index > 0) {
            if (token_index < 99) {
                current_token[token_index++] = *p;
            }
        }
        else if (token_index > 0) {
            current_token[token_index] = '\0'; // Terminar el token
            
            // Verificar si el token es una palabra clave
            const char* translation = translate_keyword(current_token);
            if (translation) {
                printf("  Palabra clave encontrada: C = '%s', Espa�ol = '%s'\n", current_token, translation);
            }
            
            token_index = 0;
            memset(current_token, 0, sizeof(current_token));
        }

        p++; // Avanzar al siguiente caracter
    }
    
    printf("--- Analisis Finalizado ---\n");
}

/**
 * @brief Funcion principal
 */
int main() {
    
    const char* file_to_analyze = "traductor.c";

    // 1. Cargar el programa en memoria din�mica
    char* code_buffer = load_file_to_memory(file_to_analyze);
    
    if (code_buffer == NULL) {
        fprintf(stderr, "No se pudo cargar el archivo '%s' en memoria.\n", file_to_analyze);
        return 1; // Salir con error
    }

    // 2. Verificar y traducir las palabras clave en el b�fer
    verify_and_translate(code_buffer);
    
    // 3. Liberar la memoria din�mica
    free(code_buffer);
    printf("\nMemoria dinamica liberada correctamente.\n");
    
    return 0; // Salir con �xito
}
