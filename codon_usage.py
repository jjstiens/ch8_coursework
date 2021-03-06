#!/usr/bin python3

""" Codon Usage Module """

"""
Program:        codon_usage
File:           codon_usage.py

Version:        1.0
Date:           22.03.18
Function:       Module for calculating codon frequency,codon usage ratio and percentage for a particular sequence.

Author:         Jennifer J Stiens
                j.j.stiens@gmail.com
                https://github.com/jenjane118/ch8_coursework

Course:         MSc Bioinformatics, Birkbeck University of London
                Biocomputing 2 Coursework

______________________________________________________________________________

Description:
============
This program will calculate codon usage frequency, percentage, and ratio of codon usage preference for a particular sequence.


Usage:
======


Revision History:
=================

V1.0           22.03.18         Original                                By: JJS
V1.1           18.04.18         Renamed (from 'Codon_Usage_module')         JJS
V1.2           22.04.18         Fixed bugs with uppercase and zero division JJS
                                
"""
#**********************************************************************************
# Import libraries
import sys
import seq_module

#**********************************************************************************

def codonFreq(dna):
    """Return frequency of each codon possibility in particular sequence.
    Input       acc                     accession number
                dna                     coding sequence (dna)

    Output      CodonsDict              dictionary of codon frequencies in sequence
    """

    CodonsDict = {
        'TTT': 0, 'TTC': 0, 'TTA': 0, 'TTG': 0, 'CTT': 0,
        'CTC': 0, 'CTA': 0, 'CTG': 0, 'ATT': 0, 'ATC': 0,
        'ATA': 0, 'ATG': 0, 'GTT': 0, 'GTC': 0, 'GTA': 0,
        'GTG': 0, 'TAT': 0, 'TAC': 0, 'TAA': 0, 'TAG': 0,
        'CAT': 0, 'CAC': 0, 'CAA': 0, 'CAG': 0, 'AAT': 0,
        'AAC': 0, 'AAA': 0, 'AAG': 0, 'GAT': 0, 'GAC': 0,
        'GAA': 0, 'GAG': 0, 'TCT': 0, 'TCC': 0, 'TCA': 0,
        'TCG': 0, 'CCT': 0, 'CCC': 0, 'CCA': 0, 'CCG': 0,
        'ACT': 0, 'ACC': 0, 'ACA': 0, 'ACG': 0, 'GCT': 0,
        'GCC': 0, 'GCA': 0, 'GCG': 0, 'TGT': 0, 'TGC': 0,
        'TGA': 0, 'TGG': 0, 'CGT': 0, 'CGC': 0, 'CGA': 0,
        'CGG': 0, 'AGT': 0, 'AGC': 0, 'AGA': 0, 'AGG': 0,
        'GGT': 0, 'GGC': 0, 'GGA': 0, 'GGG': 0}


    # format sequence to unbroken uppercase string
    dna = dna.upper()
    # divide sequence into a list of codons
    codon = ''
    codon_list = []
    for s in dna:
        codon += s
        if len(codon) == 3:
            codon_list.append(codon)
            codon = ''

    # Update dictionary for codon frequencies
    for x in codon_list:
         if x in CodonsDict:
             CodonsDict[x] += 1
    return CodonsDict

#**********************************************************************************

def codonPercent (freq_table):
    """Return percentage use of a particular codon in sequence (per 100 bp sequence)
    Input           acc                 Accession number
                    freq_table          Codon frequency dictionary

    Output          percentDict         Dictionary of codon and usage per 100bp
    """

    total_codons = 0
    percentDict = {}
    for codon in freq_table:
        total_codons += freq_table[codon]
    for codon in freq_table:
        try:
            percent = (freq_table[codon] / total_codons)*100
            percentDict[codon] = round(percent, 1)
        ## if there is no sequence returned:
        except ZeroDivisionError:
            print('Sequence not found')
            break
    return percentDict

#**********************************************************************************

def usageRatio (freq_table):
    """Returs codon usage ratio.
    Input       acc             Accession number
                freq_table      Codon frequency dict returned from codonFreq function

    Output      aaDict          Dictionary of amino acids: codons used and ratio of codon usage
    """

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

    aa_list = ['C', 'D', 'S', 'Q', 'M', 'N', 'P', 'K', 'T', 'F', 'A', 'G', 'I', 'L', 'H', 'R', 'W', 'V', 'E', 'Y', '_']



    aaDict = {}
    for aa in aa_list:
        if aa in SynCodons:
            codon_list = SynCodons[aa]
            sum = 0
            ratio = 0
            codonDict = {}
            for x in codon_list:
                sum += freq_table[x]
            for x in codon_list:
                ## to avoid zero division error
                if sum == 0:
                    ratio = 0.0
                else:
                    ratio = (freq_table[x]) / sum
                codonDict[x] = round(ratio, 2)
        aaDict[aa] = codonDict

    return aaDict

#**********************************************************************************

def getCodonusage(acc):
    """Return codon frequency, codon usage ratio and percentage for a particular gene.
    Input                   acc                                     Gene accession number
    Output                  (usage_dict, aa_dict)                   amino acid:codon dict
                                                                    codon usage(ratio, percent)

    26.04.18                Original                                By: JJS

    """
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

    code_seq = seq_module.codingSeq(acc)

    ## calculate raw frequencies of codon usage
    codon_freq = codonFreq(code_seq)

    ## find each amino acid codon usage ratio
    ratio = usageRatio(codon_freq)

    ## find percent usage (per 100 bp)
    percent = codonPercent(codon_freq)

    ratio_list = []
    ratio_dict = {}
    usage_dict = {}

    ## divide dictionary into list of codons and ratio
    for k, v in ratio.items():
        ratio_list.append(v)

    ## new dictionary with individual codons/ratio
    for item in ratio_list:
        for k, v in item.items():
            ratio_dict[k] = v

    ## dictionary listing codon: ratio, percent
    for codon, ratio in ratio_dict.items():
        for codon, freq in percent.items():
            usage_dict[codon] = ratio_dict[codon], freq

    return(SynCodons, usage_dict)

#**********************************************************************************

def help():
    """Print a usage message and exit."""
    print("""
    codon_usage.py   V1.2        2018,   J.J. Stiens

    Usage: 
    ============
    codon_usage     GENE

    Description:
    ============
    Calculate codon usage percentage, and ratio of codon usage preference for a particular sequence
    First dictionary is amino acid: list of synonymous codons
    Second dictionary is codons: ratio, percent
    """)
    exit(0)

#**********************************************************************************
### main #####

if __name__ == "__main__":
    print("Ran module directly (and did not 'import' it).")

    gene = 'AB000381.1'

    results = getCodonusage(gene)

    aa_codons = (results[0])
    ratio_percent = (results[1])

    print('amino acid   codon   ratio   percent')
    # to print amino acid/codon/ratio/percent
    for key in ratio_percent:
        for aa in aa_codons:
            if key in aa_codons[aa]:
                print(aa, '       :  ', key, '  : ', ratio_percent[key][0], '    ', ratio_percent[key][1])

   

