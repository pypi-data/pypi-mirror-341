import argparse
import seaborn as sns
import matplotlib.pyplot as plt

import math
import numpy as np
import pysam



def read_bias_report(fn_bias_report):
    list_bias_SNP = []
    list_bias_gap = []
    f = open(fn_bias_report, 'r')
    header = f.readline()
    for line in f:
        fields = line.split()
        if fields[-1] == '.':
            list_bias_gap.append(fields)
        else:
            list_bias_SNP.append(fields)
    f.close()
    return list_bias_SNP, list_bias_gap


def calculate_SNP_balance(assign_SNP, flag_real):
    """
    Return for simulated read:
    [[simulate_balance], [map_balance], [assign_balance]]
    Return for real read:
    [assign_balance]
    """
    if flag_real:
        record = [[float(fields[5]) for fields in assign_SNP]]
    else:
        record = [[],[],[]]
        for idx in range(len(assign_SNP)):
            record[0].append(float(assign_SNP[idx][14]))
            record[1].append(float(assign_SNP[idx][10]))
            record[2].append(float(assign_SNP[idx][5]))
    return record


def calculate_gap_balance(assign_gap, len_bd, get_idx):
    list_insert = [ [] for _ in range(len_bd) ]
    list_delete = [ [] for _ in range(len_bd) ]
    for idx in range(len(assign_gap)):
        # VCF_LENGTH is at index 10, EFFECTIVE_LENGTH at index 11
        length = int(assign_gap[idx][10])  # Using VCF_LENGTH by default
        if length > 0: # insertion
            diff = min(length - 1, len_bd-1)  # anything >= len_bd goes to last bin
            record = float(assign_gap[idx][get_idx])
            list_insert[diff].append(record)
        else: # deletion
            diff = min(abs(length) - 1, len_bd-1)  # anything >= len_bd goes to last bin
            record = float(assign_gap[idx][get_idx])
            list_delete[diff].append(record)
    return list_insert, list_delete


def addlabels(x, y, len_bd):
    for i in range(len(x)):
        # Format numbers: use 'k' for values ≥1000, no decimal points
        if y[i] >= 1000:
            label = f'{int(y[i]/1000)}k'
        else:
            label = str(int(y[i]))
        plt.text(i-len_bd, y[i], label, ha='center', va='bottom', fontsize=8)  # Added 30 degree rotation


