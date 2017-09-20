CC              ?= clang
CFLAGS          := $(CFLAGS) -shared -Werror -Wall -O3 -lm -fPIC
C_SRC_DIR       := c
LIB_DIR         := lib
CLANG_OMP_FLAGS := -fopenmp=libomp
GCC_OMP_FLAGS   := -fopenmp
CFLAGS          := $(CFLAGS) $(if $(filter $(CC),clang), $(CLANG_OMP_FLAGS),$(GCC_OMP_FLAGS))

all: rosetta omp

rosetta:
		@mkdir -p $(LIB_DIR)
		@$(CC) $(CFLAGS) $(C_SRC_DIR)/rosetta.c -o $(LIB_DIR)/librosetta.o

omp:
		@mkdir -p $(LIB_DIR)
		for openmp_src in $(wildcard $(C_SRC_DIR)/openmp*.c); do \
			$(CC) $(CFLAGS) $$openmp_src -o $(LIB_DIR)/lib`basename $${openmp_src%.c}`.o; \
		done;

clean:
		-rm -rf lib/


.PHONY: clean
