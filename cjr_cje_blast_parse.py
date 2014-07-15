#!/usr/bin/env python

'''In this script the Cje 11168 and Cjr DM1221 strains of the campylobacter
Jejuni were compared to distinguish the similarities of their genomes. First,
BLAST was run using the following commands:

    blastp -outfmt 6 -query NC_003912.faa -subject T00026.pep > cjr_against_cje.tsv
    blastp -outfmt 6 -query T00026.pep -subject NC_003912.faa > cje_against_cjr.tsv

Once the blast files were produced (the program takes a very long time to run,
the program was allowed to run over night) the two blast files, "cjr_against_cje"
and "cje_against_cjr," were read into the program followed by the "Cjr_network_rxn"
file and the "MetNet_reaction" file.

The BLAST files were parsed looking for the lowest e-value gene match with
a threshold of 60%. The genes that had no match were printed and counted. These
unmatched genes do not have homologs between the strains. The genes that had a
reciprical best BLAST hit were printed and counted. The homologues between the
two strains were then found by using the total amount of genes in each strain and 
subtracting the "shared/confirmed" and "unique" genes.'''

import argparse
import csv
import re
import sys
from collections import defaultdict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse blastp file to list Cjr and Cje percentage of matched amino acids sequences')
    parser.add_argument('cjr_against_cje', type=argparse.FileType('r'), help='Cjr against Cje')
    parser.add_argument('cje_against_cjr', type=argparse.FileType('r'), help='Cje against Cjr')
    parser.add_argument('Cjr_network_rxn', type=argparse.FileType('r'), help='Cjr_network_rxn')
    parser.add_argument('MetNet_reaction', type=argparse.FileType('r'), help='MetNet_reaction')

    args = parser.parse_args()

    r_e_file = args.cjr_against_cje
    e_r_file = args.cje_against_cjr
    cjr_network_file = args.Cjr_network_rxn
    metnet_file = args.MetNet_reaction

    cjr_reactions = set()
    cje_reactions = set()
    cjr_gene_map = defaultdict(set) # gi: rxnXXXXX
    cje_gene_map = defaultdict(set) # CjXXXX: ABCD
    cjr_reaction_map = defaultdict(set) # rxnXXXX: gi
    cje_reaction_map = defaultdict(set) # ABCD: CjXXXX

    cjr_network_file.readline()
    for row in csv.reader(cjr_network_file, delimiter='\t'):
        SEED_rid, RXN_name, EC, Equation_cpdid, Equation_cpdname, KEGG_rid, KEGG_maps, Gene_ids = row
        cjr_reactions.add(SEED_rid)
        for id in Gene_ids.split(','):
            cjr_gene_map[id].add(SEED_rid)
            cjr_reaction_map[SEED_rid].add(id)

    metnet_file.readline()
    for row in csv.reader(metnet_file, dialect='excel'):
        Reaction_abbreviation, Reaction_name, Equation, EC_number, Gene, Protein, H_pylori_ortholog, Pathway, Source, Notes = row
        cje_reactions.add(Reaction_abbreviation)
        for m in re.finditer(r'Cj\d+[a-z]?', Gene):
            cje_id = m.group(0)
            cje_gene_map[cje_id].add(Reaction_abbreviation)
            cje_reaction_map[Reaction_abbreviation].add(cje_id)

    gene_mapping = {}
    reaction_mapping = defaultdict(set)

    current_qid = None
    current_matches = []
    for row in csv.reader(r_e_file, delimiter='\t'):
        qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore = row
        gid = qseqid.split('|')[1]

        if float(pident) < 60 or float(evalue) > 1e-3:
            continue

        if gid != current_qid:
            # New id, save current best match
            if current_qid is not None:
                matches = sorted(current_matches, key=lambda x: x[1])
                best_match = matches[0][0]
                gene_mapping[current_qid] = best_match
            # Current id changes
            current_qid = gid
            current_matches = []

        cje_id = sseqid[4:]
        current_matches.append((cje_id, float(evalue)))
        

    for row1 in csv.reader(e_r_file, delimiter='\t'):
        qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore = row1
        cje_id = qseqid[4:]

        if float(pident) < 60 or float(evalue) > 1e-3 :
            continue

        if cje_id != current_qid:
            # New id, save current best match
            if current_qid is not None:
                matches = sorted(current_matches, key=lambda x: x[1])
                best_match = matches[0][0]
                gene_mapping[current_qid] = best_match
            # Current id changes
            current_qid = cje_id
            current_matches = []

        gid = sseqid.split('|')[1]
        current_matches.append((gid, float(evalue)))

    # Genes that appear to be unique to each model
    unique_cje_genes = set()
    unique_cjr_genes = set()
    print 'Genes that appear to be unique to each model:'
    for gene_id in cjr_gene_map.iterkeys():
        if gene_id not in gene_mapping:
            unique_cjr_genes.add(gene_id)
            print '{}\t{}'.format(gene_id, ','.join(cjr_gene_map[gene_id]))
    for gene_id in cje_gene_map.iterkeys():
        if gene_id not in gene_mapping:
            unique_cje_genes.add(gene_id)
            print '{}\t{}'.format(gene_id, ','.join(cje_gene_map[gene_id]))
    print 'Cjr unique: {}, Cje unique: {}'.format(len(unique_cjr_genes), len(unique_cje_genes))

    # Genes that appear to be shared
    shared_genes = set()
    shared_mapping = {}
    print 'Genes that appear to be shared:'
    for gene_id in cjr_gene_map.iterkeys():
        if gene_id in gene_mapping:
            best_match = gene_mapping[gene_id]
            if best_match in gene_mapping and gene_mapping[best_match] == gene_id:
                shared_genes.add(gene_id)
                shared_genes.add(best_match)
                shared_mapping[gene_id] = best_match
                shared_mapping[best_match] = gene_id
                
                print '{}\t{}'.format(gene_id, best_match)
    print 'Shared: {}'.format(len(shared_genes))

    # Genes with homologues
    print 'Genes that appear to be homologous'
    homolog_genes = set(cjr_gene_map.iterkeys()) | set(cje_gene_map.iterkeys())
    homolog_genes -= unique_cje_genes | unique_cjr_genes | shared_genes
    for gene_id in homolog_genes:
        if gene_id in cjr_gene_map:
            print '{}\thomologous to\t{}'.format(gene_id, gene_mapping[gene_id])
    for gene_id in homolog_genes:
        if gene_id in cje_gene_map:
            print '{}\thomologous to\t{}'.format(gene_id, gene_mapping[gene_id])
            
    print 'Homologues: {}'.format(len(homolog_genes))
    
    # Try to map reactions to reactions
    for rxnid in cjr_reaction_map.iterkeys():
        print rxnid
 #       cje_rid_set = set()
#        cje_gid_set = set()
        for cjr_gene_id in cjr_reaction_map[rxnid]: 
            if cjr_gene_id not in shared_mapping:
                print 'not in shared'
                print cjr_gene_id
            else:
                cje_gene_id = shared_mapping[cjr_gene_id]
                for cje_rxnid in cje_gene_map[cje_gene_id]:
#                    cje_rid_set.add(cje_rxnid)
#                    cje_gid_set.add(cje_gene_id)
                    print ' - {} ({})'.format(cje_rxnid, cje_gene_id)
            print