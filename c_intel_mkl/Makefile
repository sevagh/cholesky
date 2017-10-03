CC              ?= gcc
CFLAGS          := $(CFLAGS) -shared -Werror -Wall -lm -fPIC $(if $(filter $(CC),clang),-I/usr/lib/gcc/x86_64-redhat-linux/6.4.1/include/ -L/opt/intel/lib/intel64_lin,)
C_SRC_DIR       := ./
LIB_DIR         := ../lib
OMP_FLAGS       := $(if $(filter $(CC),clang),-fopenmp=libomp,-fopenmp)
INTEL_MKL_FLAGS := -I/opt/intel/mkl/include -L/opt/intel/mkl/lib/intel64_lin -L/opt/intel/lib/intel64_lin -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_scalapack_lp64 -lmkl_core -lmkl_blacs_openmpi_lp64 -L/usr/lib64/openmpi/lib -lpthread -liomp5 $(OMP_FLAGS) -lmpi

all: intel_mkl

libdir:
	@mkdir -p $(LIB_DIR)

intel_mkl: libdir
	@$(CC) $(CFLAGS) -O3 $(INTEL_MKL_FLAGS) $(C_SRC_DIR)/$@.c -o $(LIB_DIR)/lib$@.so
