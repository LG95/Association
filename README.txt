To run the code, use 'python main.py' with one or two command line arguments.
A single argument, name, means attribute file and training file are, respectively, name-attr.txt and name.txt.
Two arguments specify the names for attribute and training file, respectively.

main.py contains treats the command line arguments, reads the necessary files, reads the two necessary minimums from stdin, calls associate and displays the output.
build.py contains contains associate's implementation and the implementation of every helper function it uses.	