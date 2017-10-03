CC              ?= gcc
CFLAGS          := $(CFLAGS) -shared -Werror -Wall -lm -fPIC $(if $(filter $(CC),clang),-I/usr/lib/gcc/x86_64-redhat-linux/6.4.1/include/ -L/opt/intel/lib/intel64_lin,)
C_SRC_DIR       := ./
LIB_DIR         := ../lib
OMP_FLAGS       := $(if $(filter $(CC),clang),-fopenmp=libomp,-fopenmp)

all: omp

libdir:
	@mkdir -p $(LIB_DIR)

omp: libdir
	for openmp_src in $(wildcard $(C_SRC_DIR)/openmp*.c); do \
		$(CC) $(CFLAGS) -O3 $(OMP_FLAGS) $$openmp_src -o $(LIB_DIR)/lib`basename $${openmp_src%.c}`.so; \
	done;
