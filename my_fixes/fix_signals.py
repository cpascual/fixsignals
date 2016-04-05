"""Migrate signals from old style to new style
"""
# Adapted from work by Juergen E. Fischer @ qgis project

# .connect( sender, signal, receiver, slot )

# Local imports
from lib2to3 import fixer_base, pytree
from lib2to3.fixer_util import Call, Name, Attr, ArgList, Node, syms

import re


class FixSignals(fixer_base.BaseFix):
    PATTERN = """
  (
  power<
    any trailer< '.' method=('connect'|'disconnect') >
    trailer<
      '('
      arglist<
        sender=any ','
        power< (any trailer< '.' 'SIGNAL' >|'SIGNAL') trailer< '(' signal=any ')' > > ','
        slot=any
      >
      ')'
    >
  >
  |
  power<
    emitter=any trailer< '.' 'emit' >
    trailer<
      '('
        args=arglist<
            power< (any trailer< '.' 'SIGNAL' >|'SIGNAL') trailer< '(' signal=any ')' > >
            ( ',' any )*
        >
      ')'
    >
  >
  |
  power<
    emitter=any trailer< '.' 'emit' >
    trailer<
      '('
        args=power< (any trailer< '.' 'SIGNAL' >|'SIGNAL') trailer< '(' signal=any ')' > >
      ')'
    >
  >
  )
"""
    SIGPATTERN = re.compile('(["\'])([^(]+)(\(.*\))?\\1')

    def match(self, node):
        results = super(FixSignals, self).match(node)

        if not results:
            return results

        try:
            signal = results.get("signal").value # attibute error if signal is a node
            signame = self.SIGPATTERN.match(signal).groups()[1] # AttributeError if not match
            results["signame"] = signame.strip()
        except AttributeError:
            print "Non trivial signal found: ", repr(node)
            return False

        return results

    def transform(self, node, results):
        # signal = results.get("signal").value
        # signame = re.sub('^["\']([^(]+)(?:\(.*\))?["\']$', '\\1', signal)
        signame = results['signame']

        if 'emitter' in results:
            emitter = results.get("emitter").clone()
            emitter.prefix = node.prefix
            args = results.get("args").clone()
            args.children = args.children[2:]
            if args.children:
                args.children[0].prefix = ''
            res = Node(syms.power, [emitter, Name('.'), Name(signame), Name('.'), Name('emit')] + [ArgList([args])])
        else:
            sender = results.get("sender").clone()
            method = results.get("method")
            if isinstance(method, list):
                method = method[0]
            method = method.clone()
            sender.prefix = node.prefix
            slot = results.get("slot").clone()
            slot.prefix = ""
            res = Node(syms.power, [sender, Name('.'), Name(signame), Name('.'), method] + [ArgList([slot])])
        return res
