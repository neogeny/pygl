all: file_tests

file_tests:
	python -um test.parse -s -x \
		~/cpython/**/*.py \
		-i "*bad*" \
		-i "*/tests/data/*" \
		-i "test*"
