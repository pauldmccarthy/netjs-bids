#!/usr/bin/env python3
import argparse
import os
import shutil
import csv
import sys
from glob import glob
import pdb
import json

# import nibabel
# from subprocess import Popen, PIPE
# from shutil import rmtree
# import subprocess
from warnings import warn

def probtrackx_BIDS(probtrackx_dir,bids_dir):
 
    os.makedirs(bids_dir,exist_ok=True)

    probtrackx_BIDS_dir=os.path.join(bids_dir,'derivatives','probtrackx')
    os.makedirs(probtrackx_BIDS_dir,exist_ok=True)

    csv.writer(open(os.path.join(probtrackx_BIDS_dir,'conndata-network_connectivity.tsv'), 'w'), delimiter="\t").writerows(csv.reader(open(os.path.join(probtrackx_dir,'seed2seed','logdir','fdt_network_matrix'))))

    #os.makedirs(os.path.join(probtrackx_BIDS_dir,'Maps'),exist_ok=True)
    #os.makedirs(os.path.join(probtrackx_BIDS_dir,'Maps','GroupMaps.sum'),exist_ok=True)

    # GroupMaps=sorted(glob(os.path.join(probtrackx_dir,'Maps','Mode_*SubjectMaps*')))
    #GroupMaps_thumbs=sorted(glob(os.path.join(probtrackx_dir,'Maps','GroupMaps.sum/*png')))

    #cnt=0
    #for map in GroupMaps:
    #    shutil.copy(map ,os.path.join(probtrackx_BIDS_dir,'Maps','conndata-node_index-'+str(cnt).zfill(5)+'_mode.nii.gz'))
    #    cnt+=1

    #shutil.copy(os.path.join(probtrackx_dir,'Maps','GroupMaps.nii.gz'),os.path.join(probtrackx_BIDS_dir,'Maps','conndata-modes.nii.gz'))

    #cnt=0
    #for map in GroupMaps_thumbs:
    #    shutil.copy(map ,os.path.join(probtrackx_BIDS_dir,'Maps','GroupMaps.sum','conndata-node_index-'+str(cnt).zfill(5)+'_thumbnail.png'))
    #    cnt+=1

    out_json_file = open(os.path.join(probtrackx_BIDS_dir,'connectivity.json'),'w')
    out_json={'measure':'streamline_count','label':'probtrackx'}
    json.dump(out_json,out_json_file)
    out_json_file.close()

def main():

    sys.excepthook = info

    parser = argparse.ArgumentParser(description='PROFUMO BIDS output wrapper.')

    parser.add_argument('input_dir', help='The directory for the output dataset '
                        'formatted according to the BIDS standard.')
    parser.add_argument('bids_dir', help='The directory where the Profumo input files '
        'are stored.')

    args = parser.parse_args()
    
    out = probtrackx_BIDS(args.input_dir,args.bids_dir)

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def info(type, value, tb):
    if hasattr(sys, 'ps1') or not sys.stderr.isatty():
    # we are in interactive mode or we don't have a tty-like
    # device, so we call the default hook
        sys.__excepthook__(type, value, tb)
    else:
        import traceback, pdb
        traceback.print_exception(type, value, tb)
        print
        # pdb.pm() # deprecated
        pdb.post_mortem(tb)

if __name__ == "__main__":
    sys.exit(main())


