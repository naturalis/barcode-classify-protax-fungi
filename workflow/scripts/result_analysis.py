### result_analysis.py
## Code to extract results from output files which were created during runprotax.sh perl scripts.
## query5.nameprob and query6.nameprob are used as these are the order and family levels until which the subtrees are classified.
## Results are put into csv files.

## importing packages
import argparse
import pandas as pd
from Bio import SeqIO


# Function to parse the fasta file and extract taxonomic information
def parse_fasta(filepath):
    records = list(SeqIO.parse(filepath, 'fasta'))
    tax_data = []
    max_levels = 0  # Track the maximum number of taxonomic levels

    for record in records:
        header = record.description
        seq_ID = header.split(";tax")[0]
        tax_info = header.split("tax=")[1]
        tax_levels = [level.split(":")[1] for level in tax_info.split(",")]
        max_levels = max(max_levels, len(tax_levels))  # Update max levels dynamically
        tax_data.append([seq_ID] + tax_levels)

    # Dynamically generate column names based on max_levels
    columns = ["SeqID"] + [f"Level_{i}" for i in range(max_levels)]

    # Pad rows with missing levels to match max_levels
    for i in range(len(tax_data)):
        tax_data[i] = tax_data[i] + [""] * (max_levels - len(tax_data[i]))

    return pd.DataFrame(tax_data, columns=columns)


# Function to process Protax query results
def process_protax(filepath):
    with open(filepath) as handle:
        lines = handle.readlines()
    processed_data = []
    max_levels = 0  # Track the maximum number of taxonomic levels

    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) < 3:
            parts.append("NA")  # Add empty string to make it at least 3 elements
            parts.append("0")  # Add 0 as the fourth element, which is the probability of correctness
        seq_ID, classification, probability = parts[:3]
        classification = classification.replace("Fungi,", "")
        tax_levels = classification.split(',')
        max_levels = max(max_levels, len(tax_levels))  # Update max levels dynamically
        processed_data.append([seq_ID] + tax_levels + [float(probability)])

    # Dynamically generate column names based on max_levels
    columns = ["SeqID"] + [f"Protax_Level_{i}" for i in range(max_levels)] + ["Probability"]

    # Pad rows with missing levels to match max_levels
    for i in range(len(processed_data)):
        processed_data[i] = processed_data[i] + ["NA"] * (max_levels - len(processed_data[i]))

    return pd.DataFrame(processed_data, columns=columns)


# Function to dynamically select query based on maximum level in test_true
def determine_query_file(test_true, query5_path, query6_path):
    max_level = max([int(col.split("_")[1]) for col in test_true.columns if col.startswith("Level_")])
    if max_level >= 5:
        return query6_path
    else:
        return query5_path


