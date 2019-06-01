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


parser: leg packcc

leg:
	mkdir -p src
	python -Oum pglc --leg > src/pgl.leg
	leg -o src/pglc.c src/pgl.leg
	mkdir -p bin
	gcc src/pglc.c -o bin/pglc

packcc:
	mkdir -p src
	python -Oum pglc --peg > src/pgl.peg
	packcc -o pglc src/pgl.peg
	mv pglc.* src
	mkdir -p bin
	gcc src/pglc.c -o bin/pglc

