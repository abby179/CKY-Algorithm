# CKY-Algorithm
The implementation of a PCFG parser using CKY Algorithm

Training data: train.dat   
Development Data: dev.dat - original trees; dev.raw - only the sentences, used as input to the parser

Usage:   
1. The CKY algorithm only accepts grammars in Chomsky Normal Form (CNF). So the first step is to transform the original trees to CNF by python3 cnf.py < infile > outfile
2. Grammar extraction by python3 pcfg.py treebankfile grammarfile
3. Parse sentences by python3 parser.py grammarfile < infile > outfile
4. Evaluate parser by python3 eval.py goldfile outfile

You should expect the F1-score of the parser to be somewhere around .65-.75.

