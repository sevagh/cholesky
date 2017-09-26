CC              ?= gcc
CFLAGS          := $(CFLAGS) -shared -Werror -Wall -O3 -lm -fPIC $(if $(filter $(CC),clang),-I/usr/lib/gcc/x86_64-redhat-linux/6.4.1/include/ -L/opt/intel/lib/intel64_lin,)
C_SRC_DIR       := ./
LIB_DIR         := ../lib
OMP_FLAGS       := $(if $(filter $(CC),clang),-fopenmp=libomp,-fopenmp)
INTEL_MKL_FLAGS := -I/opt/intel/mkl/include -L/opt/intel/mkl/lib/intel64_lin -L/opt/intel/lib/intel64_lin -L/usr/lib64/openmpi/lib -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core -lpthread $(OMP_FLAGS) -liomp5 -lscalapack

all: rosetta omp intel_mkl

libdir:
	@mkdir -p $(LIB_DIR)

intel_mkl: libdir
	@$(CC) $(CFLAGS) $(INTEL_MKL_FLAGS) $(C_SRC_DIR)/$@.c -o $(LIB_DIR)/lib$@.o

rosetta: libdir
	@$(CC) $(CFLAGS) $(C_SRC_DIR)/$@.c -o $(LIB_DIR)/lib$@.o

omp: libdir
	for openmp_src in $(wildcard $(C_SRC_DIR)/openmp*.c); do \
		$(CC) $(CFLAGS) $(OMP_FLAGS) $$openmp_src -o $(LIB_DIR)/lib`basename $${openmp_src%.c}`.o; \
	done;
