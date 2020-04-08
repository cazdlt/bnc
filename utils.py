import requests
from tqdm import tqdm

def download_progressbar(url):
    
    r = requests.get(url, stream=True)
    file_=bytes()

    original_name=r.headers["Content-Disposition"].partition("''")[-1]
    total_size = int(r.headers.get('content-length', 0))
    block_size = int(total_size/50) #2**16

    print(f"Descargando {original_name}...")
    t=tqdm(total=total_size, unit='iB', unit_scale=True)
    for data in r.iter_content(block_size):
        t.update(len(data))
        file_+=data
    t.close()

    if total_size != 0 and t.n != total_size:
        raise "Error de descarga"

    return (r,file_)