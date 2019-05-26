# **pglc**

**pglc** (for Python Grammar Language compiler) is one of the projects exploring ideas to
[Switch Python’s parsing tech to something more powerful than LL(1)](https://discuss.python.org/t/switch-pythons-parsing-tech-to-something-more-powerful-than-ll-1/379/56).

The main objective of the project is to produce a PEG grammar for Python, so different PEG parser generators can be tested as parsing technologies for Python. The tool used to bootstrap the process is [TatSu](https://tatsu.readthedocs.io) (currently, **pglc** requires the unreleased [master version](https://github.com/neogeny/TatSu))

The strategy used in **pglc** is explained on [this topic](https://discuss.python.org/t/preparing-for-new-python-parsing/1550/38) on [Python's Discourse site](https://discuss.python.org/c/ideas).

## Project Plan

Currently, the TatSu PEG grammar for Python is being debugged against the Python source code in in the [CPython Git repository](https://github.com/python/cpython) (~ 787 KLOC).

These are the steps of the plan:

> **NOTE**: In what follows _PackCC_ may actually be `apt install peg`, or some other PEG->C parser generator that is maintained, and generates _C_. _PackCC_ was initially chosen because it was feature-complete, and self-contained, but it lacks a maintainer, and may not be fully debugged.

1. ✓ Create a TatSu parser to parse `Grammar/Grammar`
1. ✓ Parse the `Grammar/Grammar` using the above parser
1. ✓ Generate a draft PEG grammar for Python from the above using TatSu
1. ✓ Debug the PEG grammar using TatSu (PEG semantics require rule-choice ordering, etc.). The grammar is currenly good for parsing 126 KLOC of Python in `cpython/**/*.py`.
1. ⇒ Integrate the Python tokenizer using the `token` and `tokenize` modules.
1. Generate AST from Python source using the above (at this point, the grammar is debugged and the parser complete)
1. Measure parser performance (it should be within the expected Python vs C range). Pass, or abort
1. Automatically generate a [PackCC](https://github.com/apalala/packcc) grammar for Python from the above
1. Debug the PackCC grammar
1. Ditch TatSu
1. Instrument the PackCC grammar to generate AST (as TatSu, PackCC allows naming parse subexpressions)
1. Measure, and pass or abort
1. Customize PackCC and the PackCC grammar so it is `libpython` compatible (PackCC provides for this).
1. Add a node visitor to translate the PackCC grammar to "documentation grammar".
1. The current Python parser can be replaced by a PEG parser that is easy to maintain and covers source->AST.

## Testing

To run the current state of things:

```bash
$ pip install -r requirements-dev.pip
$ pytest
```

To run the tests over `cpython/**/*.py` using all CPU cores, just type:

```bash
$ make
```

See the `Makefile` or type this for options:

```bash
python -m test.parse -h
```
