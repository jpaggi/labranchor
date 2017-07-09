# Run branchpointer for test set (Chr1) and dump to file.

library(branchpointer)

library(BSgenome.Hsapiens.UCSC.hg19)
genome <- BSgenome.Hsapiens.UCSC.hg19::BSgenome.Hsapiens.UCSC.hg19
exons <- gtfToExons("../anno/gencode.v19.annotation.gtf")

queryIntron <- readQueryFile('../anno/test_taggart.tsv', queryType = "region")

queryIntron <- getQueryLoc(queryIntron,queryType="region",
                           exons = exons)

branchpointPredictionsIntron <- predictBranchpoints(queryIntron,
                                                    queryType = "region",
                                                    BSgenome = genome)

write(branchpointPredictionsIntron$branchpoint_prob, '../anno/branchpointer.taggart.score.tsv', sep = '\t')
write(branchpointPredictionsIntron$test_site, '../anno/branchpointer.taggart.pos.tsv', sep = '\t')