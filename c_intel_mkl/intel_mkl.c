#include <mkl.h>
#include <mkl_scalapack.h>
#include <mkl_blacs.h>

/* Cblacs declarations */
void Cblacs_pinfo(int*, int*);
void Cblacs_get(int, int, int*);
void Cblacs_gridinit(int*, const char*, int, int);
void Cblacs_pcoord(int, int, int*, int*);
void Cblacs_gridexit(int);
void Cblacs_barrier(int, const char*);
void Cdgerv2d(int, int, int, double*, int, int, int);
void Cdgesd2d(int, int, int, double*, int, int, int);

void
cholesky(double *A, double *L, int n)
{
    int i_  = 0;
    MKL_INT info = 0;
    MKL_INT  descA[9]; 

    int ctxt, myid, myrow, mycol, numproc;
    int procrows = 2, proccols = 2;
    Cblacs_pinfo(&myid, &numproc);
    Cblacs_get(0, 0, &ctxt);
    Cblacs_gridinit(&ctxt, "Row-major", procrows, proccols);
    Cblacs_pcoord(ctxt, myid, &myrow, &mycol);

    descinit_(descA, &n, &n, &n, &n, &i_, &i_, &ctxt, &n, &info);
    pdpotrf("L", &n, A, &i_, &i_, descA, &info);
}
