"""
This is meant to serve as a wrapper for MaxEntScan.

The perl scripts and data files were downloaded from:
http://genes.mit.edu/burgelab/maxent/download/.

Command semantics are:
  perl score5.pl fn5
  perl score3.pl fn3

  Here fn5 is \n separated
    9mers with 3 bases in the intron.
  fn3 is 23mers with 3 bases in the intron.

The main possible improvement to this tool
would be to provide an updated data set,
but I'm sure there is some subtlety in
getting this right.
"""
from subprocess import Popen, PIPE, STDOUT
import numpy as np

def maxentscan(seqs, five, BATCH = 10000):
    script = 'MaxEntScan/'
    script += 'score5.pl' if five else 'score3.pl'
    
    scores = []
    begin, end = 0, BATCH
    while end - BATCH < len(seqs):
        p = Popen(['perl', script, '-'], stdout=PIPE, stdin=PIPE)
        scores += [np.array(map(lambda x: float(x.split('\t')[1]),
                            p.communicate(input = '\n'.join(seqs[begin:end]))[0].split('\n')[:-1]))]
        begin = end
        end = end + BATCH
    return np.hstack(scores)
