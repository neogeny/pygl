all: file_tests

file_tests:
	python -OOum test.parse \
		./data/*/**/**/*.py \
		-i "**/cpython/**/test/*"

exitfirst:
	python -Oum test.parse -x \
		./data/*/**/**/*.py \
		-i "**/cpython/**/test/*"
