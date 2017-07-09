import pandas
import sys

def proc_parens(L):
    O = []
    for l in L:
        if l[0] == '(':
            l = l[1:]
        if l[-1] == ')':
            l = l[:-1]
        O += [int(l)]
    return O

t = pandas.read_excel(sys.argv[1])
branchpoints = {}


for chrom, pos, strand, motif, bps, total, unique, mutant, unique_mutant, source in zip(t['CHROM'], t['POS'], t['strand'],
                                                                                        t['Motif Model'], t['bps'],
                                                                                        t['total'], t['unique'],
                                                                                        t['mutant'], t['unique_mutant'],
                                                                                        t['RNAseq Source']):
    if 'Mattick' in source: continue
    if motif in ['transcript_switching', 'circle']: continue
    split = lambda x: str(x).split(',')
    total, unique, mutant, unique_mutant = split(total), split(unique), split(mutant), split(unique_mutant)
    assert len(total) == len(unique) == len(mutant) == len(unique_mutant)

    idx1 = [i for i, count in enumerate(total) if count[0] == '(']
    idx2 = [i for i, count in enumerate(total) if count[-1] == ')']

    if not idx1:
        assert not idx2, total
        assert len(total) == 1
        idx1, idx2 = 0, 0
    else:
        assert len(idx1) == len(idx2) == 1
        idx1, idx2 = idx1[0], idx2[0]
        assert idx2 - idx1 <= 2, "More than 3 nucleotides bulged."

    if idx2 - idx1:
        bp = idx2 #idx1 + bps.split('(')[-1].split(')')[0].index('*') - 1
        assert bp <= idx2
    else:
        bp = idx1

    for i, (t, u, m, u_m) in enumerate(zip(*map(proc_parens, [total, unique, mutant, unique_mutant]))):
        shift = i - bp
        coord = pos + (shift if strand == '+' else - shift)
        key = (chrom, coord, strand)
        branchpoints[key] = (t, u, m, u_m)
        
for (chrom, pos, strand), reads in branchpoints.items():
    if reads[2]:
        print '\t'.join([chrom, str(pos), str(pos+1), ','.join(map(str,reads)), '.', strand])
