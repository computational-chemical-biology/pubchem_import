# https://ceb.nlm.nih.gov/~simpsonmatt/download.py

import ftplib
import io
import tarfile
import os

directory = 'download'

if not os.path.exists(directory):
    os.makedirs(directory)


pmc = ftplib.FTP('ftp.ncbi.nlm.nih.gov')
pmc.login()
pmc.dir('pubchem/Compound/CURRENT-Full/SDF')

response = io.BytesIO()
pmc.cwd('pubchem/Compound/CURRENT-Full/SDF')
pmc.retrbinary("RETR " + 'Compound_000000001_000500000.sdf.gz', response.write, 32)
tar = tarfile.open(fileobj=io.BytesIO(response.getvalue()),mode="r:gz")
tar.extractall(path=directory, members=files_to_extract(tar, pmcid))

response.close()
tar.close()
