import argparse
import numpy as np
import pysam

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

def main():
    parser = argparse.ArgumentParser(description="Extract and analyze indels of specific size from bias report")
    parser.add_argument('-i', '--input', required=True, help='Input bias report file')
    parser.add_argument('-vcf', '--vcf_file', required=True, help='VCF file for indel size information')
    parser.add_argument('-s', '--size', type=int, default=3, help='Indel size to analyze (default: 3)')
    parser.add_argument('-o', '--output', help='Output file for filtered bias report')
    args = parser.parse_args()

    # Open VCF file
    f_vcf = pysam.VariantFile(args.vcf_file)

    # Read bias report
    bias_SNP, bias_gap = read_bias_report(args.input)

    # Extract indels of specified size
    target_variants = []
    balance_values = []

    print(f"\nAnalyzing indels of size +{args.size}")
    print("-" * 50)

    for entry in bias_gap:
        ref_name = entry[0]
        var_start = int(entry[1])

        indel_size = get_indel_size(ref_name, var_start, f_vcf)

        if indel_size == args.size:
            target_variants.append(entry)
            balance_values.append(float(entry[5]))  # Assuming balance is in column 6

    # Convert to numpy array and handle NaN values
    balance_array = np.array(balance_values)
    valid_balances = balance_array[~np.isnan(balance_array)]

    # Calculate statistics
    if len(valid_balances) > 0:
        median = np.median(valid_balances)
        percentile_25 = np.quantile(valid_balances, 0.25)
        percentile_75 = np.quantile(valid_balances, 0.75)

        print(f"Number of +{args.size} indels found: {len(balance_values)}")
        print(f"Number of valid balance values: {len(valid_balances)}")
        print("\nStatistics:")
        print(f"Median balance: {median:.3f}")
        print(f"25th percentile: {percentile_25:.3f}")
        print(f"75th percentile: {percentile_75:.3f}")

        print("\nSorted valid balance values:")
        print(", ".join(f"{x:.3f}" for x in sorted(valid_balances)))

        if len(balance_values) != len(valid_balances):
            print(f"\nNote: {len(balance_values) - len(valid_balances)} entries had NaN values and were excluded")
    else:
        print(f"No valid balance values found for indels of size +{args.size}")

    # Write filtered report if output file specified
    if args.output and target_variants:
        with open(args.input, 'r') as f_in, open(args.output, 'w') as f_out:
            # Copy header
            header = f_in.readline()
            f_out.write(header)

            # Write filtered entries
            for entry in target_variants:
                f_out.write('\t'.join(entry) + '\n')
        print(f"\nFiltered bias report written to: {args.output}")

if __name__ == "__main__":
    main()
