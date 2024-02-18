# scripts/random_sequences.py

from Bio import SeqIO
import random
import argparse

num_sequences = 25

# importing data
with open('data/backbone.fasta', 'r') as input_file:
    sequences = list(SeqIO.parse(input_file, 'fasta'))

# Randomly select 25 sequences [Random Route]
# selected_sequences = random.sample(sequences, min(num_sequences, len(sequences)))
# Make a set of IDS from selected_sequences, to be able to compare later
# selected_ids = set(seq.id for seq in selected_sequences)

# Select 25 sequences from input file Query_ID.testX.txt [Selected Route]
with open('model/Query_ID.test1.txt', 'r') as Query_IDs:
    selected_ids = set(line.strip() for line in Query_IDs)
selected_sequences = [seq for seq in sequences if seq.id in selected_ids]

# Write selected sequences to test.fasta
with open(snakemake.output[0], 'w') as test_file:
    SeqIO.write(selected_sequences, test_file, 'fasta')




# Create remaining_sequences based on IDs
remaining_sequences = [seq for seq in sequences if seq.id not in selected_ids]
# Write remaining sequences to train.fa
with open(snakemake.output[1], 'w') as train_file:
    SeqIO.write(remaining_sequences, train_file, 'fasta')

# with open(snakemake.output[0], 'w') as input_file:
#     sequences = list(SeqIO.parse(input_file, 'fasta'))



############################# Old method, using a function:
# def select_random_sequences(input_file, output_test, output_train, num_sequences=25):
#     # Read sequences from the input file
#     # sequences = list(SeqIO.parse(input_file, 'fasta'))
#
#     # Randomly select 25 sequences
#     selected_sequences = random.sample(sequences, min(num_sequences, len(sequences)))
#
#     # Write selected sequences to test.fa
#     with open(output_test, 'w') as test_file:
#         SeqIO.write(selected_sequences, test_file, 'fasta')
#
#     # Write remaining sequences to train.fa
#     remaining_sequences = [seq for seq in sequences if seq not in selected_sequences]
#     with open(output_train, 'w') as train_file:
#         SeqIO.write(remaining_sequences, train_file, 'fasta')
#
# # Provide the required arguments
# select_random_sequences(sequences, snakemake.output[0], snakemake.output[1])
