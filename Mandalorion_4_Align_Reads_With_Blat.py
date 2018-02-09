import os
import sys
import numpy as np

gmap_threads=sys.argv[3]
genome=sys.argv[2]
path=sys.argv[1]




def extract_fastq_data(path,infile):
    fastq_file=path+'/2D_trimmed_l.fastq'
    data={}
    length1=0
    for line in open(fastq_file):
        length1+=1
    x=4

    infile=open(fastq_file,'r')
    while x<=length1:
        x+=4
        a=infile.readline()
        b=infile.readline()
        c=infile.readline()
        d=infile.readline()

        name=a[1:].strip()
        data[name]=[a,b,c,d]
    return data

def write_filtered_fastq(pass_data,path,outfile):
    out_fastq=open(path+'/2D_trimmed_l_filtered.fastq','w')
    out_fasta=open(path+'/2D_trimmed_l_filtered.fasta','w')

    already={}
    for line in open(outfile):
        a=line.strip().split('\t')
        name=a[9]
        try:  
            bla=already[name]
        except:
            already[name]=1
            try:
                fast=pass_data[name]
                out_fastq.write(fast[0]+fast[1]+fast[2]+fast[3])
                out_fasta.write('>'+fast[0][1:]+fast[1])
            except:
                pass

def filter_reads(path,infile,outfile):

    out=open(outfile,'w')
    data_dict={}
    read_list=[]
    for line in open(infile):
        a=line.strip().split('\t')
        aligned_bases=sum(np.array(a[18].split(',')[:-1],dtype=int))/int(a[10])
        read_list.append(line)
        try:
            match=sorted(data_dict[a[9]],key=lambda x: int(x[0]))
            if int(a[0])>match[-1][0]*1.02:
                data_dict[a[9]]=[(int(a[0]),int(a[7]),aligned_bases,int(a[1]))]
            elif int(a[0])>match[-1][0]*0.98:
                data_dict[a[9]].append((int(a[0]),int(a[7]),aligned_bases,int(a[1])))
        except:
            data_dict[a[9]]=[]
            data_dict[a[9]].append((int(a[0]),int(a[7]),aligned_bases,int(a[1])))

    matched={}

    
    for line in read_list:
        a=line.strip().split('\t')
        aligned_bases=sum(np.array(a[18].split(',')[:-1],dtype=int))
        all_bases=int(a[10])
        ratio=aligned_bases/all_bases
        mismatches=int(a[1])

        gaps=[]
        scores=[]
        ratios=[]
        mis=[]
        bla=data_dict[a[9]]
        for entry in bla:
           gaps.append(entry[1]) 
           scores.append(entry[0])
           ratios.append(entry[2])
           mis.append(entry[3])
        if int(a[7]) == max(gaps): 
               if int(a[0]) >= min(scores):
                   if ratio>0.6:
                       try:
                           blas=matched[a[9]]
                       except:
                           matched[a[9]]=1 
                           out.write(line)

    out.close()




infile=path+'/2D_trimmed_l_gmapoutput.psl'
outfile=path+'/2D_trimmed_l_gmapoutput_filtered.psl'
os.system('blat %s %s %s -stepSize=5 -repMatch=2253 -minScore=100 -minIdentity=50 -maxIntron=2000000 -noHead' %(genome,path+'/2D_trimmed_l.fasta',infile))
filter_reads(path,infile,outfile)
pass_data=extract_fastq_data(path,infile)
print(len(pass_data))
write_filtered_fastq(pass_data,path,outfile)






