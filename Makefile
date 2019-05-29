all: file_tests

file_tests:
	python -OOum test.parse \
		~/cpython/*/**/**/*.py \
		./data/*/**/**/*.py \
		-i "**/cpython/**/test*/*"


exitfirst:
	python -Oum test.parse -x \
		~/cpython/*/**/**/*.py \
		./data/*/**/**/*.py \
		-i "**/cpython/**/test*/*"
