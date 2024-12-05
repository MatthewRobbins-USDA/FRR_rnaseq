#!/usr/bin/env python3
import sys, os
import numpy as np

cwd = os.getcwd()
cols_indx = []
helpScreen = """Usage: python3 csv_add_annotations.py [OPTION] tsv_file/csv_file csv_annotation_files


Options
    -h      Show this help
    -q      Suppress non-error messages
    -f      Force overwrite of files (doesn't prompt)
"""
verbose = True
overwrite = False

def split_sub(a):
    arr = a.split("\t")[:-1]
    return arr

def filtering_cols(a):
    try:
        return np.array(a)[cols_indx]
    except:
        print(a)

def get_gff_id(s):
    return s.split(";")[0].split("ID=")[1]

def gff_parsing(csvFile,annotations):
    global cols_indx
    if verbose: print("Reading files: {0}".format(csvFile))
    #csv = open(os.path.join(cwd,csv),"r").read().split("\n")[:-1]
    csv = open(os.path.join(cwd,csvFile),"r+").read().split("\n")[:-1]
    #gff = open(os.path.join(cwd,gff),"r").read().split("\n")[:-1]
    #csv[0] = np.array(csv[0])[cols_indx]
    #csv = list(map(filtering_cols,csv[1:]))
    if csvFile.split('.')[-1] == "csv":
        csv = [ i.split(',') for i in csv ]
    elif csvFile.split('.')[-1] == "tsv":
        csv = [ i.split('\t') for i in csv ]
    else:
        print("Unknown file type, could not determine from file extension. File should be a .csv or a .tsv")
        sys.exit(-1)

    annotations = open(os.path.join(cwd,annotations)).read().split("\n")[:-1]
    annotations = [ a for a in annotations if a[0]!="#" ]
    #print(annotations[0].split('\t'))
    annot_dict = {}
    for i in annotations:
        annot_parse = i.split('\t')
        if annot_parse[2] in annot_dict:
            annot_dict[annot_parse[2]] += ";{0}".format(annot_parse[4])
        else:
            annot_dict[annot_parse[2]] = annot_parse[4]

    for i in csv:
        if i[1][:-2] in annot_dict:
            i.append("\""+annot_dict[i[1][:-2]]+"\"")
        else:
            i.append("")

    
    outFile = open(os.path.join(cwd,"mapman_"+"".join(csvFile.split('.')[:-1])+".csv"),"w")
    for l in csv:
        outFile.write(",".join(l)+"\n")

    """
    csv_dict = {}
    for i in csv:
        formatted_txt = ""
        for n,c in enumerate(i[1:]):
            formatted_txt += ";{0} {1}".format(cols[n],c)
        csv_dict[i[0]] = formatted_txt
    
    if verbose: print("Preparing new gff data")
    for n,g in enumerate(gff):
        if g[:2] == "##" or "mRNA" not in g:
            continue
        gid = get_gff_id(g)
        gff[n]+=csv_dict[gid]

    if os.path.exists(os.path.join(cwd,out)) and not overwrite:
        cont = input("File: "+out+" already exists, do you wan't to overwrite? (y/n)")
    else:
        cont = "y"
    if cont.lower() == "y":
        if verbose: print("Writing to file: "+out)
        outFile = open(os.path.join(cwd,out),"w")
        for l in gff:
            outFile.write(l+"\n")
        outFile.close()
    else:
        if verbose: print("User chose to not overwrite file, program terminated")"""


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(helpScreen)
        sys.exit(-1)
    else:
        toRemove = []
        for n,a in enumerate(sys.argv):
            if a[0] == "-":
                flag = False
                if "h" in a:
                    print(helpScreen)
                    flag = True
                    sys.exit(-1)
                else:
                    if "q" in a:
                        verbose = False
                        flag = True
                    if "f" in a:
                        overwrite = True
                        flag = True
                if not flag:
                    print("Flag "+a+" unrecognized")
                    sys.exit(-1)
                toRemove.append(a)
        for i in toRemove:
            sys.argv.remove(i)
        if len(sys.argv) < 2:
            print(helpScreen)
            sys.exit(-1)
        else:
            gff_parsing(sys.argv[1],sys.argv[2])


