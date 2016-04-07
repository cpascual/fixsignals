Intro
-----

This project provides a fixer plugin for the lib2to3 module
to migrate old style Qt signals to new-style ones.

**Warning:** this is an ugly hack. Mostly for use in converting the taurus project signals 
(see https://sf.net/p/tauruslib/tickets/187/).
The fixer can be invoked with the provided 'my2to3' script.

`my2to3 -f signals` can be used as a first step, but manual tweaking is necessaryin the fixer code.

It is based on [code from qgis](https://github.com/qgis/QGIS/blob/master/scripts/qgis_fixes/fix_signals.py)

When run, it does its best in automating the migration and leaves a
`SIGNALS_TODO.log` file with notes of identified things that need manual tweaking.

Usage
-----

`my2to3 -f signals [options] <dir_or_file_to_fix>`

Use`my2to3 -h` for info on available options inherited from `2to3`


For example:

`my2to3 -f signals -w example.py`

When converting a full package instead of a small file, I recommend to redirect the output to a file for
future reference. e.g.:

`my2to3 -f signals -w ~/src/taurus/lib > signalschange.log`


Example
-------

Now let's see an example. Consider the following code from the example.py:

~~~~
from PyQt4 import Qt

MY_SIGNATURE = 'some_signal_name'
MY_SIG = Qt.SIGNAL('some_other_signal_name')

class MyWidget(Qt.QWidget):

    def m1(self):
        self.connect(self, Qt.SIGNAL('mysigname'), self.myslot)
        self.emit(Qt.SIGNAL('mysigname'), 1, 2)

    def m2(self):
        self.connect(self, Qt.SIGNAL(MY_SIGNATURE), self.myslot)
        self.emit(Qt.SIGNAL(MY_SIGNATURE), 3, 4)

    def m3(self):
        self.connect(self, MY_SIG, self.myslot)
        self.emit(MY_SIG, 5, 6)

    def myslot(self, a, b):
        print a, b, a + b
~~~~

If we run the script with:

`my2to3 -f signals -nwo outdir example.py`

We get the following transformed `outdir/example.py` file :

~~~~
from PyQt4 import Qt

MY_SIGNATURE = 'some_signal_name'
MY_SIG = Qt.SIGNAL('some_other_signal_name')

class MyWidget(Qt.QWidget):

    def m1(self):
        self.mysigname.connect(self.myslot)
        self.mysigname.emit(1, 2)

    def m2(self):
        self.connect(self, Qt.SIGNAL(MY_SIGNATURE), self.myslot)
        self.emit(Qt.SIGNAL(MY_SIGNATURE), 3, 4)

    def m3(self):
        self.connect(self, MY_SIG, self.myslot)
        self.emit(MY_SIG, 5, 6)

    def myslot(self, a, b):
        print a, b, a + b
~~~~

Now, note that there are several things that still need manual fixing:

- The `mysigname` signal needs to be declared. We need to add a class member like
  ~~~~
  mysigname = Qt.pyqtSignal(int, int)
  ~~~~
  Note that the types need to be inferred from studying the code if the signal
  signature does not include them. Looking at the emit parameters and the slot code may help.

- The emit and connects from methods m2 and m3 are not transformed at all.
  This is because there is no safe way to deal with the possible indirections in all cases.
  Just transform them manually.

These pending things are logged in a file called 'SIGNALS_TODO.log'. In this case, the log looks as follows:

~~~~
NEEDS_DECLARE:
  MyWidget:         self.mysigname

NOT_CONVERTED:
 self.connect(self, Qt.SIGNAL(MY_SIGNATURE), self.myslot)

NOT_CONVERTED:
         self.emit(Qt.SIGNAL(MY_SIGNATURE), 3, 4)

NOT_CONVERTED:
 self.connect(self, MY_SIG, self.myslot)

NOT_CONVERTED:
         self.emit(MY_SIG, 5, 6)

~~~~

Finally, note that the stdout has interesting info

~~~~
$ ./my2to3 -f signals -nwo outdir example.py
lib2to3.main: Output in 'outdir' will mirror the input directory '' layout.
root: Generating grammar tables from /usr/lib/python2.7/lib2to3/PatternGrammar.txt

SKIPPING non trivial signal:
self.connect(self, Qt.SIGNAL(MY_SIGNATURE), self.myslot)


SKIPPING non trivial signal:
        self.emit(Qt.SIGNAL(MY_SIGNATURE), 3, 4)


SKIPPING non trivial signal:
self.connect(self, MY_SIG, self.myslot)


SKIPPING non trivial signal:
        self.emit(MY_SIG, 5, 6)

RefactoringTool: Refactored example.py
--- example.py  (original)
+++ example.py  (refactored)
@@ -6,8 +6,8 @@
 class MyWidget(Qt.QWidget):
 
     def m1(self):
-        self.connect(self, Qt.SIGNAL('mysigname'), self.myslot)
-        self.emit(Qt.SIGNAL('mysigname'), 1, 2)
+        self.mysigname.connect(self.myslot)
+        self.mysigname.emit(1, 2)
 
     def m2(self):
         self.connect(self, Qt.SIGNAL(MY_SIGNATURE), self.myslot)
RefactoringTool: Writing converted example.py to outdir/example.py.
RefactoringTool: Files that were modified:
RefactoringTool: example.py


~~~~