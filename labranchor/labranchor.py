import numpy as np
from keras.models import load_model

L = 70
bases = ['A', 'C', 'G', 'T']

def onehot(seq):
    X = np.zeros((len(seq), len(bases)))
    for i, char in enumerate(seq):
        X[i, bases.index(char)] = 1
    return X

def encode(seqs):
    return np.vstack(onehot(seq).reshape(1, L, 4) for seq in seqs)

def read_fasta(fasta):
    names, seqs = [], []
    with open(fasta) as fp:
        first = True
        for line in fp:
            line = line.strip()
            if line[0] == '>':
                names += [line[1:]]
                if not first and len(seqs[-1]) != L:
                    print 'All sequences must have length 70.'
                    usage()
                first = False
                seqs += ['']
            else:
                line = line.upper()
                if 'N' in line: line = line.replace('N', 'A')
                seqs[-1] += line
    assert len(names) == len(seqs)
    return names, seqs

def write_best(names, preds, oname):
    with open(oname, 'w') as out:
        for name, pos, score in zip(names, np.argmax(preds, axis = 1), np.max(preds, axis = 1)):
            out.write("{}\t{}\t{}\n".format(name, pos-L, score))

def write_best_bed(names, preds, oname):
    with open(oname, 'w') as out:
        for name, pos, score in zip(names, np.argmax(preds, axis = 1), np.max(preds, axis = 1)):
            chrom, three, strand = name.split(':')
            three = int(three)
            bp = three + (pos-L) if strand == '+' else three - (pos-L)
            out.write('\t'.join(map(str, [chrom, bp, bp+1, three, score, strand])) + '\n')

def write_all(names, preds, oname):
    with open(oname, 'w') as out:
        for name, pred in zip(names, preds):
            out.write("{}\t{}\n".format(name, ','.join(map(str, pred))))

def usage():
    print "Usage: python labrachor.py <weights> <'top-bed'/'top'/'all'> <fasta_file> <output>"
    print
    print "Weights file should likely be path to '2layer.h5'"
    print "'top' returns the top scoring branchpoint per 3'ss, while 'all' gives 70 probabilities for positions -70 through -1."
    print "The fasta file should contain length 70 sequences right-aligned to a 3'ss. I.e. most should end in 'AG'."
    print "The output must be a file name, pipes are not supported."
    exit()

def predict(weights, top, fasta, oname):
    print "Loading sequences from {}".format(fasta)
    names, seqs = read_fasta(fasta)
    print "Read {} sequences".format(len(names))
    print "Loading model from {}".format(weights)
    model = load_model(weights)
    print 'Encoding sequences.'
    X = encode(seqs)
    print 'Making predictions.'
    preds = model.predict(X).reshape(-1, L)
    print "Writing predictions to {}".format(oname)
    if top == 'top-bed':
        write_best_bed(names, preds, oname)
    elif top == 'top':
        write_best(names, preds, oname)
    else:
        write_all(names, preds, oname)
    print 'Success!'
    
if __name__ == '__main__':
    import sys
    try:
        weights, top, fasta, oname = sys.argv[1:]
    except ValueError:
        usage()
        
    if top not in ['all', 'top', 'top-bed']:
        print "2nd argument must be 'all', 'top', or 'top-bed'!"
        usage()
    
    predict(weights, top, fasta, oname)
