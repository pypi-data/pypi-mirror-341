import marshal
from amazing_filters.filters import FILTERS

SIGNATURE = b"FILTER"

def embed_filter(image_path, output_path, filter_name):
    if filter_name not in FILTERS:
        raise ValueError(f"Unknown filter: {filter_name}")
    code_blob = marshal.dumps(FILTERS[filter_name].__code__)
    payload = SIGNATURE + code_blob
    with open(image_path, "rb") as fin:
        img_data = fin.read()
    with open(output_path, "wb") as fout:
        fout.write(img_data)
        fout.write(payload)
