import argparse
import random


def fastq_to_fasta(fastq_file, fasta_file, percent):
    """
    Convert a FASTQ file to a FASTA file, processing only a percentage of the sequences.

    Args:
        fastq_file (str): Path to the input FASTQ file.
        fasta_file (str): Path to the output FASTA file.
        percent (int): Percentage of sequences to include in the output.
    """
    with open(fastq_file, 'r') as fq, open(fasta_file, 'w') as fa:
        while True:
            try:
                # Read 4 lines from the FASTQ file
                header = fq.readline().strip()  # Line 1: Header (starts with @)
                sequence = fq.readline().strip()  # Line 2: Sequence
                fq.readline()  # Line 3: +
                fq.readline()  # Line 4: Quality score

                if not header or not sequence:
                    break  # End of file

                # Randomly decide whether to include this sequence based on the percentage
                if random.uniform(0, 100) <= percent:
                    fasta_header = ">" + header.split()[0][1:]  # Remove @, keep the ID
                    fa.write(f"{fasta_header}\n{sequence}\n")

            except Exception as e:
                print(f"Error processing file: {e}")
                break


def main():
    parser = argparse.ArgumentParser(
        description="Convert a FASTQ file to a FASTA file with an optional percentage filter.")
    parser.add_argument("fastq_file", help="Path to the input FASTQ file.")
    parser.add_argument("fasta_file", help="Path to the output FASTA file.")
    parser.add_argument("--percent", type=int, default=100,
                        help="Percentage of sequences to include in the output (1-100). Default is 100.")

    args = parser.parse_args()

    if not (0 <= args.percent <= 100):
        raise ValueError("The --percent argument must be between 1 and 100.")

    fastq_to_fasta(args.fastq_file, args.fasta_file, args.percent)


if __name__ == "__main__":
    main()

# import argparse
#
#
# def fastq_to_fasta(fastq_file, fasta_file):
#     """
#     Convert a FASTQ file to a FASTA file.
#
#     Args:
#         fastq_file (str): Path to the input FASTQ file.
#         fasta_file (str): Path to the output FASTA file.
#     """
#     with open(fastq_file, 'r') as fq, open(fasta_file, 'w') as fa:
#         while True:
#             try:
#                 # Read 4 lines from the FASTQ file
#                 header = fq.readline().strip()  # Line 1: Header (starts with @)
#                 sequence = fq.readline().strip()  # Line 2: Sequence
#                 fq.readline()  # Line 3: +
#                 fq.readline()  # Line 4: Quality score
#
#                 if not header or not sequence:
#                     break  # End of file
#
#                 # Convert the header to a FASTA format
#                 fasta_header = ">" + header.split()[0][1:]  # Remove @, keep the ID
#                 fa.write(f"{fasta_header}\n{sequence}\n")
#
#             except Exception as e:
#                 print(f"Error processing file: {e}")
#                 break
#
#
# def main():
#     parser = argparse.ArgumentParser(description="Convert a FASTQ file to a FASTA file.")
#     parser.add_argument("fastq_file", help="Path to the input FASTQ file.")
#     parser.add_argument("fasta_file", help="Path to the output FASTA file.")
#
#     args = parser.parse_args()
#     fastq_to_fasta(args.fastq_file, args.fasta_file)
#
#
# if __name__ == "__main__":
#     main()
#
