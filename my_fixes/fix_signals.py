"""Migrate signals from old style to new style
"""
# Adapted by Carlos Pascual-Izarra @cells.es
# from work by Juergen E. Fischer @ qgis project
#
# DISCLAIMER: this adaptation is EXTREMELY fragile, and focused on the
#             coding style found in Taurus. It does not intend to cover all
#             cases.


# Local imports
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, ArgList, Node, syms

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
        (power< (any trailer< '.' 'SIGNAL' >|'SIGNAL') trailer< '(' signal=any ')' > > | sigobj=any) ','
        slot=any
      >
      ')'
    >
  >
  |
  power<
    emitter=(any (trailer< '.' any>)*) trailer< '.' 'emit' >
    trailer<
      '('
        args=arglist<
            (power< (any trailer< '.' 'SIGNAL' >|'SIGNAL') trailer< '(' signal=any ')' > > | sigobj=any)
            sigarg=(( ',' any )*)
        >
      ')'
    >
  >
  |
  power<
    emitter=(any (trailer< '.' any>)*) trailer< '.' 'emit' >
    trailer<
      '('
        args=power< (any trailer< '.' 'SIGNAL' >|'SIGNAL') trailer< '(' signal=any ')' > >
      ')'
    >
  >
  |
  power<
    emitter=(any (trailer< '.' any>)*) trailer< '.' 'emit' >
    trailer<
      '('
        sigobj=any
      ')'
    >
  >
  )
"""
    SIGPATTERN = re.compile('(["\'])([^(]+)(\(.*\))?\\1')

    def __init__(self, *args, **kwargs):
        r = super(FixSignals, self).__init__(*args, **kwargs)
        self._siglog = file('SIGNALS_TODO.log','w')
        self._knownsigs = set()
        return r

    def _findClassName(self, node):
        n=node
        while n is not None and n.type != syms.classdef:
            n=n.parent
        leaves = n.leaves()
        leaves.next()
        l = leaves.next()
        return str(l)

    def match(self, node):
        results = super(FixSignals, self).match(node)

        if not results:
            return results

        try:
            if 'sigobj' in results and results['sigobj']:
                raise AttributeError
            # next line raises AttributeError if signal is a node
            signal = results.get("signal").value
            # next line raises AttributeError if not match
            signame = self.SIGPATTERN.match(signal).groups()[1]
            results["signame"] = signame.strip()
        except AttributeError:
            print "\nSKIPPING non trivial signal:\n%s\n" % node
            self._siglog.write("NOT_CONVERTED:\n %s\n\n" % node)
            return False

        if 'emitter' in results:
            e = ''.join(map(str, results.get("emitter")))
            cls = self._findClassName(node)
            if (cls,e,signame) not in self._knownsigs:
                self._knownsigs.add((cls,e,signame))
                self._siglog.write("NEEDS_DECLARE:\n %s: %s.%s\n\n" % (cls, e, signame))

        return results

    def transform(self, node, results):
        signame = results['signame']

        if 'emitter' in results:
            emitter = results.get("emitter")
            emitter = Name(''.join(map(str, emitter)))

            if 'sigarg' in results:
                args = results.get("args").clone()
                args.children = args.children[2:]
                if args.children:
                    args.children[0].prefix = ''
                res = Node(syms.power, [emitter, Name('.'), Name(signame), Name('.'), Name('emit')] + [ArgList([args])])
            else:
                res = Node(syms.power, [emitter, Name('.'), Name(signame), Name('.'), Name('emit()')])

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
