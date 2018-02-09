import sys
import os
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('-f','--fastq',type=str)
parser.add_argument('-g','--genome',type=str)
parser.add_argument('-q','--quality_cutoff',type=str)
parser.add_argument('-t','--gmap_threads',type=str, default='1')
args=parser.parse_args()

fastq=args.fastq
genome=args.genome
quality_cutoff=args.quality_cutoff
gmap_threads=args.gmap_threads

fastq_name=fastq.split('/')[-1]
path='/'.join(fastq.split('/')[:-1])+'/'
print(path)


os.system('python3 Mandalorion_1_Clean_Read_and_File_Names.py %s %s %s ' %(path, fastq_name,quality_cutoff))
os.system('python3 Mandalorion_3_Remove_ISPCR_Sequences.py %s ' %(path))
os.system('python3 Mandalorion_4_Align_Reads_With_Blat.py %s %s %s' %(path, genome, gmap_threads))
content_file=open(path+'/content_file','w')
content_file.write('%s\t%s\t%s\n' %(path+'/2D_trimmed_l_gmapoutput_filtered.psl',path+'/2D_trimmed_l_filtered.fasta',path+'/'))