# Main function
def main(args):
    # Load data
    test_true = parse_fasta(args.true)
    query_path = determine_query_file(test_true, args.query5, args.query6)
    protax_results = process_protax(query_path)

    # Align levels dynamically
    num_levels = max(
        len([col for col in test_true.columns if col.startswith("Level_")]),
        len([col for col in protax_results.columns if col.startswith("Protax_Level_")])
    )
    for i in range(num_levels):
        test_true[f"Level_{i}"] = test_true.get(f"Level_{i}", "")
        protax_results[f"Protax_Level_{i}"] = protax_results.get(f"Protax_Level_{i}", "")

    # Merge data
    df = pd.merge(test_true, protax_results, on="SeqID", how="inner")

    # Determine the lowest classification level for each SeqID
    results = []
    for _, row in df.iterrows():
        lowest_true_level = max(
            [i for i in range(num_levels) if row[f"Level_{i}"]],
            default=None
        )
        if lowest_true_level is not None:
            true_classification = row[f"Level_{lowest_true_level}"]
            protax_classification = row[f"Protax_Level_{lowest_true_level}"]
            protax_probability = row["Probability"]
            accuracy = int(true_classification == protax_classification)
            results.append({
                "SeqID": row["SeqID"],
                "True_Classification": true_classification,
                "Protax_Classification": protax_classification,
                "Protax_Probability": protax_probability,
                "Accuracy": accuracy
            })

    # Convert results to a DataFrame and calculate overall accuracy
    results_df = pd.DataFrame(results)
    overall_accuracy = results_df["Accuracy"].mean()

    # Save results to CSV
    results_df.to_csv(args.output, index=False)
    with open(args.output, 'a') as f:
        f.write(f"\nTotal Accuracy,,,{overall_accuracy:.4f}\n")

    print(f"Results saved to {args.output}")
    print(f"Total Accuracy: {overall_accuracy:.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate PROTAX classifications.')
    parser.add_argument('--true', help='Input: the true classification in SINTAX format', required=True)
    parser.add_argument('--query5', help='Input: PROTAX classification until Order', required=True)
    parser.add_argument('--query6', help='Input: PROTAX classification until Family', required=True)
    parser.add_argument('--output', help='Output: CSV file with results and accuracy', required=True)
    args = parser.parse_args()

    main(args)



##########################################################################
########################## Old code ######################################
##### This code does not add Protax_Probability column to result csv #####
###########################################################################

# ## importing packages
# import argparse
# import pandas as pd
# import numpy as np
# from Bio import SeqIO
#
#
# # Function to parse the fasta file and extract taxonomic information
# def parse_fasta(filepath):
#     records = list(SeqIO.parse(filepath, 'fasta'))
#     tax_data = []
#     max_levels = 0  # Track the maximum number of taxonomic levels
#
#     for record in records:
#         header = record.description
#         seq_ID = header.split(";tax")[0]
#         tax_info = header.split("tax=")[1]
#         tax_levels = [level.split(":")[1] for level in tax_info.split(",")]
#         max_levels = max(max_levels, len(tax_levels))  # Update max levels dynamically
#         tax_data.append([seq_ID] + tax_levels)
#
#     # Dynamically generate column names based on max_levels
#     columns = ["SeqID"] + [f"Level_{i}" for i in range(max_levels)]
#
#     # Pad rows with missing levels to match max_levels
#     for i in range(len(tax_data)):
#         tax_data[i] = tax_data[i] + [""] * (max_levels - len(tax_data[i]))
#
#     return pd.DataFrame(tax_data, columns=columns)
#
#
#
# # Function to process Protax query results
# def process_protax(filepath):
#     with open(filepath) as handle:
#         lines = handle.readlines()
#     processed_data = []
#     max_levels = 0  # Track the maximum number of taxonomic levels
#
#     for line in lines:
#         parts = line.strip().split('\t')
#         if len(parts) < 3:
#             parts.append("NA")  # Add empty string to make it at least 3 elements
#             parts.append(0)  # Add 0 as the fourth element, which is the probability of correctness
#         seq_ID, classification, probability = parts[:3]
#         classification = classification.replace("Fungi,", "")
#         tax_levels = classification.split(',')
#         max_levels = max(max_levels, len(tax_levels))  # Update max levels dynamically
#         processed_data.append([seq_ID] + tax_levels + [probability])
#
#     # Dynamically generate column names based on max_levels
#     columns = ["SeqID"] + [f"Protax_Level_{i}" for i in range(max_levels)] + ["Probability"]
#
#     # Pad rows with missing levels to match max_levels
#     for i in range(len(processed_data)):
#         processed_data[i] = processed_data[i] + ["NA"] * (max_levels - len(processed_data[i]))
#
#     return pd.DataFrame(processed_data, columns=columns)
#
# # Function to dynamically select query based on maximum level in test_true
# def determine_query_file(test_true, query5_path, query6_path):
#     max_level = max([int(col.split("_")[1]) for col in test_true.columns if col.startswith("Level_")])
#     if max_level >= 5:
#         # print("Using query6 for classification up to Family level.")
#         return query6_path
#     else:
#         # print("Using query5 for classification up to Order level.")
#         return query5_path
#
# # Main function
# def main(args):
#     # Load data
#     test_true = parse_fasta(args.true)
#     query_path = determine_query_file(test_true, args.query5, args.query6)
#     protax_results = process_protax(query_path)
#
#     # Align levels dynamically
#     num_levels = max(
#         len([col for col in test_true.columns if col.startswith("Level_")]),
#         len([col for col in protax_results.columns if col.startswith("Protax_Level_")])
#     )
#     for i in range(num_levels):
#         test_true[f"Level_{i}"] = test_true.get(f"Level_{i}", "")
#         protax_results[f"Protax_Level_{i}"] = protax_results.get(f"Protax_Level_{i}", "")
#
#     # Merge data
#     df = pd.merge(test_true, protax_results, on="SeqID", how="inner")
#
#     # Determine the lowest classification level for each SeqID
#     results = []
#     for _, row in df.iterrows():
#         lowest_true_level = max(
#             [i for i in range(num_levels) if row[f"Level_{i}"]],
#             default=None
#         )
#         if lowest_true_level is not None:
#             true_classification = row[f"Level_{lowest_true_level}"]
#             protax_classification = row[f"Protax_Level_{lowest_true_level}"]
#             accuracy = int(true_classification == protax_classification)
#             results.append({
#                 "SeqID": row["SeqID"],
#                 "True_Classification": true_classification,
#                 "Protax_Classification": protax_classification,
#                 "Protax_Probability": 0,
#                 "Accuracy": accuracy
#             })
#
#     # Convert results to a DataFrame and calculate overall accuracy
#     results_df = pd.DataFrame(results)
#     overall_accuracy = results_df["Accuracy"].mean()
#
#     # Save results to CSV
#     results_df.to_csv(args.output, index=False)
#     with open(args.output, 'a') as f:
#         f.write(f"\nTotal Accuracy,,,{overall_accuracy:.4f}\n")
#
#     print(f"Results saved to {args.output}")
#     print(f"Total Accuracy: {overall_accuracy:.2f}")
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Evaluate PROTAX classifications.')
#     parser.add_argument('--true', help='Input: the true classification in SINTAX format', required=True)
#     parser.add_argument('--query5', help='Input: PROTAX classification until Order', required=True)
#     parser.add_argument('--query6', help='Input: PROTAX classification until Family', required=True)
#     parser.add_argument('--output', help='Output: CSV file with results and accuracy', required=True)
#     args = parser.parse_args()
#
#     main(args)