def plot_balance(balance_delete, balance_SNP, balance_insert, output_name, len_bd, list_incidents, list_plot_name, use_median=False):
    len_plot = len(list_plot_name)
    balance_list = [np.zeros(2*len_bd+1) for idx in range(len_plot)]
    balance_25th = [np.zeros(2*len_bd+1) for idx in range(len_plot)]
    balance_75th = [np.zeros(2*len_bd+1) for idx in range(len_plot)]
    
    # Process deletions
    for idy, list_delete in enumerate(balance_delete):
        for idx in range(len_bd):
            list_balance = np.array(list_delete[idx])
            if len(list_balance) > 1:
                valid_balance = list_balance[~np.isnan(list_balance)]
                # Calculate 1 - value for all statistics
                flipped_balance = 1 - valid_balance
                balance_list[idy][len_bd-1-idx] = np.median(flipped_balance) if use_median else np.mean(flipped_balance)
                # Note: when we flip values, 75th becomes 25th and vice versa
                balance_25th[idy][len_bd-1-idx] = np.quantile(flipped_balance, 0.25)  # Was 0.75
                balance_75th[idy][len_bd-1-idx] = np.quantile(flipped_balance, 0.75)  # Was 0.25
            else:
                balance_list[idy][len_bd-1-idx] = np.nan
                balance_25th[idy][len_bd-1-idx] = np.nan
                balance_75th[idy][len_bd-1-idx] = np.nan
    
    # Process SNPs
    for idy, list_balance in enumerate(np.array(balance_SNP)):
        valid_balance = list_balance[~np.isnan(list_balance)]
        flipped_balance = 1 - valid_balance
        balance_list[idy][len_bd] = np.median(flipped_balance) if use_median else np.mean(flipped_balance)
        balance_25th[idy][len_bd] = np.quantile(flipped_balance, 0.25)  # Was 0.75
        balance_75th[idy][len_bd] = np.quantile(flipped_balance, 0.75)  # Was 0.25
    
    # Process insertions
    for idy, list_insert in enumerate(balance_insert):
        for idx in range(len_bd):
            list_balance = np.array(list_insert[idx])
            if len(list_balance) > 1:
                valid_balance = list_balance[~np.isnan(list_balance)]
                flipped_balance = 1 - valid_balance
                balance_list[idy][len_bd+1+idx] = np.median(flipped_balance) if use_median else np.mean(flipped_balance)
                balance_25th[idy][len_bd+1+idx] = np.quantile(flipped_balance, 0.25)  # Was 0.75
                balance_75th[idy][len_bd+1+idx] = np.quantile(flipped_balance, 0.75)  # Was 0.25
            else:
                balance_list[idy][idx+len_bd+1] = np.nan
                balance_25th[idy][idx+len_bd+1] = np.nan
                balance_75th[idy][idx+len_bd+1] = np.nan

    t = list(range(-len_bd, len_bd+1))
    f, (a0, a1) = plt.subplots(2, 1, gridspec_kw={
        'height_ratios': [3, 1],
        'hspace': 0.1
    })
    f.set_size_inches(20, 10)  # Slightly taller to accommodate labels
    
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    
    # Adjust the subplot parameters to give specified padding
    f.subplots_adjust(right=0.85, hspace=0.1)  # Make room for legend on right
    
    for idx, name in enumerate(list_plot_name):
        # Calculate error bar lengths
        yerr_minus = balance_list[idx] - balance_25th[idx]
        yerr_plus = balance_75th[idx] - balance_list[idx]
        yerr = np.vstack((yerr_minus, yerr_plus))
        
        # Plot with asymmetric error bars
        a0.errorbar(t, balance_list[idx],  # Removed (1-balance_list[idx]) since we already flipped
                   yerr=yerr, 
                   capsize=3, fmt='-o', label=name, color=colors[idx],
                   markersize=6, elinewidth=1, capthick=1)
    
    # Move legend inside the upper panel, near the bottom
    a0.legend(frameon=True, fancybox=True, framealpha=0.9,
              loc='lower center',  # Place at bottom center
              bbox_to_anchor=(0.5, 0.05),  # Position slightly above bottom
              ncol=2)  # Two columns for better space usage
    
    a0.axhline(y=0.5, color='gray', linestyle='dashdot', linewidth=0.9)
    a0.set(ylabel='Fraction of alternate allele')
    a0.grid(True, linestyle='--', alpha=0.3)
    
    a1.set(xlabel='Insertion (+) or deletion (-) length')
    a1.set(ylabel='# of variants')
    
    # Increase bar width
    width = 0.65  # Changed from 0.5 to 0.8 for thicker bars
    bars = a1.bar(t, list_incidents, align='center', width=width, log=True, linewidth=1)
    a1.set_ylim([1, max(list_incidents)*5])
    
    # Create x-ticks only for multiples of 5 and boundaries
    xticks = []
    xticklabels = []
    for x in range(-len_bd, len_bd + 1):
        if x == -len_bd or x == len_bd or x % 5 == 0:
            xticks.append(x)
            if x == -len_bd:
                xticklabels.append(f"≤-{len_bd}")
            elif x == len_bd:
                xticklabels.append(f"≥{len_bd}")
            else:
                xticklabels.append(str(x))
    
    a1.set_xticks(xticks)
    a1.set_xticklabels(xticklabels)  # Remove rotation
    
    # Use the same x-ticks for the upper plot
    a0.set_xticks(xticks)
    a0.set_xticklabels(xticklabels)  # Remove rotation
    
    addlabels(t, list_incidents, len_bd)
    a1.grid(axis='y', linestyle='--', alpha=0.3)
    
    a0.set_xlim(a1.get_xlim())
    
    # Adjust subplot spacing
    f.subplots_adjust(hspace=0.1)  # Keep minimal space between plots
    
    plt.savefig(output_name + '.indel_balance.pdf', bbox_inches='tight', dpi=300)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-lr', '--list_report', nargs='+', required=True, help='the list of assignment bias report')
    parser.add_argument('-ln', '--list_name',   nargs='+', required=True, help='the second bias report')
    parser.add_argument('-bd', '--boundary', type=int, default=40, help='the boundary indel lengths extend from 0')
    parser.add_argument('-map', '--flag_mapping', action='store_true', help='show the mapping rather than local result')
    parser.add_argument('-real', '--flag_real', action='store_true', help='specify if the report contains no simulation information')
    parser.add_argument('-out', '--output_name', help="output file name")
    parser.add_argument('-median', '--use_median', action='store_true', help='Use median instead of mean for central tendency')
    parser.add_argument('-l', '--length_type', choices=['VCF', 'EFFECTIVE'], default='VCF',
                       help='Which length to use for stratification (VCF_LENGTH or EFFECTIVE_LENGTH)')
    args = parser.parse_args()

    # Remove vcf argument and its usage
    fn_vcf = None

    list_report = args.list_report
    list_name   = args.list_name
    boundary = args.boundary
    flag_map = args.flag_mapping
    flag_real = args.flag_real
    output_name = args.output_name
    if output_name == None:
        output_name = list_name[0]

    assert len(list_report) == len(list_name), "Number of bias_report and bias names are different."
    
    # read the bias report
    list_bias_report = []
    for fn_assign_report in list_report:
        assign_report = read_bias_report(fn_assign_report)
        list_bias_report.append(assign_report)
    
    # fetch the SNP balance information
    list_balance_SNP = []
    for assign_SNP, assign_gap in list_bias_report:
        balance_SNP = calculate_SNP_balance(assign_SNP, flag_real)
        list_balance_SNP.append(balance_SNP)

    if flag_real: # no simulation of mapping information provided
        list_plot_name = list_name #[name + '(real)' for name in list_name]
        
        # fetch the gap balance information
        list_balance_delete = []
        list_balance_insert = []
        for assign_SNP, assign_gap in list_bias_report:
            balance_insert, balance_delete = calculate_gap_balance(assign_gap, boundary, 5)
            list_balance_insert.append(balance_insert)
            list_balance_delete.append(balance_delete)

        balance_SNP    = list_balance_SNP
        balance_delete = list_balance_delete
        balance_insert = list_balance_insert
    else: # to plot the simulated reads, the first entry is the simulated balance information, then we can choose map or local_assignment
        flag_choice = 2
        gap_choice  = 5
        list_plot_name = ["simulated"]
        if flag_map:
            flag_choice = 1
            gap_choice  = 10
            list_plot_name += [name + '(map)' for name in list_name]
        else:
            list_plot_name += [name + '(assign)' for name in list_name]
    
        # fetch the gap balance information
        balance_insert, balance_delete = calculate_gap_balance(list_bias_report[0][1], boundary, 14) # getting the simulated information
        list_balance_delete = [balance_delete]
        list_balance_insert = [balance_insert]
        for assign_SNP, assign_gap in list_bias_report:
            balance_insert, balance_delete = calculate_gap_balance(assign_gap, boundary, gap_choice)
            list_balance_insert.append(balance_insert)
            list_balance_delete.append(balance_delete)

        balance_SNP    = [list_balance_SNP[0][0]] + [balance[flag_choice] for balance in list_balance_SNP]
        balance_delete = list_balance_delete
        balance_insert = list_balance_insert
    

    # get the incident numbers of the indels
    list_incidents = []
    # Add deletion counts (reversed)
    for balance in list_balance_delete[0][::-1]:
        list_incidents.append(len(balance))
    # Add SNP count
    list_incidents.append(len(list_balance_SNP[0][0]))
    # Add insertion counts
    for balance in list_balance_insert[0]:
        list_incidents.append(len(balance))
    
    plot_balance(balance_delete, balance_SNP, balance_insert, output_name, boundary, list_incidents, list_plot_name, args.use_median)

