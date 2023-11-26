all: parser

parser:
	python -Om pygl > pygl/parser/generated.py
