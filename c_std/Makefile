CC              ?= gcc
CFLAGS          := $(CFLAGS) -shared -Werror -Wall -lm -fPIC $(if $(filter $(CC),clang),-I/usr/lib/gcc/x86_64-redhat-linux/6.4.1/include/ -L/opt/intel/lib/intel64_lin,)
C_SRC_DIR       := ./
LIB_DIR         := ../lib

all: rosetta3 rosetta0 rosetta_fastmath rosetta_softfloat

libdir:
	@mkdir -p $(LIB_DIR)

rosetta3: libdir
	@$(CC) $(CFLAGS) -O3 $(C_SRC_DIR)/rosetta.c -o $(LIB_DIR)/librosetta3.so

rosetta_fastmath: libdir
	@$(CC) $(CFLAGS) -O3 -ffast-math $(C_SRC_DIR)/rosetta.c -o $(LIB_DIR)/librosettafastmath.so

rosetta_softfloat: libdir
	@$(CC) $(CFLAGS) -O3 -msoft-float $(C_SRC_DIR)/rosetta.c -o $(LIB_DIR)/librosettasoftfloat.so

rosetta0: libdir
	@$(CC) $(CFLAGS) -O0 $(C_SRC_DIR)/rosetta.c -o $(LIB_DIR)/librosetta0.so
