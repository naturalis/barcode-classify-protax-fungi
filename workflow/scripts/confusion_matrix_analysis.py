import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from sklearn.metrics import confusion_matrix


def generate_confusion_matrix(input_csv, output_pdf):
    # Load the results
    data = pd.read_csv(input_csv)

    # Extract true and predicted classifications
    true_labels = data['True_Classification'].fillna('Unknown').astype(str)
    predicted_labels = data['Protax_Classification'].fillna('Unknown').astype(str)

    # Create confusion matrix
    labels = sorted(set(true_labels) | set(predicted_labels))  # Unique sorted labels
    cm = confusion_matrix(true_labels, predicted_labels, labels=labels)

    # Calculate total accuracy
    total_accuracy = (true_labels == predicted_labels).mean()
    print(f"Total Accuracy: {total_accuracy:.4f}")

    # # Plot confusion matrix
    # plt.figure(figsize=(20, 20))  # Increase figure size for better readability
    # sns.heatmap(cm, annot=False, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels, cbar=True)
    # plt.xlabel('Predicted Classification')
    # plt.ylabel('True Classification')
    # plt.title('Confusion Matrix')
    #
    # # Save the confusion matrix plot as a PDF
    # plt.tight_layout()
    # plt.savefig(output_pdf, format='pdf', dpi=300)
    # print(f"Confusion matrix saved as {output_pdf}")

    # Create annotation array with empty strings for zero counts
    annot = [[f"{value}" if value > 0 else "" for value in row] for row in cm]

    # Plot confusion matrix with non-zero sample count annotations
    plt.figure(figsize=(20, 20))  # Increase figure size for better readability
    sns.heatmap(
        cm,
        annot=annot,  # Annotate only non-zero counts
        fmt="",       # String formatting for annotations
        cmap="Blues",
        xticklabels=labels,
        yticklabels=labels,
        cbar=True,
        annot_kws={"color": "black", "size": 10}
    )
    plt.xlabel('Predicted Classification')
    plt.ylabel('True Classification')
    plt.title('Confusion Matrix')

    # Save the confusion matrix plot as a PDF
    plt.tight_layout()
    plt.savefig(output_pdf, format='pdf', dpi=300)
    print(f"Confusion matrix saved as {output_pdf}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a confusion matrix for ProTaX results.')
    parser.add_argument('--input', help='Input CSV file with ProTaX results', required=True)
    parser.add_argument('--output', help='Output .PDF file for confusion matrix', required=True)
    args = parser.parse_args()

    generate_confusion_matrix(args.input, args.output)