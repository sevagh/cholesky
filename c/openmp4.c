#include <math.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void
cholesky(double *A, double *L, int n)
{
	for (int i = 0; i < n; i++) {
		double s = 0;
		for (int k = 0; k < i; k++) {
			s += L[k * n + i] * L[k * n + i];
		}
		L[i * n + i] = sqrt(A[i * n + i] - s);
#pragma omp parallel for
		for (int j = i + 1; j < n; j++) {
			double s = 0;
			for (int k = 0; k < i; k++) {
				s += L[k * n + i] * L[k * n + j];
			}
			L[i * n + j] = (1.0 / L[i * n + i] * (A[i * n + j] - s));
		}
	}
}
