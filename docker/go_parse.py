#!/usr/bin/env python3
import pandas as pd
import multiprocessing
import sys
helpScreen = """Usage: python3 go_parse.py [OPTIONS] input_tsv output_tsv

Reads a tsv file and outputs a tsv file with names and all corresponding GO data separated by semicolons

Options
    -h      Show this help
    -q      Suppress non-error messages
"""
verbose = True

    
def process_chunk(chunk,lock,prog,verbose=True):
    go_cols = [n for n,col in enumerate(chunk.columns) if 'GO' in col]
    out_chunk = []
    for i,(n,r) in enumerate(chunk.iterrows()):
        GO_str = ",".join([ r[x] for x in go_cols if r[x]!="NA"])
        GO_str = GO_str.replace(",,",",")[:-1]
        exists = []
        for x in GO_str.split(","):
            if x not in exists:
                exists.append(x)
        GO_str = ";".join(exists)
        if GO_str == "":
            continue
        out_chunk.append([r[0],GO_str])
        #out_chunk.loc[i] = [r[0],GO_str]
    out_chunk = pd.DataFrame(out_chunk)
    with lock:
        prog.value+=1
        if verbose: print(f"Finished chunk {prog.value}")
    return out_chunk

def join(tsv_in,tsv_out):
    if verbose: print("Reading input tsv file...",end="",flush=True)
    chunks = pd.read_csv(tsv_in,sep="\t",dtype=str,na_filter=False,chunksize=10000)
    if verbose: print("Done\nParsing GO data...")

    with multiprocessing.Manager() as mgr:
        prog = mgr.Value("i",0)
        lock = mgr.Lock()
        multiprocessing.set_start_method('spawn', force=True)
        pool = multiprocessing.Pool(multiprocessing.cpu_count()-1)
        result = pool.starmap(process_chunk,[(chunk,lock,prog,verbose) for chunk in chunks])
        pool.close()
        pool.join()
        df = pd.concat(result)
        print("Done")

    if verbose: print("Writing to file...")
    df.to_csv(tsv_out,sep="\t",index=False,header=False,chunksize=10000)
        

if __name__ == '__main__':
    if len(sys.argv) < 3:
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
                if not flag:
                    print("Flag "+a+" unrecognized")
                    sys.exit(-1)
                toRemove.append(a)
        for i in toRemove:
            sys.argv.remove(i)
        if len(sys.argv) < 3:
            print(helpScreen)
            sys.exit(-1)
        else:
            join(sys.argv[1],sys.argv[2])
