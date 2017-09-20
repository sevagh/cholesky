#include <math.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

double
inner_sum(double *li, double *lj, int n)
{
	double s = 0;
	for (int i = 0; i < n; i++) {
		s += li[i] * lj[i];
	}
	return s;
}

void
cholesky(double *A, double *L, int n)
{
	for (int j = 0; j < n; j++) {
		double s = inner_sum(&L[j * n], &L[j * n], j);
		L[j * n + j] = sqrt(A[j * n + j] - s);
#pragma omp parallel for schedule(static, 8)
		for (int i = j + 1; i < n; i++) {
			double s = inner_sum(&L[j * n], &L[i * n], j);
			L[i * n + j] = (1.0 / L[j * n + j] * (A[i * n + j] - s));
		}
	}
}
