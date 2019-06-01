import sys

from . import _base
from ._base import (
    PEGCodeGenerator,
    Grammar as _Grammar,
)


THIS_MODULE = sys.modules[__name__]


class PackCCCodeGenerator(PEGCodeGenerator):
    def __init__(self):
        super().__init__(modules=[_base, THIS_MODULE])


class Grammar(_Grammar):
    template = '''\
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
