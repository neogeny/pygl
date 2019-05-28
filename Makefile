all: file_tests

file_tests:
	python -OOum test.parse -s  \
		~/cpython/**/*.py \
		~/**/tatsu/tatsu/**/*.py \
		-i "*bad*"

exitfirst:
	python -Oum test.parse -s -x \
		~/cpython/**/*.py \
		-i "*bad*"
