#! /usr/bin/env python

from os import path
dir_script = path.dirname(path.realpath(__file__))
import sys
sys.path.append(dir_script+'/../')
import pydssp
import torch
import tqdm
import pdbbasic as pdbb



from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
argparse = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
argparse.add_argument('pdbs', nargs='+', type=str, help='Input PDB file')
argparse.add_argument('--device', '-d', type=str, default=None, help='Device')
argparse.add_argument('--output-file', '-o', type=str, default=None, help='Output file')
args = argparse.parse_args()

if args.device == None:
    args.device = 'cuda' if torch.cuda.is_available() else 'cpu'

fh = open(args.output_file, 'w') if args.output_file is not None else sys.stdout

for pdb in tqdm.tqdm(args.pdbs):
    # read pdb file
    coord = torch.Tensor(pdbb.readpdb(pdb, atoms=['N','CA','C','O']))
    coord = coord.to(args.device)
    # main calculation
    dssp = pydssp.assign(coord)
    # output
    fh.write(f"{''.join(dssp)} {pdb}\n")
