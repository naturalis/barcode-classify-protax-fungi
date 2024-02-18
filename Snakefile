# Snakefile
rule split_sequences:
    input:
        backbone = 'data/backbone.fasta',
        test = 'model/Query_ID.test1.txt' # Need to figure out how to do this with each of the test text files. Perhaps make two separate rules for this?
    output:
        'model/test.fasta',
        'model/train.fasta' # reference sequences
    params:
        dependencies='requirements.txt'
    shell:
        """
        scripts/random_sequences.py 
        """

rule get_sintax_data:
    input:
        '../MDDB-phylogeny/results/thesis results/l0.2_s3_4_1500_o2.0_a1/chunks/unaligned/{chunks}.fasta',
        'model/Query_ID.test2.txt' #Change to test2 or 3 when please you, or maybe this should go automatically?
    output:
        'data/sintaxits1data.fasta'
    script:
        'scripts/get_SINTAXdata.py'

rule run_protax:
    input:
        'model/test.fasta',
        'data/sintaxits1data.fasta'
    output:
        'results/test1/query.fa'
    shell:
        """
        ODIR="/mnt/c/Users/Cathy.LAPTOP-SDFOSKVI/PycharmProjects/barcode-classify-protax-fungi/results/test1"
        ITS=its1
        cp /mnt/c/Users/Cathy.LAPTOP-SDFOSKVI/PycharmProjects/barcode-classify-protax-fungi/model/test.fasta $PWD/query.fasta
        source runprotax
        """
    # mkdir"/mnt/c/Users/Cathy.LAPTOP-SDFOSKVI/PycharmProjects/barcode-classify-protax-fungi/results"
    # mkdir"/mnt/c/Users/Cathy.LAPTOP-SDFOSKVI/PycharmProjects/barcode-classify-protax-fungi/results/test1"

# rule reference_sequences_udb:
#     input:
#         "model/train.fasta"
#     output:
#         "model/itsfull.udb"
#     shell:
#         "thirdparty/usearch10.0.240_i86linux32 -makeudb_usearch {input} -output {output}"



# rule reference_sequences_sintax:
#     input:
#         "model/train.fasta"
#     output:
#         "model/sintaxitsfull.udb"
#     shell:
#         "thirdparty/usearch10.0.240_i86linux32 -makeudb_sintax {input} -output {output}"


