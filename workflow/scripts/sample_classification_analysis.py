## sample_classification_analysis.py
## This script has two goals:
## 1. Determine the percentage of samples that has been classified
## 2. Determine the subtrees from the MDDB-phylogenetic tree these samples have been classified in


import argparse
import os
import csv
import re


def parse_query_file(query_file):
    # Parse query file and extract SeqID, Classification, and Probability
    classifications = {}
    with open(query_file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')

            # Initialize default values for missing data
            seq_id = "NA"
            classification = "NA"
            probability = 0

            if len(parts) >= 1:
                seq_id = parts[0]
            if len(parts) >= 2:
                classification = parts[1]
            if len(parts) >= 3:
                try:
                    probability = float(parts[2])
                except ValueError:
                    probability = 0.0  # Default probability for invalid values

            # Add the data to the dictionary
            classifications[seq_id] = (classification, probability)

    return classifications


def extract_taxonomy_from_filename(filename):
    # Extract taxonomy from the filename
    filename = filename.strip()

    # Match the filename with taxonomy levels
    match = re.match(r'(\d+_\d+)_p__(.*?)_c__(.*?)_o__(.*?)_f__(.*?)\.*.fasta$', filename)
    if match:
        # print(match.groups()[1:])
        return match.groups()[1:]  # Return as (phylum, class, order, family)

    match = re.match(r'(\d+_\d+)_p__(.*?)_c__(.*?)_o__(.*?)\.*.fasta$', filename)
    if match:
        # print(match.groups()[1:])
        return match.groups()[1:]  # Return as (phylum, class, order)

    return None


# def match_classification_to_subtree(classification, filenames):
#     # Try to match the classification (up to family) to a subtree (filename)
#     taxonomy_levels = classification.split(',')[1:]  # Skip "Fungi"
#     for filename in filenames:
#         taxonomy_from_filename = extract_taxonomy_from_filename(filename)
#         # Convert taxonomy_levels to a tuple for comparison
#         if taxonomy_from_filename and taxonomy_from_filename[:len(taxonomy_levels)] == tuple(taxonomy_levels):
#             return filename
#     return None

def match_classification_to_subtree(classification, filenames):
    if classification == "NA":
        return None  # Skip matching for "NA"

    # Split classification string and ensure it aligns with taxonomy
    taxonomy_levels = classification.split(',')[1:]  # Skip "Fungi"
    taxonomy_levels = [level.strip() for level in taxonomy_levels if level.strip()]  # Clean up levels

    for filename in filenames:
        taxonomy_from_filename = extract_taxonomy_from_filename(filename)
        if taxonomy_from_filename and taxonomy_from_filename[:len(taxonomy_levels)] == tuple(taxonomy_levels):
            return filename
    return None

def merge_queries(query4, query5):
    # Merge query4 and query5, preserving existing data in query4
    merged = query5.copy()
    for seq_id, (classification, probability) in query4.items():
        if seq_id in merged:
            existing_classification, existing_probability = merged[seq_id]
            merged_classification = (
                classification if classification != "NA" else existing_classification
            )
            merged_probability = (
                probability if probability != 0 else existing_probability
            )
            merged[seq_id] = (merged_classification, merged_probability)
        else:
            merged[seq_id] = (classification, probability)
    return merged


def process_sequences(merged_queries, directory_files):
    # Process sequences to classify and match to subtrees
    results = []
    total_prob = 0
    classified_count = 0
    total_sequences = len(merged_queries)

    for seq_id, (classification, prob) in merged_queries.items():
        matched_subtree = match_classification_to_subtree(classification, directory_files)
        results.append([seq_id, classification, matched_subtree, prob])

        if matched_subtree:
            classified_count += 1
        total_prob += prob

    # Compute average probability and classification percentage
    avg_prob = total_prob / (classified_count if classified_count > 0 else 1)
    classified_percentage = (classified_count / total_sequences) * 100 if total_sequences > 0 else 0

    return results, avg_prob, classified_percentage


def write_to_csv(results, avg_prob, classified_percentage, output_file):
    # Write results to a CSV file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['SeqID', 'Classification', 'Matched Subtree', 'Probability'])
        writer.writerows(results)
        writer.writerow([])  # Blank row for readability
        writer.writerow(['Average Probability:', avg_prob])
        writer.writerow(['Percentage Classified:', f'{classified_percentage}%'])


def main():
    parser = argparse.ArgumentParser(description='Classify sequences and match to subtrees.')
    parser.add_argument('--directory', help='Path to the directory containing FASTA files')
    parser.add_argument('--query4', help='Path to query4 file')
    parser.add_argument('--query5', help='Path to query5 file')
    parser.add_argument('--output', help='Path to the output CSV file')

    args = parser.parse_args()

    # Parse query files
    query4 = parse_query_file(args.query4)
    query5 = parse_query_file(args.query5)

    # Merge query4 and query5
    merged_queries = merge_queries(query4, query5)

    # Get all filenames in the directory
    directory_files = os.listdir(args.directory)

    # Process sequences
    results, avg_prob, classified_percentage = process_sequences(merged_queries, directory_files)

    # Write results to CSV
    write_to_csv(results, avg_prob, classified_percentage, args.output)


if __name__ == '__main__':
    main()


# import argparse
# import os
# import csv
# import re
#
#
# def parse_query_file(query_file):
#     # Parse query file and extract SeqID, Classification, and Probability
#     classifications = {}
#     with open(query_file, 'r') as f:
#         for line in f:
#             parts = line.strip().split('\t')
#
#             # Initialize default values for missing data
#             seq_id = "NA"
#             classification = "NA"
#             probability = 0
#
#             if len(parts) >= 1:
#                 seq_id = parts[0]
#             if len(parts) >= 2:
#                 classification = parts[1]
#             if len(parts) >= 3:
#                 try:
#                     probability = float(parts[2])
#                 except ValueError:
#                     probability = 0.0 # Set to NA for invalid probability
#
#             # Add the data to the dictionary
#             classifications[seq_id] = (classification, probability)
#
#     return classifications
#
#
# # def parse_query_file(query_file):
# #     # Parse query file and extract SeqID, Classification, and Probability
# #     classifications = {}
# #     with open(query_file, 'r') as f:
# #         for line in f:
# #             parts = line.strip().split('\t')
# #             # Skip empty lines or malformed lines
# #             if len(parts) < 3:
# #                 # print(f"Skipping malformed line: {line.strip()}")
# #                 continue
# #             seq_id = parts[0]
# #             classification = parts[1]
# #             try:
# #                 probability = float(parts[2])
# #             except ValueError:
# #                 print(f"Skipping line with invalid probability: {line.strip()}")
# #                 continue
# #             classifications[seq_id] = (classification, probability)
# #     return classifications
#
#
# def extract_taxonomy_from_filename(filename):
#     # Strip any extra spaces or special characters
#     filename = filename.strip()
#
#     # Try matching the filename with the full taxonomy (including family) and optional extension
#     match = re.match(r'(\d+_\d+)_p__(.*?)_c__(.*?)_o__(.*?)_f__(.*?)\.*.fasta$', filename)
#     if match:
#         return match.groups()[1:]  # Return as (phylum, class, order, family)
#
#     # Try matching without the family part and optional extension
#     match = re.match(r'(\d+_\d+)_p__(.*?)_c__(.*?)_o__(.*?)\.*.fasta$', filename)
#     if match:
#         return match.groups()[1:]  # Return as (phylum, class, order)
#
#     # If no match, return None
#     return None
#
# def match_classification_to_subtree(classification, filenames):
#     # Try to match the classification (up to family) to a subtree (filename)
#     taxonomy_levels = classification.split(',')[1:]  # Skip "Fungi"
#     for filename in filenames:
#         taxonomy_from_filename = extract_taxonomy_from_filename(filename)
#         # Convert taxonomy_levels to a tuple for comparison
#         if taxonomy_from_filename and taxonomy_from_filename[:len(taxonomy_levels)] == tuple(taxonomy_levels):
#             return filename
#     return None
#
# def merge_queries(query4, query5):
#     # Merge query4 and query5, preserving existing data in query4
#     merged = query4.copy()
#     for seq_id, (classification, probability) in query5.items():
#         if seq_id in merged:
#             existing_classification, existing_probability = merged[seq_id]
#             merged_classification = (
#                 classification if classification != "NA" else existing_classification
#             )
#             merged_probability = (
#                 probability if probability != 0 else existing_probability
#             )
#             merged[seq_id] = (merged_classification, merged_probability)
#         else:
#             merged[seq_id] = (classification, probability)
#     return merged
#
# def process_sequences(query5, query4, directory_files):
#     # Process each sequence ID and try to find the classification and matched subtree
#     results = []
#     total_prob = 0
#     classified_count = 0
#     total_sequences = len(query5) + len(query4)
#
#     for seq_id in query5.keys():
#         classification, prob = query5[seq_id]
#         matched_subtree = match_classification_to_subtree(classification, directory_files)
#
#         if matched_subtree is None:  # If not found, try query4
#             if seq_id in query4:
#                 classification, prob = query4[seq_id]
#                 matched_subtree = match_classification_to_subtree(classification, directory_files)
#
#         # Fill in results
#         results.append([seq_id, classification, matched_subtree if matched_subtree else 'NA', prob])
#
#         if matched_subtree:
#             classified_count += 1
#         total_prob += prob
#
#     # If no classification in query5, check query4
#     for seq_id in query4.keys():
#         if seq_id not in query5:
#             classification, prob = query4[seq_id]
#             matched_subtree = match_classification_to_subtree(classification, directory_files)
#             results.append([seq_id, classification, matched_subtree if matched_subtree else 'NA', prob])
#             total_prob += prob
#             if matched_subtree:
#                 classified_count += 1
#
#     # Compute average probability and classification percentage
#     avg_prob = total_prob / (classified_count if classified_count > 0 else 1)
#     classified_percentage = (classified_count / total_sequences) * 100 if total_sequences > 0 else 0
#
#     return results, avg_prob, classified_percentage
#
#
# def write_to_csv(results, avg_prob, classified_percentage, output_file):
#     # Write results into CSV file
#     with open(output_file, 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['SeqID', 'Classification', 'Matched Subtree', 'Probability'])
#         writer.writerows(results)
#         writer.writerow([])  # Blank row for readability
#         writer.writerow(['Average Probability:', avg_prob])
#         writer.writerow(['Percentage Classified:', f'{classified_percentage}%'])
#
# def main():
#     parser = argparse.ArgumentParser(description='Classify sequences and match to subtrees.')
#     parser.add_argument('--directory', help='Path to the directory containing FASTA files')
#     parser.add_argument('--query4', help='Path to query4 file')
#     parser.add_argument('--query5', help='Path to query5 file')
#     parser.add_argument('--output', help='Path to the output CSV file')
#
#     args = parser.parse_args()
#
#     # Parse query files
#     query4 = parse_query_file(args.query4)
#     query5 = parse_query_file(args.query5)
#
#     # Get all filenames in the directory
#     directory_files = os.listdir(args.directory)
#
#     # Process sequences
#     results, avg_prob, classified_percentage = process_sequences(query5, query4, directory_files)
#
#     # Write results to CSV
#     write_to_csv(results, avg_prob, classified_percentage, args.output)
#
#
# if __name__ == '__main__':
#     main()

