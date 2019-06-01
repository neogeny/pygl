all: file_tests

file_tests:
	PYTHONPATH=. python -OOum test.parse \
		~/cpython/**/*.py \
		./data/* \
		./data/** \
		-i "**/cpython/**/test/data/**" \
		-i "**/cpython/**/test/bad*" \
		-i ".[a-z]*" \
		-i "test2to3" \
		-i "build" \
		-i "dist"


exitfirst:
	PYTHONPATH=. python -Oum test.parse -x \
		~/cpython/**/*.py \
		./data/* \
		./data/** \
		-i "**/cpython/**/test/data/**" \
		-i "**/cpython/**/test/*/bad*" \
		-i ".[a-z]*" \
		-i "build" \
		-i "dist"


parser: packcc peg

packcc:
	packcc -o pglc src/pgl.peg
	mv pglc.* src
	mkdir -p bin
	gcc -c src/pglc.c -o bin/pglc

peg:
	peg -o src/pglc.c src/pgl.peg
	mkdir -p bin
	gcc -c src/pglc.c -o bin/pglc

src/pgl.peg:
	mkdir -p src
	python -Oum pglc -c > src/pgl.peg
