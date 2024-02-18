# # get_SINTAXdata.py

# get_traindata.py
# Script goal is to create taxonomically annotated seq ID's for SINTAX

import os
from Bio import SeqIO

def integrate_taxonomy(sequence_id, taxonomy):
    # Generate the integrated sequence ID with taxonomic annotation
    return f"{sequence_id};tax={''.join(taxonomy)}"

def process_fasta_file(input_file, output_file, excluded_ids):
    # Open the input fasta file and create the output fasta file
    with open(input_file, 'r') as input_handle, open(output_file, 'a') as output_handle:
        # Parse the sequences from the input fasta file
        records = list(SeqIO.parse(input_handle, 'fasta'))

        # Process each sequence
        for record in records:
            # Skip the sequence if its ID is in the excluded IDs list
            if record.id in excluded_ids:
                continue

            # Extract taxonomic information from the file name
            file_name_parts = os.path.splitext(os.path.basename(input_file))[0].split('__')
            taxonomy = [] # Make empty taxonomy list, will be added to, taxon by taxon
            for idx, part in enumerate(file_name_parts[1:]):
                # Replace underscores with commas for all parts
                part = part.replace('_', ',')

                # When part contains >1 commas, only keep everything before the first
                # and after the last, separated by a ','.:
                if ',' in part and idx < len(file_name_parts[1:]) - 1 and idx != 0:
                    part = f"{part.split(',')[0]},{part.split(',')[-1]}"
                    taxonomy.append(f"{part}:")

                # Remove everything after the last comma for the last part
                if idx == len(file_name_parts[1:]) - 1:
                    part = part.split(',')[0]
                    taxonomy.append(f"{part}")

                # Add p: at start and : at end, only at the first part
                if idx == 0:
                    taxonomy.append(f"p:{part}:")

            # Integrate taxonomic information into the sequence ID
            new_id = integrate_taxonomy(record.id, taxonomy)

            # Create a new SeqRecord with the updated ID
            new_record = record.__class__(seq=record.seq, id=new_id, name="", description="")

            # Write the updated sequence to the output fasta file
            SeqIO.write([new_record], output_handle, 'fasta')

if __name__ == "__main__":
    input_folder = "..\\MDDB-phylogeny\\results\\thesis results\\l0.2_s3_4_1500_o2.0_a1\\chunks\\unaligned"
    output_file = "model\\sintaxits1train.fasta"
    excluded_ids_file = "model\\Query_ID.test1.txt"

    # Read excluded IDs from the file
    with open(excluded_ids_file, 'r') as excluded_ids_handle:
        excluded_ids = set(line.strip() for line in excluded_ids_handle)

    # Iterate over each fasta file in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".fasta"):
            input_file_path = os.path.join(input_folder, file_name)
            process_fasta_file(input_file_path, output_file, excluded_ids)

    print("Integration complete.")


#########################################################################
############### OLD METHOD: DOES NOT EXCLUDE QUERY ID's #################
#########################################################################
# # Script goal is to create taxonomically annotated seq ID's for SINTAX
#
# import os
# from Bio import SeqIO
#
# def integrate_taxonomy(sequence_id, taxonomy):
#     # Generate the integrated sequence ID with taxonomic annotation
#     return f"{sequence_id};tax={''.join(taxonomy)}"
#
# def process_fasta_file(input_file, output_file):
#     # Open the input fasta file and create the output fasta file
#     with open(input_file, 'r') as input_handle, open(output_file, 'a') as output_handle:
#         # Parse the sequences from the input fasta file
#         records = list(SeqIO.parse(input_handle, 'fasta'))
#
#         # Process each sequence
#         for record in records:
#             # Extract taxonomic information from the file name
#             file_name_parts = os.path.splitext(os.path.basename(input_file))[0].split('__')
#             taxonomy = [f"p:{part.replace('_', ',')}:" if idx == 0 else f"{part.replace('_', ',')}:" if idx < len(
#                 file_name_parts[1:]) - 1 else f"{part.replace('_', ',')}" for idx, part in
#                         enumerate(file_name_parts[1:])]
#             # The above code adds a p: at the start of taxonomy, replaces _ to , and adds a : to each part except the
#             # last.
#
#             # Integrate taxonomic information into the sequence ID
#             new_id = integrate_taxonomy(record.id, taxonomy)
#
#             # Create a new SeqRecord with the updated ID
#             new_record = record.__class__(seq=record.seq, id=new_id, name="", description="")
#
#             # Write the updated sequence to the output fasta file
#             SeqIO.write([new_record], output_handle, 'fasta')
#
# if __name__ == "__main__":
#     input_folder = "..\\MDDB-phylogeny\\results\\thesis results\\l0.2_s3_4_1500_o2.0_a1\\chunks\\unaligned"
#     output_file = "model\\sintaxits1train.fasta"
#
#     # Iterate over each fasta file in the input folder
#     for file_name in os.listdir(input_folder):
#         if file_name.endswith(".fasta"):
#             input_file_path = os.path.join(input_folder, file_name)
#             process_fasta_file(input_file_path, output_file)
#
#     print("Integration complete.")
#
#
#
