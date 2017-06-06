import sys

"""
chr1HAVANAgene1186914412.+.gene_id "ENSG00000223972.4"; transcript_id "ENSG00000223972.4"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "pseudogene"; transcript_status "KNOWN"; transcript_name "DDX11L1"; level 2; havana_gene "OTTHUMG00000000961.2";
"""

def parse(line):
    chrom, source, feature, start, end, _, strand, _, info = line.strip().split('\t')
    info = {el.split(' ')[0].strip('"'): el.split(' ')[1].strip('"')
            for el in info.strip(';').split('; ')}
    start, end = int(start)-1, int(end) # bed coordinates
    return chrom, feature, start, end, strand, info

for line in sys.stdin:
    if line[0] == '#': continue
    chrom, feature, start, end, strand, info = parse(line)
    if 'gene_type' not in info or info['gene_type'] != 'protein_coding': continue
    if 'transcript_type' not in info or info['transcript_type'] != 'protein_coding': continue

    if feature == 'transcript':
        cur_transcript = info['transcript_id']
        last_exon = None

    elif feature == 'exon':
        assert info['transcript_id'] == cur_transcript
        if last_exon:
            gene_ids = ':'.join([info['gene_id'], info['transcript_id'], info['gene_name']])
            if strand == '+':
                pos, begin, stop = last_exon, start-100, start
            else:
                begin, stop, pos = end, end + 100, last_exon
            if stop > begin:
                print '\t'.join([chrom, str(begin), str(stop), gene_ids, str(pos), strand])
        if strand == '+':
            last_exon = end
        else:
            last_exon = start
