all: file_tests

file_tests:
	python -Oum test.parse -s  \
		~/cpython/**/*.py \
		-i "*bad*"

exitfirst_file_tests:
	python -Oum test.parse -s -x \
		~/cpython/**/*.py \
		-i "*bad*"
