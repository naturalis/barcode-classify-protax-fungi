# 1) user creates $ODIR and copies input sequence 'query.fa' there before running this script
# 2) Shell variable ITS needs to be defined to be either its1, its2, or itsfull. It defines the model and
# reference sequences \to be used.

# get working directory
PWD=$(pwd)

# Command line arguments, RUNID = Test no., ITS = its1/its2/itsfull and PERCENT = (confidence) threshold for the prediction to become a result
RUNID=$1
ITS=$2
PERCENT=$3

ODIR="$PWD/userdir" # Output data directory
INSEQ=$ODIR/test_test.fasta #test data fasta file
THRESHOLD=$PERCENT/100

# Let User know if the query file is missing
if [ ! -e $INSEQ ]; then
 echo "ERROR: test.fasta not in ODIR ($ODIR)"
 return 1
fi

# Tell User they need to specify either its1, its2 or itsfull as their second argument
if [ "$ITS" != "its1" ] && [ "$ITS" != "its2" ] && [ "$ITS" != "itsfull" ]; then
 echo "ERROR: ITS must be either its1, its2, or itsfull (was '$ITS')"
 return 1
fi


# Locations for PROTAX and database files
PROTAXDIR=$PWD                    # Directory Path that has files to run PROTAX (e.g. this one)
PROTAX=$PROTAXDIR/protaxscripts   # Directory Path to PROTAX scripts
MDIR="$PWD/db_files_TU-NHM"       # Directory Path to db_files, which has udb, taxonomy, rseqs, ref.tax and parameter files
THIRDPARTY=$PROTAXDIR/thirdparty  # Directory Path to thirdparty applications, e.g. usearch and krona

# Locations for OUTPUT files of PROTAX and SINTAX
SIMFILE1=$ODIR/query.m8           # Output Directory PROTAX
OUTSINTAX=$ODIR/query.sintax      # Output Directory Sintax
SIMFILE2=$ODIR/query.sasintax     # Output Directory Sintax

grep '^>' $INSEQ | cut -c2- > $ODIR/query.ids       # Removes the > from the headers and returns it to query.ids


# Uses the usearch_global command to search the -db for high-identity hits (maxaccepts) according to the USEARCH algorithm
# Outputs 1000 hits into ODIR/query.m8
$THIRDPARTY/vsearch -usearch_global $INSEQ -db $MDIR/${ITS}.udb -id 0.75 -maxaccepts 1000 -strand both -userfields query+target+id -userout $SIMFILE1
# USEARCH global algorithm works in the following way:
# The algorithm searches a database for high-identity hits on the maxaccepts number of database sequences.
# USEARCH uses a k-mer approach. Utilizing the fact that sequences that are similar often have short words in common.
# It does not estimate the sequence identity from the number of matching kmers. It uses word count to prioritize the db search.
# Accepts/hits are above the (-id) threshold, rejects below.

# Uses the -sintax command and algorithm search the -db and output in query.sintax
$THIRDPARTY/vsearch -sintax $INSEQ -db $MDIR/sintax${ITS}.udb -tabbedout $OUTSINTAX -strand both
# SINTAX algorithm works similarly to the RDP classifier. However, there is no need for training.
# The top taxonomy is identified by k-mer similarity

# Changes query.sintax format (d: is 1, s: is 7) and redirects result into query.sasintax, checking for each sequence if the tax result is found in taxonomy.ascii7
perl $PROTAX/sintax2sa.pl $MDIR/taxonomy.ascii7 $OUTSINTAX > $SIMFILE2

grep '^>' $INSEQ | cut -c2- > $ODIR/query.ids  # Removes the > from the headers and returns it to query.ids

# perl $PROTAX/testsample2init.pl {startnode} {input} > {output}
perl $PROTAX/testsample2init.pl 1 $ODIR/query.ids > $ODIR/query1.logprob # grabs IDs and startnode from query.ids to create query.logprob. The next loop expands by making query{LEVEL}.logprobs

# parent probs from previous level classification
for LEVEL in 2 3 4 5 6 7 # for each level in taxonomy
do
 echo "LEVEL $LEVEL"
 PREVLEVEL=$((LEVEL-1))
 IFILE=$ODIR/query${PREVLEVEL}.logprob # input file: previous level, it build on previously made classifications and probabilities
 OFILE=$ODIR/query${LEVEL}.logprob # output file: current level, adds new probabilities
 # classify.pl classifying algorithm for assigning taxonomic labels, computes probabilities for each sequence
 perl $PROTAX/classify.pl "$IFILE" $MDIR/tax$LEVEL $MDIR/ref.tax$LEVEL $MDIR/rseqs$LEVEL $MDIR/params.${ITS}.level${LEVEL} $SIMFILE1 $SIMFILE2  0 .01 $OFILE 0
done

######### Krona #########

perl $PROTAX/fastalensize.pl $INSEQ > $ODIR/query.lensize

# if sequences do not represent clusters, clustersize file (text file with lines: seqid clustersize) can be replaced by '-'

perl $PROTAX/protaxlogprob2kronaxml.pl $THRESHOLD Fungi $MDIR/taxonomy $ODIR/query.lensize $ODIR/query[1,2,3,4,5,6,7].logprob > $ODIR/krona.xml

# export PATH=$PATH:$PROTAX/thirdparty/krona/bin
$THIRDPARTY/krona/bin/ktImportXML.pl -o "$ODIR"/krona.html "$ODIR"/krona.xml

###################
# .logprob files contain list of node ids and logprobs, convert node ids to taxonomic names and logprobs to probs
# NOTE: for final output, we can add information from best matching reference sequences etc., this is just example

for LEVEL in 2 3 4 5 6 7
do
 perl $PROTAX/nameprob.pl $MDIR/taxonomy $ODIR/query${LEVEL}.logprob > $ODIR/query${LEVEL}.nameprob
done

INFILE="source_$RUNID"
cp $PROTAXDIR/README.txt "$ODIR"

#zip "$INFILE.zip" README.txt krona.html krona.xml query2.logprob query3.logprob query4.logprob query5.logprob query6.logprob query7.logprob query.fa query.lensize query.sasintax query2.nameprob query3.nameprob query4.nameprob query5.nameprob query6.nameprob query7.nameprob query.ids query.m8 query.sintax
pushd "$PWD/userdir/"
zip "../outdata/$INFILE.zip" /*
popd
