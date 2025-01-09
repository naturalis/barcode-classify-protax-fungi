# # test_train_split.py
# # Splits train and test, 20% testing set and 80% train
# # 20% train set includes Query1, Query2, and Query3.txt, which are queries used by Lena to test BLAST accuracy.
# # This code takes all sequences from a specific folder and puts them in one fasta files, skipping the sequences listed
# # in a text file.
import os
import argparse
from Bio import SeqIO
import random

# Function which checks if output file exists, if it does not: it creates, if it does: wipe it
def create_or_wipe_files(file):
    with open(file, 'w'):
        pass

# Function to collect all sequences from all chunks
def collect_all_sequences(input_folder):
    all_records = []
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".fasta"):
            input_file_path = os.path.join(input_folder, file_name)
            with open(input_file_path, 'r') as input_handle:
                for record in SeqIO.parse(input_handle, 'fasta'):
                    if "OUTGROUP" not in record.id:
                        all_records.append(record)
    return all_records

# Function to split the test/train set
def process_fasta_files(input_folder, output_file, test_file, excluded_ids, test_sequences):
    with open(output_file, 'a') as output_handle, open(test_file, 'a') as test_handle:
        for file_name in os.listdir(input_folder):
            if file_name.endswith(".fasta"):
                input_file_path = os.path.join(input_folder, file_name)
                with open(input_file_path, 'r') as input_handle:
                    records = list(SeqIO.parse(input_handle, 'fasta'))

                    for record in records:
                        if record.id in excluded_ids or record.id in test_sequences:
                            new_record = record.__class__(seq=record.seq, id=record.id, name="", description="")
                            SeqIO.write([new_record], test_handle, 'fasta')
                        else:
                            new_record = record.__class__(seq=record.seq, id=record.id, name="", description="")
                            SeqIO.write([new_record], output_handle, 'fasta')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process fasta files and exclude specific IDs.')
    parser.add_argument('--input', help='Input folder containing fasta files', required=True)
    parser.add_argument('--output', help='Output train fasta file', required=True)
    parser.add_argument('--test', help='Output test fasta file', required=True)
    parser.add_argument('--excluded1', help='File containing IDs to be excluded / Query1', required=False)
    parser.add_argument('--excluded2', help='File containing IDs to be excluded / Query2', required=False)
    parser.add_argument('--excluded3', help='File containing IDs to be excluded / Query3', required=False)
    parser.add_argument('--test_ratio', help='Proportion of data to allocate to test set (default: 0.2)',
                        type=float, default=0.2)
    args = parser.parse_args()

    input_folder = args.input
    output_file = args.output
    test_file = args.test
    test_ratio = args.test_ratio

    create_or_wipe_files(output_file)
    create_or_wipe_files(test_file)

    # Collect all query IDs from any provided exclusion files
    excluded_ids = set()
    for excluded_file in [args.excluded1, args.excluded2, args.excluded3]:
        if excluded_file:  # Only process files that are provided
            with open(excluded_file, 'r') as file_handle:
                excluded_ids.update(line.strip() for line in file_handle)

    # Collect all sequences from all chunks
    all_sequences = collect_all_sequences(input_folder)

    # Calculate the total number of test sequences
    total_sequences = len(all_sequences)
    if test_ratio > 0:
        test_count = int(total_sequences * test_ratio)
        test_sequences = set(record.id for record in random.sample(all_sequences, test_count))
    else:
        test_sequences = set()  # No random test sequences if ratio is 0.0

    # Add only excluded sequences to the test set if ratio is 0.0
    if test_ratio == 0.0:
        test_sequences.update(excluded_ids)

    # Process all fasta files to split into test/train sets
    process_fasta_files(input_folder, output_file, test_file, excluded_ids, test_sequences)


#
#
# import os
# import argparse
# from Bio import SeqIO
# import random
#
#
# # Function which checks if output file exists, if it does not: it creates, if it does: wipe it
# def create_or_wipe_files(file):
#     # Create or clear the file
#     with open(file, 'w'):
#         pass
#
#
# # Function to collect all sequences from all chunks
# def collect_all_sequences(input_folder):
#     all_records = []
#     for file_name in os.listdir(input_folder):
#         if file_name.endswith(".fasta"):
#             input_file_path = os.path.join(input_folder, file_name)
#             with open(input_file_path, 'r') as input_handle:
#                 for record in SeqIO.parse(input_handle, 'fasta'):
#                     # Skip sequences with OUTGROUP in their ID
#                     if "OUTGROUP" not in record.id:
#                         all_records.append(record)
#                 # all_records.extend(list(SeqIO.parse(input_handle, 'fasta')))
#     return all_records
#
#
# # Function to split the test/trainset
# def process_fasta_files(input_folder, output_file, test_file, excluded_ids, test_sequences):
#     # Open files for appending
#     with open(output_file, 'a') as output_handle, open(test_file, 'a') as test_handle:
#
#         # Iterate over each fasta file in the input folder
#         for file_name in os.listdir(input_folder):
#             if file_name.endswith(".fasta"):
#                 input_file_path = os.path.join(input_folder, file_name)
#                 with open(input_file_path, 'r') as input_handle:
#                     records = list(SeqIO.parse(input_handle, 'fasta'))
#
#                     # Separate sequences into test and train sets
#                     for record in records:
#                         if record.id in excluded_ids or record.id in test_sequences:
#                             new_record = record.__class__(seq=record.seq, id=record.id, name="", description="")
#                             SeqIO.write([new_record], test_handle, 'fasta')
#                         else:
#                             new_record = record.__class__(seq=record.seq, id=record.id, name="", description="")
#                             SeqIO.write([new_record], output_handle, 'fasta')
#
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Process fasta files and exclude specific IDs.')
#     parser.add_argument('--input', help='Input folder containing fasta files', required=True)
#     parser.add_argument('--output', help='Output train fasta file', required=True)
#     parser.add_argument('--test', help='Output test fasta file', required=True)
#     parser.add_argument('--excluded1', help='File containing IDs to be excluded / Query1', required=False)
#     parser.add_argument('--excluded2', help='File containing IDs to be excluded / Query2', required=False)
#     parser.add_argument('--excluded3', help='File containing IDs to be excluded / Query3', required=False)
#     parser.add_argument('--test_ratio', help='Proportion of data to allocate to test set (default: 0.2)',
#                         type=float, default=0.2)
#     args = parser.parse_args()
#
#     input_folder = args.input
#     output_file = args.output
#     test_file = args.test
#     test_ratio = args.test_ratio
#
#     create_or_wipe_files(output_file)
#     create_or_wipe_files(test_file)
#
#     # Collect all query IDs
#     excluded_ids = set()
#     for excluded_file in [args.excluded1, args.excluded2, args.excluded3]:
#         with open(excluded_file, 'r') as file_handle:
#             excluded_ids.update(line.strip() for line in file_handle)
#
#     # Collect all sequences from all chunks
#     all_sequences = collect_all_sequences(input_folder)
#
#     # Calculate the total number of test sequences
#     total_sequences = len(all_sequences)
#     test_count = int(total_sequences * test_ratio)
#
#     # Randomly sample test sequences
#     test_sequences = set(record.id for record in random.sample(all_sequences, test_count))
#
#     # Process all fasta files to split into test/train sets
#     process_fasta_files(input_folder, output_file, test_file, excluded_ids, test_sequences)
