#include <math.h>
#include <omp.h>

void
cholesky(double *A, double *L, int n)
{
	for (int j = 0; j < n; j++) {

		double s = 0;
		for (int k = 0; k < j; k++) {
			s += L[j * n + k] * L[j * n + k];
		}
		L[j * n + j] = sqrt(A[j * n + j] - s);
#pragma omp parallel for
		for (int i = j + 1; i < n; i++) {
			double s = 0;
			for (int k = 0; k < j; k++) {
				s += L[i * n + k] * L[j * n + k];
			}
			L[i * n + j] = (1.0 / L[j * n + j] * (A[i * n + j] - s));
		}
	}
}
