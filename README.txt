Usage:

my2to3 -f signals [options] <dir_or_file_to_fix>


For example:

my2to3 -f signals example.py

For more serious use, I recommend to use redirect the output to a file for
future reference. e.g.:

my2to3 -f signals -w ~/src/taurus/lib > signalschange.log

