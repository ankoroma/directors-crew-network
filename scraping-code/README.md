Here is the code and finished dataset for the web scraping task of our Network Science group project. To initialize the scraping, simply run dataset_generator.py. This script uses a collection of functions, some created by myself (Jeff Bailey) and some provided by our professor, to initialize or add to a .jsonl dataset of directors and their credited crew. There are three modifiable parameters to this script, which can be inputted when prompted after running it. These are: 
1. your director data, which currently comes from the provided 100_film_directors.csv
2. your dataset file name, which I have not uploaded to the repo because it was quite large
3. a list of desired roles to record credits from, which after discussion I decided not to use. Putting an empty list [''] will scrape from all crew roles. 

The script loads the csv into a pandas df and then, for each director listed in the dataframe, checks the jsonl if the director is already recorded and if not it runs scraping functions to record every crew member credited with a role in the desired list for each of the director's feature film credits. This will output a jsonl file, with a json dictionary for each director's credits.

The script "credit_compressor.py" was used to compress the large jsonl dataset into a gzip file, which took less than a fifth of the space of the original jsonl. When it is run, it prompts the user for input for the jsonl path and the desired gzip path.

For both of these scripts, simply passing nothing to the input prompts will run the scripts with default values which I used: director data from 100_film_directors.csv, dataset saved to scraped_credits.jsonl, [''] no filtered roles, and compressed_credits.gz
