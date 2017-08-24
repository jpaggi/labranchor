# LaBrachoR (LSTM Branchpoint Retriever)

**LaBranchoR uses a LSTM network built with keras to predict the
position of RNA splicing branchpoints relative to a three prime
splice site. Precisely evaluating LaBranchoR was challenging due
to pervasive noise in the experimental data, but as we show in our
paper, we estimate that LaBranchoR correcty predicts a branchpoint
for over 90% of 3'ss.**

## Download existing branchpoint annotations

See our website linked above to download branchpoint predictions
for introns in gencode v19 (hg19) or view LaBranchoR predicted
branchpoints in the UCSC genome browser.

## Running LaBranchoR

If having to run the model yourself would stop you from using LaBranchoR,
please open an issue requesting the desired predictions or contact the
authors via email.


**All of the code and model weights needed to run LaBranchoR are available in
the 'labranchor' directory. Running LaBranchoR requires keras and numpy to be installed.**

### Predicting branchpoints

The script labranchor.py makes predictions for a fasta file of sequences upstream of
3'ss. It can be invoked with

**python labrachor.py weights 'top-bed'/'top'/'all' fasta_file output**


**weights:**
	The path to the h5 weights file (labranchor/2layer.h5)

**'top-bed'/'top'/'all':**
	top-bed: produces a bed file of predicted branchpoints. Assumes
		 fasta names are chrom:3'ss_coord:strand (ex. chr1:1000:+)
	top: reports the shift of the top scoring branchpoint from the
	     associated 3'ssfor each fasta entry
	all: reports a comma seperated list of branchpoint probabilities
	     corresponding to positions -70 to -1 from each 3'ss

**fasta_file:**
	Path to a fasta file of sequences upstream of 3'ss. Input sequences
	are required to be 70 base pairs and should not contain characters
	other than 'A', 'C', 'G', 'T', or 'N'. Any Ns will be considered A's
	during prediction.

**output:**
	Path to the output file. See the above options for formatting.

### Creating 3'ss sequence fasta files

The script create_fasta.py can be used to create fasta files suitable for
branchpoint prediction for all introns in given gtf file.

It can be invoked with:

**python create_fasta.py genome gtf output**

**genome:**
	A path to a genome fasta file consistent with the gtf file.

**gtf:**
	The path to the gtf file you wish to predict branchpoints in.

**output:**
	The path to the output fasta file.

## Analysis Included in Paper

Model training: notebooks/train_model.ipynb

Model performance: notebooks/performance_*

Cases where LaBranchoR disagrees with experimental data: notebooks/disagreement_*

Genome-wide properties and overlap with pathogenic variants: notebooks/landscape_*

Properties of C and no -2 U branchpoints: notebooks/landscape_C_and_noT.ipynb

Enrichments of ExAC variants: notebooks/ExAC_variant_enrichments.ipynb

Generation of ISM supplmentary data: notebooks/supp_data.ipynb

## Analysis not included in paper

Exploration of nucleotide importances: notebooks/importance.ipynb

Analysis of secondary structure near branchpoints: notebooks/secondary_*