#include <stdio.h>    
#include <stdlib.h>   
#include <string.h>   
#include <ctype.h>    

/**
 * @brief Estructura para el par de traducción.
 */
typedef struct {
    const char* c_keyword;
    const char* es_translation;
} KeywordPair;

/**
 * @brief Diccionario de palabras clave.
 */
KeywordPair keyword_dictionary[] = {
    {"auto", "automatico"}, {"break", "romper"}, {"case", "caso"},
    {"char", "caracter"}, {"const", "constante"}, {"continue", "continuar"},
    {"default", "defecto"}, {"do", "hacer"}, {"double", "doble"},
    {"else", "si_no"}, {"enum", "enumeracion"}, {"extern", "externo"},
    {"float", "flotante"}, {"for", "para"}, {"goto", "ir_a"},
    {"if", "si"}, {"inline", "en_linea"}, {"int", "entero"},
    {"long", "largo"}, {"register", "registro"}, {"restrict", "restringido"},
    {"return", "retornar"}, {"short", "corto"}, {"signed", "con_signo"},
    {"sizeof", "tamano_de"}, {"static", "estatico"}, {"struct", "estructura"},
    {"switch", "segun"}, {"typedef", "definir_tipo"}, {"union", "union"},
    {"unsigned", "sin_signo"}, {"void", "vacio"}, {"volatile", "volatil"},
    {"while", "mientras"}, {"_Bool", "_Booleano"}, {"_Complex", "_Complejo"},
    {"_Imaginary", "_Imaginario"},
    {NULL, NULL} 
};

/**
 * @brief Carga un archivo en memoria dinámica.
 */
char* load_file_to_memory(const char* filename) {
    FILE* file = fopen(filename, "rb");
    if (!file) {
        // Si el archivo no existe, creamos uno de prueba para que el programa no falle
        printf("Aviso: El archivo '%s' no existe. Creando uno de prueba...\n", filename);
        file = fopen(filename, "wb+");
        fprintf(file, "int main() { if(true) return 0; } // Ejemplo");
        fseek(file, 0, SEEK_SET);
    }

    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET); 

    char* buffer = (char*)malloc(file_size + 1);
    if (!buffer) {
        fclose(file);
        return NULL;
    }

    fread(buffer, 1, file_size, file);
    buffer[file_size] = '\0'; 
    
    fclose(file);
    printf("--- Archivo '%s' cargado (%ld bytes) ---\n\n", filename, file_size);
    return buffer;
}

const char* translate_keyword(const char* token) {
    for (int i = 0; keyword_dictionary[i].c_keyword != NULL; i++) {
        if (strcmp(keyword_dictionary[i].c_keyword, token) == 0) {
            return keyword_dictionary[i].es_translation;
        }
    }
    return NULL;
}

void verify_and_translate(char* code) {
    printf("--- Iniciando Analisis y Traduccion ---\n");
    
    int in_line_comment = 0, in_block_comment = 0, in_string = 0, in_char = 0;
    char* p = code;
    char current_token[100];
    int token_index = 0;
    
    while (*p != '\0') {
        // Manejo de Comentarios y Cadenas
        if (in_line_comment && *p == '\n') { in_line_comment = 0; }
        else if (in_block_comment && *p == '*' && *(p+1) == '/') { in_block_comment = 0; p += 2; continue; }
        
        if (in_line_comment || in_block_comment) { p++; continue; }

        if (in_string && *p == '"' && *(p-1) != '\\') { in_string = 0; p++; continue; }
        if (in_char && *p == '\'' && *(p-1) != '\\') { in_char = 0; p++; continue; }
        
        if (in_string || in_char) { p++; continue; }

        // Deteccion de estados
        if (*p == '/' && *(p+1) == '/') { in_line_comment = 1; p += 2; continue; }
        if (*p == '/' && *(p+1) == '*') { in_block_comment = 1; p += 2; continue; }
        if (*p == '"') { in_string = 1; p++; continue; }
        if (*p == '\'') { in_char = 1; p++; continue; }

        // Tokenización
        if (isalpha(*p) || *p == '_') {
            if (token_index < 99) current_token[token_index++] = *p;
        } 
        else if (isalnum(*p) && token_index > 0) {
            if (token_index < 99) current_token[token_index++] = *p;
        }
        else {
            if (token_index > 0) {
                current_token[token_index] = '\0';
                const char* translation = translate_keyword(current_token);
                if (translation) {
                    printf("  Palabra clave: '%s' -> '%s'\n", current_token, translation);
                }
                token_index = 0;
            }
        }
        p++;
    }
    printf("--- Analisis Finalizado ---\n");
}

int main() {
    const char* file_to_analyze = "traductor.c";
    char* code_buffer = load_file_to_memory(file_to_analyze);
    
    if (code_buffer) {
        verify_and_translate(code_buffer);
        free(code_buffer);
        printf("\nMemoria liberada correctamente.\n");
    }
    return 0;
} 
