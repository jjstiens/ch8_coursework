
#!/usr/bin python3

""" Whole Genome Codon Usage program """

"""
Program:        whole_genome_freq
File:           whole_genome_freq.py

Version:        1.0
Date:           18.04.18
Function:       Returns codon usage ratio and percentage for entire chromosome.

Author:         Jennifer J Stiens
                j.j.stiens@gmail.com
                https://github.com/jenjane118/ch8_coursework

Course:         MSc Bioinformatics, Birkbeck University of London
                Biocomputing 2 Coursework

______________________________________________________________________________

Description:
============
This program will calculate codon usage frequency, percentage, and ratio of codon usage preference for entire chromosome.

Usage:
======
whole_genome_freq

Revision History:
=================


V1.0           18.04.18         Original            By: JJS
V1.1           1.05.18          changed output          JJS
V1.2           2.05.18          reworked as function    JJS
V1.3           4.05.18          added bias function     JJS
"""
#*****************************************************************************
# Import libraries

import gene_module
import seq_module
import codon_usage
from data_access import list_query

from xml.dom import minidom

#****************************************************************************
def help():
    """Print a usage message and exit."""
    print("""
    codon_usage.py   V1.3        2018,   J.J. Stiens

    Usage: 
    ============
    codon_usage 

    Description:
    ============
    Calculate codon usage percentage, and ratio of codon usage preference for entire chromosome
    First dictionary is amino acid: list of synonymous codons
    Second dictionary is codons: ratio, percent
    """)
    exit(0)

#****************************************************************************

def total_usage():
    """Return genome usage information for entire database of genes.
    Input               self
    Output              (SynCodons, usage_dict)         Dictionary of synonymous codons for each amino acid
                                                        Dictionary of codon: ratio, percent usage statistics

    """
    genbank = list_query.genbank_query()
    for gene in genbank:
        acc = gene[0]
        genid = gene[1]
        product = gene[2]
        location = gene[3]

        ## Uses initialisation function to create a gene object for each listing from database
        gene_object = gene_module.Gene(acc, genid, product, location)

    object_dict = {}  # individual object dictionary of identifiers
    chrom_dict = {}  # chromosome dictionary of all gene objects
    total_freq = {}
    ## Create a dictionary of gene objects
    for object in gene_module.Gene._registry:
        object_dict = gene_module.Gene.geneList(object)

        ## use coding seq function to determine coding sequence for each gene
        for k, v in object_dict.items():
            chrom_dict[k] = v

    for k in chrom_dict:
        coding_dna = seq_module.codingSeq(k)

        ##  call function to determine codon frequency for each gene
        codon_table = codon_usage.codonFreq(coding_dna)

        ##  add each to total codon frequency dictionary
        for key in codon_table:
            if key in total_freq:
                total_freq[key] += codon_table[key]
            else:
                total_freq[key] = codon_table[key]

    print(total_freq)
    ## calculate codon usage ratio for whole genome (returns dictionary, 'whole_genome_ratio')
    gene = 'total'
    whole_genome_ratio = codon_usage.usageRatio(total_freq)

    SynCodons = {
        'C': ['TGT', 'TGC'],
        'D': ['GAT', 'GAC'],
        'S': ['TCT', 'TCG', 'TCA', 'TCC', 'AGC', 'AGT'],
        'Q': ['CAA', 'CAG'],
        'M': ['ATG'],
        'N': ['AAC', 'AAT'],
        'P': ['CCT', 'CCG', 'CCA', 'CCC'],
        'K': ['AAG', 'AAA'],
        'T': ['ACC', 'ACA', 'ACG', 'ACT'],
        'F': ['TTT', 'TTC'],
        'A': ['GCA', 'GCC', 'GCG', 'GCT'],
        'G': ['GGT', 'GGG', 'GGA', 'GGC'],
        'I': ['ATC', 'ATA', 'ATT'],
        'L': ['TTA', 'TTG', 'CTC', 'CTT', 'CTG', 'CTA'],
        'H': ['CAT', 'CAC'],
        'R': ['CGA', 'CGC', 'CGG', 'CGT', 'AGG', 'AGA'],
        'W': ['TGG'],
        'V': ['GTA', 'GTC', 'GTG', 'GTT'],
        'E': ['GAG', 'GAA'],
        'Y': ['TAT', 'TAC'],
        '_': ['TAG', 'TGA', 'TAA']}

    ## calculate codon usage percent (usage per 100bp) for whole genome (returns dictionary, 'whole_genome_percent')
    whole_genome_percent = codon_usage.codonPercent(total_freq)

    ## make a list of codons and ratios (separate from aa key)
    ratio_list = []
    ratio_dict = {}
    usage_dict = {}
    for k, v in whole_genome_ratio.items():
        ratio_list.append(v)
    ## make new dictionary with codon:ratio
    for item in ratio_list:
        for k,v in item.items():
            ratio_dict[k] = v
    ## create dictionary listing codon: ratio, percent
    for codon, ratio in ratio_dict.items():
        for codon, percent in whole_genome_percent.items():
            usage_dict[codon] = ratio_dict[codon], percent

    return SynCodons, usage_dict

#****************************************************************************

def codon_compare(acc):
    """ Return rough comparison of codon usage ratios between gene and whole chromosome
    Input                       acc                 Accession number of gene of interest

    Output                      bias_list           List of codons in specified gene that have ratios that differ by
                                                    more than 50% from codon usage ratio chromosome-wide
    """

    # for gene of interest
    results = codon_usage.getCodonusage(acc)
    gene_stats = results[1]

    codons_dictionary = total_usage()
    wgf_stats = codons_dictionary[1]

    bias_list = []
    for k in gene_stats:
        if k in wgf_stats:
            ratio_gene = gene_stats[k][0]
            ratio_wgf = wgf_stats[k][0]
            if ratio_gene - ratio_wgf >= abs(.5):
                bias_list.append(k)

    return bias_list

#****************************************************************************

## main ##

if __name__ =="__main__":

    codons_dictionary = total_usage()

    print(codons_dictionary[0])
    print(codons_dictionary[1])

    gene = 'AB000381.1'
    results = codon_compare(gene)

    for x in results:
        print(x, 'Possible codon bias')

    #write to file
    f = open('whole_genome_usage.txt', 'w')
    print(codons_dictionary[0], file=f)
    print(codons_dictionary[1], file=f)
    f.close()