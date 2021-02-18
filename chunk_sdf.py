from rdkit import Chem
import json

suppl = Chem.SDMolSupplier('Compound_000000001_000500000.sdf')

mols = [x for x in suppl]
plist = []
for m in mols:
    try:
        plist.append(Chem.rdchem.Mol.GetPropsAsDict(m))
    except:
        plist.append({})

chunksize = 10000
fprefix = 'Compound_000000001_000500000'
for i in range(0, len(plist), chunksize):
    to_query = plist[i:i+chunksize]
    with open(f'{fprefix}_{i}.json', 'w+') as f:
        json.dump(to_query, f)
