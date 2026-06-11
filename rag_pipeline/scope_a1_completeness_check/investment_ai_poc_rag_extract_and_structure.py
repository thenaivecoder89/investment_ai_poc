from bs4 import BeautifulSoup
from collections import Counter
from dotenv import load_dotenv
from pathlib import Path
import os
import math
import re
import statistics
import pymupdf
import csv
import json
import pandas as pd

# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------

# If a page contains fewer native characters than this,
# attempt OCR for that page.
OCR_THRESHOLD = 80

# Top and bottom 8% of each page are considered possible
# header/footer regions.
MARGIN_RATIO = 0.08

# Initializing environment variables and loading data
load_dotenv()
doc_manifest = os.getenv("DOC_MANIFEST")
ph3_output = os.getenv("PH3_OUTPUT")
df_manifest = pd.read_csv(doc_manifest)

# ---------------------------------------------------------------------
# TEXT CLEANING
# ---------------------------------------------------------------------
print(f"Manifest data: \n{df_manifest.head(5)}")
print(f"Manifest Data Columns: \n{df_manifest.columns}")
full_file_path = pd.concat(df_manifest["full_path"], df_manifest["file_name"])
print(f"Full File Paths: \n{full_file_path}")