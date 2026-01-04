#define _XOPEN_SOURCE 700
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <signal.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <time.h>
#include <stdint.h>

// --- Globals ---
int tailleTampon;

sem_t tokenProd;    // places libres pour produire
sem_t tokenConsom;  // items disponibles pour consommer
sem_t tokenAcces;   // mutex

char *bufferChiffres;

volatile sig_atomic_t flag_de_fin = 0;
int ip = 0;
int ic = 0;

int nbTotalGen = 0;
int nbTotalConsom = 0;

// --- Signal handler ---
static void alarm_set(int signum) {
    (void)signum;
    flag_de_fin = 1;
}

// --- Threads ---
void* producteur(void* pid) {
    long id = (long)pid;
    int nbGen = 0;

    for (;;) {
        // sem_wait(&tokenAcces); 
        // Problème : un producteur décrémente le sémaphore d'accès au buffer (le mutex de Temu) avant même de "savoir" s'il peut produire.
        // Alors, quand les producteurs ne peuvent plus produire, il bloquent l'accès au buffer et le programme se retrouve en deadlock (car consommateurs ne peuvent pas consommer).
        // Solution : le producteur doit d'abord être en état de produire avant d'utiliser le sémaphore Access (mutex de Dollorama) 
        sem_wait(&tokenProd);

        if (flag_de_fin) {
            sem_post(&tokenProd);
            break;
        }

        char val = '0' + rand() % 10;

        // On utilise les sémaphores uniquement pour les opérations nécéssaire (ici c'est juste utiliser le buffer)
        sem_wait(&tokenAcces); 
        bufferChiffres[ip] = val;
        sem_post(&tokenAcces);
        sem_post(&tokenConsom);

        printf("[Prod %ld] produit '%c' à pos %d\n", id, val, ip);

        nbGen++;
        nbTotalGen++;
        ip = (ip + 1) % tailleTampon;
    }

    printf("Producteur %ld a produit %d lettres\n", id, nbGen);
    return NULL;
}

void* consommateur(void* cid) {
    long id = (long)cid;
    int nbConsom = 0;

    for (;;) {
        sem_wait(&tokenConsom);
        
        // On utilise les sémaphores uniquement pour les opérations nécéssaire (ici c'est juste utiliser le buffer)
        sem_wait(&tokenAcces);
        int valeurConsom = bufferChiffres[ic];
        sem_post(&tokenAcces);
        sem_post(&tokenProd);

        printf("[Cons %ld] consomme '%c' à pos %d\n", id, (valeurConsom ? valeurConsom : '-'), ic);

        ic = (ic + 1) % tailleTampon;

        if (valeurConsom == 0) {
            break;
        }

        nbConsom++;
        nbTotalConsom++;
    }

    printf("Consommateur %ld a consommé %d lettres\n", id, nbConsom);
    return NULL;
}

// --- main ---
int main(int argc, char* argv[]) {
    if (argc < 4) {
        fprintf(stderr, "Usage: %s <nbProducteurs> <nbConsommateurs> <tailleTampon>\n", argv[0]);
        return 1;
    }

    int nProd   = atoi(argv[1]);
    int nConsom = atoi(argv[2]);
    tailleTampon = atoi(argv[3]);

    srand((unsigned)time(NULL));

    bufferChiffres = calloc((size_t)tailleTampon, sizeof(char));
    pthread_t* producteurs   = malloc((size_t)nProd   * sizeof(pthread_t));
    pthread_t* consommateurs = malloc((size_t)nConsom * sizeof(pthread_t));

    sem_init(&tokenProd,   0, (unsigned)tailleTampon);
    sem_init(&tokenConsom, 0, 0);
    sem_init(&tokenAcces,  0, 1);

    signal(SIGALRM, alarm_set);

    for (long i = 0; i < nProd; ++i) {
        pthread_create(&producteurs[i], NULL, producteur, (void*)i);
    }
    for (long i = 0; i < nConsom; ++i) {
        pthread_create(&consommateurs[i], NULL, consommateur, (void*)i);
    }

    alarm(5); // Adjust to see race conditions between producers and consumers

    while (!flag_de_fin) {
        sleep(100);
    }
    for (int i = 0; i < nProd; ++i) {
        sem_post(&tokenProd);
    }
    for (int i = 0; i < nProd; ++i) {
        pthread_join(producteurs[i], NULL);
    }

    for (int i = 0; i < nConsom; ++i) {
        sem_wait(&tokenAcces);
        sem_wait(&tokenProd);
        bufferChiffres[ip] = 0;
        printf("[Main] poison pill à pos %d\n", ip);
        ip = (ip + 1) % tailleTampon;
        sem_post(&tokenAcces);
        sem_post(&tokenConsom);
    }

    for (int i = 0; i < nConsom; ++i) {
        pthread_join(consommateurs[i], NULL);
    }

    printf("Total Consommés: %d\n", nbTotalConsom);
    printf("Total Générés:  %d\n", nbTotalGen);

    sem_destroy(&tokenProd);
    sem_destroy(&tokenConsom);
    sem_destroy(&tokenAcces);
    free(bufferChiffres);
    free(producteurs);
    free(consommateurs);

    return 0;
}