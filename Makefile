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


packcc:
	mkdir -p src
	python -Oum pglc -c > src/pgl.peg
	packcc -o pglc src/pgl.peg
	mv pglc.* src
	mkdir -p bin
	gcc -o bin/pglc src/pglc.c
