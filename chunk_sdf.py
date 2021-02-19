from rdkit import Chem
import json
import sys
import os

def chunk_sdf(filename, chunksize):
    chunksize = int(chunksize)
    suppl = Chem.SDMolSupplier(filename)
    mols = [x for x in suppl]
    plist = []
    for m in mols:
        try:
            plist.append(Chem.rdchem.Mol.GetPropsAsDict(m))
        except:
            plist.append({})

    fprefix = filename.replace('.sdf', '')
    for i in range(0, len(plist), chunksize):
        to_query = plist[i:i+chunksize]
        with open(f'{fprefix}_{i}.json', 'w+') as f:
            json.dump(to_query, f)

if __name__=='__main__':
    chunk_sdf(*sys.argv[1:])
