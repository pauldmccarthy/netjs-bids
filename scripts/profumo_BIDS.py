#!/usr/bin/env python3
import argparse
import os
import shutil
import csv
import sys
from glob import glob
import pdb
import json
import numpy

# import nibabel
# from subprocess import Popen, PIPE
# from shutil import rmtree
# import subprocess
from warnings import warn

def profumo_BIDS(profumo_dir,bids_dir):
 
    os.makedirs(bids_dir,exist_ok=True)

    profumo_BIDS_dir=os.path.join(bids_dir,'derivatives','profumo')
    os.makedirs(profumo_BIDS_dir,exist_ok=True)

    #csv.writer(open(os.path.join(profumo_BIDS_dir,'conndata-network_connectivity.tsv'), 'w'), delimiter="\t").writerows(csv.reader(open(os.path.join(profumo_dir,'NetMats','NetMats.csv'))))
    netMat = numpy.loadtxt(os.path.join(profumo_dir,'NetMats','NetMats.csv'),delimiter=',')

    ndims = int(numpy.round(-0.5 + numpy.sqrt(0.5+2*netMat.shape[1])))
    netMatIndsU = numpy.triu_indices(ndims, 1)
    netMatIndsL = numpy.triu_indices(ndims, 1)

    for subj in range(netMat.shape[0]):
        omat=numpy.zeros((ndims,ndims))
        omat[netMatIndsU] = netMat[subj,ndims:]
        #omat.T[netMatIndsU] = netMat[subj,:]
        outFileName=os.path.join(profumo_BIDS_dir,'conndata-network_netmat-'+str(subj).zfill(5)+'_connectivity')
        numpy.savetxt(outFileName+'.tsv',omat,delimiter="\t")

        out_json_file = open(outFileName+'.json','w')
        out_json={'measure':'Correlation','label':'Subject'+str(subj).zfill(5)}
        json.dump(out_json,out_json_file)
        out_json_file.close()
    os.makedirs(os.path.join(profumo_BIDS_dir,'Maps'),exist_ok=True)

    # GroupMaps=sorted(glob(os.path.join(profumo_dir,'Maps','Mode_*SubjectMaps*')))

    os.makedirs(os.path.join(profumo_BIDS_dir,'Maps','GroupMaps.sum'),exist_ok=True)
    GroupMaps_thumbs=sorted(glob(os.path.join(profumo_dir,'Maps','GroupMaps.sum/*png')))

    #cnt=0
    #for map in GroupMaps:
    #    shutil.copy(map ,os.path.join(profumo_BIDS_dir,'Maps','conndata-node_index-'+str(cnt).zfill(5)+'_mode.nii.gz'))
    #    cnt+=1

    shutil.copy(os.path.join(profumo_dir,'Maps','GroupMaps.nii.gz'),os.path.join(profumo_BIDS_dir,'Maps','conndata-modes.nii.gz'))

    cnt=0
    for map in GroupMaps_thumbs:
        shutil.copy(map ,os.path.join(profumo_BIDS_dir,'Maps','GroupMaps.sum','conndata-node_index-'+str(cnt).zfill(5)+'_thumbnail.png'))
        cnt+=1

    out_json_file = open(os.path.join(profumo_BIDS_dir,'connectivity.json'),'w')
    out_json={'measure':'Correlation','label':'PROFUMO'}
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
    
    out = profumo_BIDS(args.input_dir,args.bids_dir)

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


