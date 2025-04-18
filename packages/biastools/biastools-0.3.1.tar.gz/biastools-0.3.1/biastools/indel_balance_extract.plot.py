import argparse
import numpy as np
import pysam
import matplotlib.pyplot as plt
from math import ceil

def read_bias_report(fn_bias_report):
    """Read bias report and separate SNP and gap entries"""
    list_bias_SNP = []
    list_bias_gap = []
    with open(fn_bias_report, 'r') as f:
        header = f.readline()
        for line in f:
            fields = line.split()
            if fields[-1] == '.':
                list_bias_gap.append(fields)
            else:
                list_bias_SNP.append(fields)
    return list_bias_SNP, list_bias_gap

def get_indel_size(ref_name, var_start, f_vcf):
    """Get indel size from VCF file"""
    var_segment = f_vcf.fetch(contig=ref_name, start=var_start-1, stop=var_start+1)
    for var in var_segment:
        if var.start + 1 != var_start:
            continue
        len_ref = len(var.ref)
        if len(var.alts) == 1:
            len_alt = len(var.alts[0])
        else:
            hap = var.samples[0]['GT']
            if hap[0] != 0:
                len_alt = len(var.alts[hap[0]-1])
            else:
                len_alt = len(var.alts[hap[1]-1])
        return len_alt - len_ref - 1
    return None

def plot_single_distribution(ax, balance_values, indel_size, boundary):
    """Create distribution plot with percentile lines for a single subplot"""
    if len(balance_values) == 0:
        ax.text(0.5, 0.5, 'No variants', ha='center', va='center')
        ax.set_title(f'Size {"≥" if indel_size == boundary else ""}{indel_size:+d}')
        return

    valid_balances = balance_values[~np.isnan(balance_values)]
    if len(valid_balances) == 0:
        ax.text(0.5, 0.5, 'No valid balance values', ha='center', va='center')
        ax.set_title(f'Size {"≥" if indel_size == boundary else ""}{indel_size:+d}')
        return

    # Calculate statistics
    median = np.median(valid_balances)
    percentile_25 = np.quantile(valid_balances, 0.25)
    percentile_75 = np.quantile(valid_balances, 0.75)
    
    # Create histogram
    n, bins, patches = ax.hist(valid_balances, bins=10, range=(0, 1), 
                              edgecolor='black', alpha=0.7)
    
    # Add percentile lines
    ax.axvline(x=median, color='red', linestyle='--', label=f'Median ({median:.3f})')
    ax.axvline(x=percentile_25, color='green', linestyle='--', label=f'25th ({percentile_25:.3f})')
    ax.axvline(x=percentile_75, color='blue', linestyle='--', label=f'75th ({percentile_75:.3f})')
    
    # Add counts above bars with larger font
    for i, count in enumerate(n):
        ax.text(bins[i] + (bins[i+1] - bins[i])/2, count, 
                str(int(count)), ha='center', va='bottom', fontsize=10)
    
    # Set title and grid
    size_label = f'{"≥" if indel_size == boundary else ""}{indel_size:+d}'
    ax.set_title(f'Size {size_label} (n={len(valid_balances)})', fontsize=12)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Set x and y labels with larger font
    ax.set_xlabel('Allelic Balance', fontsize=10)
    ax.set_ylabel('Number of Variants', fontsize=10)


def main():
    parser = argparse.ArgumentParser(description="Create distribution plots for allelic balance of all indel sizes")
    parser.add_argument('-i', '--input', required=True, help='Input bias report file')
    parser.add_argument('-vcf', '--vcf_file', required=True, help='VCF file for indel size information')
    parser.add_argument('-bd', '--boundary', type=int, default=25, help='Boundary for aggregating larger indel sizes (default: 25)')
    parser.add_argument('-o', '--output', required=True, help='Output prefix for PDF file')
    args = parser.parse_args()

    # Open VCF file
    f_vcf = pysam.VariantFile(args.vcf_file)

    # Read bias report
    bias_SNP, bias_gap = read_bias_report(args.input)

    # Create dictionary to store balance values for each indel size
    indel_balances = {}
    
    # Process all entries
    for entry in bias_gap:
        ref_name = entry[0]
        var_start = int(entry[1])
        
        indel_size = get_indel_size(ref_name, var_start, f_vcf)
        if indel_size is not None:
            # Aggregate sizes larger than boundary
            if abs(indel_size) > args.boundary:
                if indel_size > 0:
                    indel_size = args.boundary
                else:
                    indel_size = -args.boundary
                    
            if indel_size not in indel_balances:
                indel_balances[indel_size] = []
            indel_balances[indel_size].append(float(entry[5]))

    # Create plots
    indel_sizes = sorted(indel_balances.keys())
    n_plots = len(indel_sizes)
    n_cols = 5  # Number of columns in the grid
    n_rows = ceil(n_plots / n_cols)

    # Create figure
    fig = plt.figure(figsize=(24, 6*n_rows))  # Increased figure width and height per row

    # Add a main title
    fig.suptitle(f'Distribution of Allelic Balance by Indel Size (Aggregated at ±{args.boundary})',
                 fontsize=16, y=0.95)

    # Create subplots with more space between them
    for idx, size in enumerate(indel_sizes):
        ax = plt.subplot(n_rows, n_cols, idx + 1)
        plot_single_distribution(ax, np.array(indel_balances[size]), size, args.boundary)

        # Add legend only to the first plot with larger font
        if idx == 0:
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

    # Adjust layout with more space between subplots
    plt.tight_layout(rect=[0, 0.03, 1, 0.95], h_pad=0.5, w_pad=0.5)
    
    # Save plot
    plt.savefig(f'{args.output}.balance_dist.pdf', bbox_inches='tight', dpi=300)
    plt.close()

    print(f"\nAnalysis complete:")
    print(f"Created distribution plots for indel sizes (aggregated at ±{args.boundary})")
    print(f"Plot saved as: {args.output}.balance_dist.pdf")

if __name__ == "__main__":
    main()
