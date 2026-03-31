#include <stdio.h>

// BUSCA SEQUENCIAL
int buscaSequencial(int v[], int n, int chave, int *iteracoes) {
    *iteracoes = 0;
    for(int i = 0; i < n; i++) {
        (*iteracoes)++;
        if(v[i] == chave) {
            return i;
        }
    }
    return -1;
}

// BUSCA BINÁRIA
int buscaBinaria(int v[], int n, int chave, int *iteracoes) {
    int inicio = 0, fim = n - 1;
    *iteracoes = 0;

    while(inicio <= fim) {
        (*iteracoes)++;
        int meio = (inicio + fim) / 2;

        if(v[meio] == chave) {
            return meio;
        } else if(v[meio] < chave) {
            inicio = meio + 1;
        } else {
            fim = meio - 1;
        }
    }
    return -1;
}

int main() {
    // Vetor ordenado (necessário para busca binária)
    int vetor[20] = {2, 5, 8, 12, 15, 18, 21, 24, 27, 30,
                     33, 36, 39, 42, 45, 48, 51, 54, 57, 60};

    int n = 20;
    int chaveExistente = 24;
    int chaveInexistente = 100;

    int iterSeq, iterBin;

    // TESTE COM VALOR EXISTENTE
    printf("=== BUSCA VALOR EXISTENTE (%d) ===\n", chaveExistente);

    int posSeq = buscaSequencial(vetor, n, chaveExistente, &iterSeq);
    int posBin = buscaBinaria(vetor, n, chaveExistente, &iterBin);

    printf("Sequencial -> Posicao: %d | Iteracoes: %d\n", posSeq, iterSeq);
    printf("Binaria    -> Posicao: %d | Iteracoes: %d\n\n", posBin, iterBin);

    // TESTE COM VALOR INEXISTENTE
    printf("=== BUSCA VALOR INEXISTENTE (%d) ===\n", chaveInexistente);

    posSeq = buscaSequencial(vetor, n, chaveInexistente, &iterSeq);
    posBin = buscaBinaria(vetor, n, chaveInexistente, &iterBin);

    printf("Sequencial -> Posicao: %d | Iteracoes: %d\n", posSeq, iterSeq);
    printf("Binaria    -> Posicao: %d | Iteracoes: %d\n", posBin, iterBin);

    return 0;
}