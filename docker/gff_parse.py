#!/usr/bin/env python3
import sys, os
import numpy as np

cwd = os.getcwd()
cols_indx = []
helpScreen = """Usage: python3 gff_parse.py [OPTION] tsv_file gff_file columns_txt_file output_file_name

columns_txt_file should be a text file with column names seperated by semicolons (;)

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

def gff_parsing(tsv,gff,cols,out):
    global cols_indx
    if verbose: print("Reading files: {0}, {1}, {2}".format(tsv,gff,cols))
    tsv = open(os.path.join(cwd,tsv),"r").read().split("\n")[:-1]
    gff = open(os.path.join(cwd,gff),"r").read().split("\n")[:-1]
    cols = np.loadtxt(os.path.join(cwd,cols), dtype=str, delimiter=";")
    filter_cols = cols != ''
    cols = cols[filter_cols]
    if verbose: print("Columns selected: "+", ".join(cols))
    tsv = list(map(split_sub,tsv))
    cols_indx = np.array([ tsv[0].index(i) for i in cols ])
    cols_indx = np.insert(cols_indx,0,0)
    tsv[0] = np.array(tsv[0])[cols_indx]
    tsv = list(map(filtering_cols,tsv[1:]))
    tsv_dict = {}
    for i in tsv:
        formatted_txt = ""
        for n,c in enumerate(i[1:]):
            formatted_txt += ";{0}={1}".format(cols[n].lower().replace(" ","_"),c)
        tsv_dict[i[0]] = formatted_txt
    if verbose: print("Preparing new gff data")
    for n,g in enumerate(gff):
        if verbose:
            if n%25==0:
                print(f"\b\b\b\b{int(100*(n/len(gff)))}%",end="",flush=True)
        if g[:2] == "##" or "mRNA" not in g:
            continue
        gid = get_gff_id(g)
        gff[n]+=tsv_dict[gid]
    if verbose: print("\b\b\b\bDone")
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
        if verbose: print("User chose to not overwrite file, program terminated")


if __name__ == '__main__':
    if len(sys.argv) < 5:
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
        if len(sys.argv) < 5:
            print(helpScreen)
            sys.exit(-1)
        else:
            gff_parsing(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])


