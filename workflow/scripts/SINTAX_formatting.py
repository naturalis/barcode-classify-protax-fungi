# SINTAX_formatting.py
# Use this script to format any file into SINTAX format
# SINTAX format is the following:
# > seq1;tax=p:Phylum,c:Class,o:Order,f:Family
# [sequence]
# E.g.: >SH1237664.08FU_JN685254_reps;tax=p:Glomeromycota,c:Glomeromycetes,o:Glomerales
# TCGATTTAGCGAACCTGCTATGGTTTCGCGAAACAATGTATTTAAAACCTACTCATATAAAAAATTTTTTTGTATATATAATATATTTAAGATCACTTTCAACAACGGATCTCTTGGTTCTCGCATCGATGAAGAACGTAGCGAAGTGCGATAAGTAATGTGAATTGCAGATTCCGTGAATCATCGAATCTTTGAACGCAAATTGCACTCTCTGGCATTCCAGGGAGTATGCCTGTTTGAGGGTCAGTATAACAAAAAAAAATCGGTATGTTGCTTTTTTTGTGACTTTCCGGATTTTGGGTTATCTTAATGTTTTTAAAATTTAAGAGGCTTAAAATTGATCTCTTGCGCATTATTTTTAGATGTACATAAATTCTTTTATTCGTCATATAATGCCAAAATTTGTTAGATACGATCATACTGTGTGGTTCGTACCTAAAATTTTTCATAA


import os
import argparse
from Bio import SeqIO

def create_or_wipe_file(file_path):
    """Creates or clears the given file."""
    with open(file_path, 'w'):
        pass

def integrate_sintax_format(sequence_id, taxonomy):
    """Generates the SINTAX-formatted taxonomy for a sequence."""
    return f"{sequence_id};tax={''.join(taxonomy)}"

def process_fasta_files(input_folder, test_file, output_file):
    """
    Processes fasta files to generate a `test_true` output in SINTAX format.
    All sequences matching IDs in `test.fasta` will be written to `test_true.fasta` in SINTAX format.
    """
    # Read the IDs of test sequences from the test file
    test_ids = set(record.id for record in SeqIO.parse(test_file, 'fasta'))

    # Process each fasta file in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".fasta"):
            input_file_path = os.path.join(input_folder, file_name)

            with open(input_file_path, 'r') as input_handle:
                records = list(SeqIO.parse(input_handle, 'fasta'))

            for record in records:
                if record.id in test_ids:
                    # Extract taxonomy from the file name
                    file_name_parts = os.path.splitext(os.path.basename(input_file_path))[0].split('__')
                    taxonomy = []
                    for idx, part in enumerate(file_name_parts[1:]):
                        part = part.replace('_', ',')
                        if ',' in part and idx < len(file_name_parts[1:]) - 1 and idx != 0:
                            part = f"{part.split(',')[0]},{part.split(',')[-1]}"
                            taxonomy.append(f"{part}:")
                        if idx == len(file_name_parts[1:]) - 1:
                            part = part.split(',')[0]
                            taxonomy.append(f"{part}")
                        if idx == 0:
                            taxonomy.append(f"p:{part}:")

                    # Generate SINTAX-formatted sequence ID
                    sintax_id = integrate_sintax_format(record.id, taxonomy)
                    new_record = record.__class__(seq=record.seq, id=sintax_id, name="", description="")

                    # Write the SINTAX-formatted record to the output file
                    with open(output_file, 'a') as output_handle:
                        SeqIO.write([new_record], output_handle, 'fasta')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a SINTAX-formatted test_true file.')
    parser.add_argument('--input', help='Input folder containing fasta files', required=True)
    parser.add_argument('--test', help='Input test fasta file (test.fasta)', required=True)
    parser.add_argument('--output', help='Output test_true file in SINTAX format (test_true.fasta)', required=True)
    args = parser.parse_args()

    input_folder = args.input
    test_file = args.test
    output_file = args.output

    create_or_wipe_file(output_file)

    # Process fasta files to generate the test_true file
    process_fasta_files(input_folder, test_file, output_file)

    print(f"Test true file generated in SINTAX format: {output_file}")
