import sys

from tatsu import grammars
from tatsu.codegen import ModelRenderer
from tatsu.codegen import CodeGenerator

THIS_MODULE = sys.modules[__name__]


class PEGCodeGenerator(CodeGenerator):
    def __init__(self):
        super().__init__(modules=[THIS_MODULE])


class Any(ModelRenderer):
    template = '.'


class BasedRule(ModelRenderer):
    template = 'ERROR'


class Choice(ModelRenderer):
    template = '{options:: / :}'


class Closure(ModelRenderer):
    template = '({exp})*'


class Comment(ModelRenderer):
    template = ''


class Constant(ModelRenderer):
    template = '{literal}'


class Cut(ModelRenderer):
    template = ''


class EOF(ModelRenderer):
    template = '!.'


class EOLComment(Comment):
    template = ''


class EmptyClosure(ModelRenderer):
    template = '()*'


class Fail(ModelRenderer):
    template = '!()'


class Gather(ModelRenderer):
    template = '{exp} ({sep} {exp})*'


class Grammar(ModelRenderer):
    packcc_template = '''\
    %prefix '{name}'

    %header {{
    }}

    %source {{
    }}

    {rules:::}

    %%

    int main() {{
        int ret;
        {name}_context_t *ctx = {name}_create(NULL);
        while ({name}_parse(ctx, &ret));
        {name}_destroy(ctx);
    }}
    '''

    template = '{rules:::}'

    def render_fields(self, fields):
        super().render_fields(fields)
        fields.update(
            name='pglc',
            rules=self.node.used_rules(),
        )


class Group(ModelRenderer):
    template = '({exp})'


class Join(ModelRenderer):
    template = '{exp} ({sep} {exp})*'


class LeftJoin(ModelRenderer):
    template = '{exp} ({sep} {exp})*'


class Lookahead(ModelRenderer):
    template = '&{exp}'


class Named(ModelRenderer):
    # template = '{name}:{exp}'
    template = '{exp}'


class NamedList(Named):
    # template = '{name}:{exp}'
    template = '{exp}'


class NegativeLookahead(ModelRenderer):
    template = '!{exp}'


class Optional(ModelRenderer):
    template = '({exp})?'


class Override(Named):
    # template = '{name}:{exp}'
    template = '{exp}'


class OverrideList(NamedList):
    # template = '{name}:{exp}'
    template = '{exp}'


class Pattern(ModelRenderer):
    template = '{regex}'

    def render_fields(self, fields):
        super().render_fields(fields)
        fields.update(regex=repr(self.regex.pattern))


class PositiveClosure(Closure):
    template = '({exp})*'


class PositiveGather(Gather):
    template = ''


class PositiveJoin(ModelRenderer):
    template = ''


class RightJoin(ModelRenderer):
    template = ''


class Rule(ModelRenderer):
    template = '''\
    {name} <- {exp}

    '''

    def render_fields(self, fields):
        super().render_fields(fields)
        exp = self.exp
        if isinstance(exp, grammars.Choice):
            n = len(self.name) + 2
            exp = ('\n' + n * ' ' + '/ ').join(
                self.get_renderer(o).render() for o in exp.options
            )
            fields.update(exp=exp)


class RuleInclude(ModelRenderer):
    template = ''


class RuleRef(ModelRenderer):
    template = '{name}'


class Sequence(ModelRenderer):
    template = '{sequence:: :}'


class SkipTo(ModelRenderer):
    template = ''


class Special(ModelRenderer):
    template = ''


class Token(ModelRenderer):
    template = '{token}'

    def render_fields(self, fields):
        super().render_fields(fields)
        fields.update(token=repr(self.token))


class Void(ModelRenderer):
    template = '(&.)?'
