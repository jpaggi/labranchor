CLINVAR=$1
OUT=$2

cat $CLINVAR \
    | python clinvar.py \
    | sort -k1,2 -V \
    | vcf_canonicalize /dev/stdin /dev/stdout \
    | vcf_annotate_details /dev/stdin /dev/stdout \
    | vcf_genedetails_to_semanticeffect /dev/stdin /dev/stdout > $OUT
