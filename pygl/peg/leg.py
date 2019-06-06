import sys

from tatsu import grammars

from . import _base
from ._base import (
    PEGCodeGenerator,
    Grammar as _Grammar,
    Choice as _Choice,
    Rule as _Rule,
)


THIS_MODULE = sys.modules[__name__]


class LEGCodeGenerator(PEGCodeGenerator):
    def __init__(self):
        super().__init__(modules=[_base, THIS_MODULE])


class Grammar(_Grammar):
    template = '''\
        %{{
           #include <stdio.h>     /* printf() */
           #include <stdlib.h>    /* atoi() */
       %}}

        {rules:::}

        %%
        int main()
        {{
             while (yyparse())
               ;
             return 0;
        }}
    '''


class Choice(_Choice):
    choice_op = '|'


class Rule(_Rule):
    choice_op = '|'

    template = '''\
        {name} = {exp:::} ;

    '''
    multiline_template = '''\
        {name} = {exp:1::}
            ;

    '''

    def render_fields(self, fields):
        if isinstance(self.exp, grammars.Choice):
            self.template = self.multiline_template
        super().render_fields(fields)
