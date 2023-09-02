import gzip
import shutil

#this script simply zips up an inputted jsonl file
jsonl_file = input("\nEnter path for collected jsonl dataset: ") or 'scraped_credits.jsonl'
gzipname = input("\nEnter desired path for the zipped dataset (end it with .gz): ") or 'compressed_credits.gz'
with open(jsonl_file, 'rb') as f_in:
    with gzip.open(gzipname, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)