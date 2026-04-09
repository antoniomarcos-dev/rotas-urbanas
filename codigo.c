#include <stdio.h>
#include <stdlib.h>

typedef struct No {
    int valor;
    struct No *esq, *dir;
} No;

No *criarNo(int valor) {
    No *novo = (No *)malloc(sizeof(No));
    novo->valor = valor;
    novo->esq = novo->dir = NULL;
    return novo;
}

No *inserir(No *raiz, int valor) {
    if (raiz == NULL) return criarNo(valor);
    if (valor < raiz->valor)
        raiz->esq = inserir(raiz->esq, valor);
    else if (valor > raiz->valor)
        raiz->dir = inserir(raiz->dir, valor);
    return raiz;
}

No *buscar(No *raiz, int valor) {
    if (raiz == NULL || raiz->valor == valor) return raiz;
    if (valor < raiz->valor) return buscar(raiz->esq, valor);
    return buscar(raiz->dir, valor);
}

No *minimo(No *raiz) {
    while (raiz->esq != NULL) raiz = raiz->esq;
    return raiz;
}

No *remover(No *raiz, int valor) {
    if (raiz == NULL) return NULL;
    if (valor < raiz->valor)
        raiz->esq = remover(raiz->esq, valor);
    else if (valor > raiz->valor)
        raiz->dir = remover(raiz->dir, valor);
    else {
        // Folha ou um filho
        if (raiz->esq == NULL) { No *t = raiz->dir; free(raiz); return t; }
        if (raiz->dir == NULL) { No *t = raiz->esq; free(raiz); return t; }
        // Dois filhos
        No *suc = minimo(raiz->dir);
        raiz->valor = suc->valor;
        raiz->dir = remover(raiz->dir, suc->valor);
    }
    return raiz;
}

void emOrdem(No *raiz) {
    if (raiz == NULL) return;
    emOrdem(raiz->esq);
    printf("%d ", raiz->valor);
    emOrdem(raiz->dir);
}

int main() {
    No *raiz = NULL;
    int vals[] = {50, 30, 70, 20, 40, 60, 80, 10, 65, 90};

    // Inserção de 10 valores
    for (int i = 0; i < 10; i++)
        raiz = inserir(raiz, vals[i]);
    printf("Arvore: "); emOrdem(raiz); printf("\n");

    // Busca existente e inexistente
    printf("Busca 40: %s\n", buscar(raiz, 40) ? "encontrado" : "nao encontrado");
    printf("Busca 99: %s\n", buscar(raiz, 99) ? "encontrado" : "nao encontrado");

    // Remoção: nó folha
    raiz = remover(raiz, 40);
    printf("Remove 40 (folha):      "); emOrdem(raiz); printf("\n");

    // Remoção: nó com um filho
    raiz = remover(raiz, 20);
    printf("Remove 20 (um filho):   "); emOrdem(raiz); printf("\n");

    // Remoção: nó com dois filhos
    raiz = remover(raiz, 70);
    printf("Remove 70 (dois filhos): "); emOrdem(raiz); printf("\n");

    return 0;
}
