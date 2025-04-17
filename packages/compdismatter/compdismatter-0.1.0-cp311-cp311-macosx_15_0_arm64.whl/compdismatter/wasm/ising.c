#include <stdlib.h>
#include <stdio.h>
#include <math.h>

void mcmove(int *lattice, int N, double beta) {
    for (int k = 0; k < N*N; ++k) {
        int i = rand() % N;
        int j = rand() % N;
        // printf("i: %d, j: %d\n", i, j);
        int idx = i * N + j;
        int s = lattice[idx];

        int sum = lattice[((i+1)%N)*N + j] + lattice[i*N + (j+1)%N]
                + lattice[((i-1+N)%N)*N + j] + lattice[i*N + ((j-1+N)%N)];

        int cost = 2 * s * sum;
        if (cost <= 0 || ((double) rand() / RAND_MAX) < exp(-cost * beta)) {
            lattice[idx] = -s;
        }
    }
}
