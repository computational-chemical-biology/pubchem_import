# https://ceb.nlm.nih.gov/~simpsonmatt/download.py
# https://gist.github.com/ReneNyffenegger/20d2ed058d86bdfaeae6

import ftplib
import zlib
import sys
import os

def get_gz(ftp, ftp_filename, local_filename):
    decomp = zlib.decompressobj(16+zlib.MAX_WBITS)
    unzip = open (local_filename, 'wb')
    def next_packet(data):
        unzip.write(decomp.decompress(data))
    ftp.retrbinary('RETR ' + ftp_filename, next_packet)
    decompressed = decomp.flush()
    unzip.write(decompressed)
    unzip.close()

if __name__=='__main__':
    num = int(sys.argv[1])
    directory = 'download'
    file_path = 'pubchem/Compound/CURRENT-Full/SDF'

    if not os.path.exists(directory):
        os.makedirs(directory)

    pmc = ftplib.FTP('ftp.ncbi.nlm.nih.gov')
    pmc.login()
    pmc.cwd(file_path)
    fls = pmc.nlst()
    fls = [x for x in fls if 'md5'not in x]
    d = os.listdir('download')
    for f in fls[:num]:
        if f not in d:
            get_gz(pmc, f,
                   os.path.join('download',
                                f.replace('.gz', '')))
