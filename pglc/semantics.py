from .model import *  # noqa

class PGLSemantics(object):
    def grammar(self, ast):
        p, e = ast.parseinfo.pos, ast.parseinfo.endpos
        return Grammar(rules=ast.rules, pos=p, endpos=e)

    def rule(self, ast):  # noqa
        p, e = ast.parseinfo.pos, ast.parseinfo.endpos
        return Rule(name=ast.name, exp=ast.exp, pos=p, endpos=e)

    def exp(self, ast):  # noqa
        return ast

    def choice(self, ast):  # noqa
        if len(ast.choice) == 1:
            return ast.choice[0]
        p, e = ast.parseinfo.pos, ast.parseinfo.endpos
        return Choice(options=ast.choice, pos=p, endpos=e)

    def sequence(self, ast):  # noqa
        if len(ast.seq) == 1:
            return ast.seq[0]
        p, e = ast.parseinfo.pos, ast.parseinfo.endpos
        return Seq(seq=ast.seq, pos=p, endpos=e)

    def subexp(self, ast):  # noqa
        return ast

    def closure(self, ast):  # noqa
        p, e = ast.parseinfo.pos, ast.parseinfo.endpos
        if ast.ctype == '*':
            return Closure(exp=ast.closure, pos=p, endpos=e)
        else:
            return PositiveClosure(exp=ast.closure, pos=p, endpos=e)

    def atom(self, ast):  # noqa
        return ast

    def group(self, ast):  # noqa
        return ast

    def optional(self, ast):  # noqa
        p, e = ast.parseinfo.pos, ast.parseinfo.endpos
        return Optional(exp=ast.opt, pos=p, endpos=e)

    def ref(self, ast):  # noqa
        p, e = ast.parseinfo.pos, ast.parseinfo.endpos
        return Ref(name=ast.ref, pos=p, endpos=e)

    def name(self, ast):  # noqa
        return ast

    def token(self, ast):  # noqa
        p, e = ast.parseinfo.pos, ast.parseinfo.endpos
        return Token(token=ast.token, pos=p, endpos=e)
