import sys

bps = {}
for line in sys.stdin:
    if line[0] == 'B': continue
    chrom, pos, strand, model = line.split(',')[:4]
    if model in ['circle', 'template_switching', 'none']: continue
    key = (chrom, pos, strand)
    if key in bps: continue
    bps[key] = ','.join(line.strip().split(',')[3:])

for (chrom, pos, strand), quality in bps.items():
    print '\t'.join([chrom, pos, str(int(pos)+1), quality, '.', strand])
