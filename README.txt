To run the code, use 'python main.py' with one or two command line arguments.

This code was developed on Ubuntu 14.04.4 LTS and its default python verion (2.7.x) is the most compatible.

Execution requires two files: attribute file, a simple text file containing the name and domain of each attribute, and training file, a simple text file containg any number of lines, each line having one value for each of the attributes described in the attribute file. An attribute's domain may be a sequence with all possible values or the word continuous for real numbers.

A single argument, name, means attribute file and training file are, respectively, name-attr.txt and name.txt.
Two arguments specify the names for attribute and training file, respectively.

main.py contains treats the command line arguments, reads the necessary files, reads the two necessary minimums from stdin, calls associate and displays the output.
build.py contains contains associate's implementation and the implementation of every helper function it uses.	
