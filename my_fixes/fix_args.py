"""Migrate QString `.arg` to python string `.format`
"""
# Written by Matteo Bertini <naufraghi@develer.com>

# Local imports
from lib2to3 import fixer_base
from lib2to3.fixer_util import Comma, ArgList, Node, String, Name, Dot, Leaf, syms

# I've not found a way to match multiple tr("...").arg(v1).arg(v2)
# so here we generate a finite matcher, with a plausible number
# of arguments (order counts, longer matchers must come first).
N_ARGS = 5

def gen_args(n):
    pattern = "trailer< '.' 'arg' > trailer< '(' arg%d=any ')' >"
    args = []
    for i in range(n):
        args.append(" ".join((pattern % (j+1)) for j in range(n - i)))
    return "(\n  %s\n)" % "\n | ".join(args)


class FixArgs(fixer_base.BaseFix):
    PATTERN = """
    power<
      before=any*
      tr=('tr' | 'translate') trailer< '(' message=any ')' >
      {args}
      rest=any*
    >
    |
    power<
      before=any*
      tr=trailer< '.' ('tr' | 'translate') > trailer< '(' message=any ')' >
      {args}
      rest=any*
    >
    """.format(args=gen_args(N_ARGS))
    def transform(self, node, results):
        # before
        before = [b.clone() for b in results['before']]
        # tr | translate
        tr = results['tr']
        new_tr = [(tr[0] if isinstance(tr, list) else tr).clone()]
        # message
        message = results['message'].clone()
        for ch in (message.pre_order() if not isinstance(message, Leaf) else [message]):
            if isinstance(ch, Leaf):
                for i in range(N_ARGS):
                    # %1 -> {0}, ...
                    ch.value = ch.value.replace("%{0}".format(i+1), "{%d}" % i)
        new_tr += [ArgList([message])]
        # format
        def format_args():
            for key in sorted(results):
                if key.startswith('arg'):
                    arg = results[key]
                    if isinstance(arg, list):
                        for a in arg:
                            yield a.clone()
                    else:
                        yield arg.clone()
                    yield Comma()
                    yield String(' ')
                                                        # Skip last Comma, String
        new_format = [Dot(), Name('format'), ArgList(list(format_args())[:-2])]
        # rest
        rest = [r.clone() for r in results['rest']]
        # new node
        new = Node(syms.power, before + new_tr + new_format + rest)
        new.prefix = node.prefix
        new.parent = node.parent
        return new
