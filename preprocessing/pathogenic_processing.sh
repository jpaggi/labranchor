HGMD=$1
OUT=$2

grep 'CLASS=DM;' $HGMD \
    | vcf_canonicalize /dev/stdin /dev/stdout \
    | vcf_annotate_details /dev/stdin /dev/stdout \
    | vcf_genedetails_to_semanticeffect /dev/stdin /dev/stdout > $OUT
