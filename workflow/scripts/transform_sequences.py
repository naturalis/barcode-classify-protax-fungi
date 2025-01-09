import argparse

def transform_sequence(input_file, output_file):
    with open(input_file, 'r') as f_in:
        lines = f_in.readlines()

    transformed_lines = []

    for line in lines:
        if line.startswith('>'):
            transformed_lines.append(line)
        else:
            transformed_lines[-1] += line.strip()

    with open(output_file, 'w') as f_out:
        for line in transformed_lines:
            f_out.write(line + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform sequence data.')
    parser.add_argument('--input', help='Input sequence data file', required=True)
    parser.add_argument('--output', help='Output transformed sequence data file', required=True)
    args = parser.parse_args()

    transform_sequence(args.input, args.output)
