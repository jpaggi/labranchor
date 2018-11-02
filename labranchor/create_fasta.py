L = 70
class Genome:
    def __init__(self, fasta_fn):
        self.genome = {}
        with open(fasta_fn) as fp:
            chrom = fp.readline().strip()[1:].split(" ")[0]
            seq = ''
            for line in fp:
                if line[0] == '>':
                    self.genome[chrom] = seq
                    chrom = line.strip()[1:].split(" ")[0]
                    seq = ''
                else:
                    seq += line.strip().upper()

    def get_seq(self, chrom, start, end, strand = '+'):
        seq = self.genome[chrom][start:end]
        if strand == '-':
            seq = ''.join(map(self.revcomp, seq[::-1]))
        return seq 

    @staticmethod
    def revcomp(char):
        char = char.upper()
        if   char == 'A': return 'T'
        elif char == 'C': return 'G'
        elif char == 'G': return 'C'
        elif char == 'T': return 'A'
        assert char == 'N', "{} is not a valid base".format(char)
        return 'N'


def parse(line):
    chrom, source, feature, start, end, _, strand, _, info = line.strip().split('\t')
    info = {el.split(' ')[0].strip('"'): el.split(' ')[1].strip('"')
            for el in info.strip(';').split('; ')}
    start, end = int(start)-1, int(end) # bed coordinates
    return chrom, feature, start, end, strand, info

def read_gtf(gtf):
    coords = set()
    with open(gtf) as fp:
        for line in fp:
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
                    if strand == '+':
                        pos, three = last_exon, start
                    else:
                        three, pos = end-1, last_exon
                    coords.add((chrom, three, strand))
                if strand == '+':
                    last_exon = end
                else:
                    last_exon = start
    return list(coords)

def coords_to_fasta(coords, genome, oname):
    with open(oname, 'w') as out:
        for chrom, three, strand in coords:
            if strand == '+':
                seq = genome.get_seq(chrom, three-L, three, strand)
            else:
                seq = genome.get_seq(chrom, three+1, three+L+1, strand)
            out.write(">{}:{}:{}\n".format(chrom, three, strand))
            out.write(seq + '\n')

def gtf_to_fasta(gtf, genome, oname):
    print "Parsing gtf file at {}".format(gtf)
    coords = read_gtf(gtf)
    print coords[0]
    print "Found {} 3'ss.".format(len(coords))
    print "Loading genome fasta file from {}".format(genome)
    genome = Genome(genome)
    print "Writing output to {}".format(oname)
    coords_to_fasta(coords, genome, oname)
    print 'Success!'

if __name__ == '__main__':
    import sys
    genome, gtf, oname = sys.argv[1:]
    gtf_to_fasta(gtf, genome, oname)

