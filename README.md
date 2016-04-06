Ugly hack to migrate old style Qt signals to new-style.
It can be used as a first step, but manual tweaking is necessary.

It is based on [code from qgis](https://github.com/qgis/QGIS/blob/master/scripts/qgis_fixes/fix_signals.py),
and adapted specifically for migrating the Taurus project (see https://sf.net/p/tauruslib/tickets/187/).

When run, it does its best in automating the migration and leaves a
SIGNALS_TODO.log with notes of identified things that need manual tweaking.

Usage:

my2to3 -f signals [options] <dir_or_file_to_fix>


For example:

my2to3 -f signals example.py

For more serious use, I recommend to use redirect the output to a file for
future reference. e.g.:

my2to3 -f signals -w ~/src/taurus/lib > signalschange.log