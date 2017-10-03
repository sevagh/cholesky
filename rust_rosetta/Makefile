all: librosetta_cholesky_rs

librosetta_cholesky_rs:
	@cargo build --release
	@cp $(CURDIR)/target/release/librosetta_cholesky_rs.so ../lib
