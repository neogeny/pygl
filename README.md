# **pglc**

**pglc** (for Python Grammar Language compiler) is one of the projects exploring ides to
[Switch Python’s parsing tech to something more powerful than LL(1)](https://discuss.python.org/t/switch-pythons-parsing-tech-to-something-more-powerful-than-ll-1/379/56).

The main objective of the project is to produce a PEG grammar for Python, so different PEG parser generators can be tested as parsing technologies for Python. The tool used to bootstrap the process is [TatSu](https://tatsu.readthedocs.io) (currently, **pglc** requires the unreleased [master version](https://github.com/neogeny/TatSu))

The strategy used in **pglc** is explained on [this topic](https://discuss.python.org/t/preparing-for-new-python-parsing/1550/38) on [Python's Discourse site].

**pglc** is a tool that takes the Python grammar (`Grammar/Grammar`) in the source and generates a Python->AST translator.

## Testing

To run the current state of things:

```bash
$ pip install -r requirements-dev.pip
$ pytest
```
