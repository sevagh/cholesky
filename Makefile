all: c_std c_openmp c_intel_mkl rust_rosetta

c_std:
	@make -C ./c_std

c_openmp:
	@make -C ./c_openmp

c_intel_mkl:
	@make -C ./c_intel_mkl

rust_rosetta:
	@make -C ./rust_rosetta

clean:
	-rm -rf ./lib

.PHONY: c_std c_openmp c_intel_mkl clean
