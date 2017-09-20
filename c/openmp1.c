#include <math.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void
cholesky(double *A, double *L, int n)
{
	for (int j = 0; j < n; j++) {
#pragma omp parallel for
		for (int i = j; i < n; i++) {
			double s = 0;
			for (int k = 0; k < j; k++) {
				s += L[i * n + k] * L[j * n + k];
			}
			L[i * n + j] = (i == j) ? sqrt(A[i * n + i] - s)
			                        : (1.0 / L[j * n + j] * (A[i * n + j] - s));
		}
	}
}
