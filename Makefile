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


parser:
	python -Oum pglc -g > pglc/parser/generated.py


cparser: leg packcc

leg:
	mkdir -p gensrc
	python -Oum pglc --leg > gensrc/pgl.leg
	leg -o gensrc/pglc.c gensrc/pgl.leg
	mkdir -p bin
	gcc gensrc/pglc.c -o bin/pglc

packcc:
	mkdir -p gensrc
	python -Oum pglc --peg > gensrc/pgl.peg
	packcc -o pglc gensrc/pgl.peg
	mv pglc.* gensrc
	mkdir -p bin
	gcc gensrc/pglc.c -o bin/pglc

