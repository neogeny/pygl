all: file_tests

file_tests:
	PYTHONPATH=. python -Oum test.parse \
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

profile_tests:
	PYTHONPATH=. python -Oum cProfile -o pygl.profile \
	-m test.parse -S \
		~/cpython/**/*.py \
		./data/* \
		./data/** \
		-i "**/cpython/**/test/data/**" \
		-i "**/cpython/**/test/bad*" \
		-i ".[a-z]*" \
		-i "test2to3" \
		-i "build" \
		-i "dist"


parser:
	python -Oum pygl -g > pygl/parser/generated.py


cparser: leg packcc

leg:
	mkdir -p gensrc
	python -Oum pygl --leg > gensrc/pgl.leg
	leg -o gensrc/pygl.c gensrc/pgl.leg
	mkdir -p bin
	gcc gensrc/pygl.c -o bin/pygl

packcc:
	mkdir -p gensrc
	python -Oum pygl --peg > gensrc/pgl.peg
	packcc -o pygl gensrc/pgl.peg
	mv pygl.* gensrc
	mkdir -p bin
	gcc gensrc/pygl.c -o bin/pygl

