# Snakefile

rule split_sequences:
    input:
        backbone = 'data/backbone.fasta',
        test = 'model/Query_ID.test3.txt' # Need to figure out how to do this with each of the test text files. Perhaps make two separate rules for this?
    output:
        'userdir/query.fasta',
        'model/train.fasta' # reference sequences
    params:
        dependencies='requirements.txt'
    shell:
        """
        python scripts/random_sequences.py
        """

rule get_sintax_data:
    input:
        '../MDDB-phylogeny/results/thesis results/l0.2_s3_4_1500_o2.0_a1/chunks/unaligned',
        'model/Query_ID.test3.txt' #Change to test2 or 3 when please you, or maybe this should go automatically?
    output:
        'db_files/sintaxits1train.fa'
    script:
        'scripts/get_SINTAXdata.py'

rule get_udb_data:
    input:
        'db_files/sintaxits1train.fa',
        'model/train.fasta'
    output:
        'db_files/sintaxits1.udb',
        'db_files/its1.udb'
    shell:
        """
        vsearch --makeudb_usearch db_files/sintaxits1train.fa --output db_files/sintaxits1.udb
        vsearch --makeudb_usearch model/train.fasta --output db_files/its1.udb
        
        """

rule run_protax:
    input:
        'db_files/its1.udb',
        'db_files/sintaxits1.udb',
        'userdir/query.fasta'
    output:
        'userdir/krona.html'
    shell:
        """
        ./run_protax_plutof.sh 01 its1 90
        """
