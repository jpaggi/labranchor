import sys
#from genome import Genome

#genome = Genome('splicing_classifier/data/raw/hg19.fa')

bases = ['A', 'C', 'G', 'T']
for line in sys.stdin:
    if line[0] == '#': continue
    line = line.strip().split('\t')
    if line[16] != 'GRCh37': continue        # Assembly
    if line[6] != 'Pathogenic': continue     # Pathogenic

    chrom, start, stop, ref, alt = line[18:23]
    if chrom == 'MT': continue

    ID = line[0]

    if alt not in bases or ref not in bases:
        continue
    print '\t'.join([chrom, start, line[0], ref, alt, '.', '.', '.'])
