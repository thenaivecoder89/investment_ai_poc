# Demo Data Folder - Renewable Energy Investment Review Copilot POC

This package is structured for the 1-week POC demo discussed in the SoW review workflow.

## Important note
The ChatGPT execution sandbox used to prepare this ZIP could not resolve external internet hostnames, so the live public files could not be downloaded directly inside the sandbox. The package therefore contains:

1. The complete folder structure.
2. Seed libraries for completeness checks, IC questions, and renewable-energy risk prompts.
3. A source register with exact source URLs, target filenames, and intended POC use.
4. A ready-to-run downloader script (`scripts/download_all_data.py`) that you can run locally to download the public data into the same folder structure.
5. Manual download instructions for sources where the public portals require UI interaction.

## How to use this package locally

### Step 1 - Unzip
Unzip this folder to your local machine.

### Step 2 - Install Python dependencies
From the unzipped `Demo_Data_Folder` parent directory, run:

```bash
pip install -r Demo_Data_Folder/scripts/requirements.txt
```

### Step 3 - Run the downloader
Run:

```bash
python Demo_Data_Folder/scripts/download_all_data.py
```

The script will attempt to download:
- IFC disclosure pages
- ADB PDFs
- NREL ATB files
- World Bank WDI API data
- SEC submissions, company facts, and latest 10-K filings

For World Bank PPI and IRENASTAT, follow the instructions in:
- `scripts/MANUAL_DOWNLOAD_STEPS.md`

These two sources may need browser selection/export depending on the exact table and filters required.

## POC module mapping

| POC module | Input folders |
|---|---|
| RAG completeness and gap analysis | `01_RAG_Public_Deal_Documents/IFC_Disclosure_Pages`, `01_RAG_Public_Deal_Documents/ADB_Project_Documents`, `01_RAG_Public_Deal_Documents/SEC_Annual_Reports_and_Filings`, `04_Seed_Libraries` |
| Financial extraction | IFC, ADB, SEC filings, NREL ATB |
| Historical / likely IC question matching | `04_Seed_Libraries/ic_question_library.csv` + RAG corpus |
| ARIMA market alignment | `02_Benchmark_and_Market_Data/IRENASTAT`, `02_Benchmark_and_Market_Data/World_Bank_WDI` |
| K-means clustering | `02_Benchmark_and_Market_Data/World_Bank_PPI`, `02_Benchmark_and_Market_Data/NREL_ATB` |
| Regression reasonableness check | NREL ATB + IRENASTAT + WDI + PPI |

## Recommended first demo pack
For fastest development, start with:
1. IFC disclosure pages
2. ADB PDFs
3. NREL ATB model parameters
4. WDI macro data
5. Seed libraries

Then add PPI, IRENASTAT, and SEC filings after the base RAG pipeline is stable.
