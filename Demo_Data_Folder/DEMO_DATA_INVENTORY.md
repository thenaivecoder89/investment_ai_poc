# Demo Data Inventory

## Included directly in this ZIP

| Item | Location | Status |
|---|---|---|
| Folder structure | `Demo_Data_Folder/` | Included |
| Source register | `00_Source_Register/source_register.csv` | Included |
| Source manifest | `00_Source_Register/source_manifest.json` | Included |
| Download status note | `00_Source_Register/download_status.csv` | Included |
| Completeness checklist seed | `04_Seed_Libraries/completeness_checklist.csv` | Included |
| IC question library seed | `04_Seed_Libraries/ic_question_library.csv` | Included |
| Renewable risk taxonomy seed | `04_Seed_Libraries/renewable_energy_risk_taxonomy.csv` | Included |
| Downloader script | `scripts/download_all_data.py` | Included |
| Manual download steps | `scripts/MANUAL_DOWNLOAD_STEPS.md` | Included |
| Requirements file | `scripts/requirements.txt` | Included |

## Public data to be downloaded locally using the included script

| Source | Download method | Target folder |
|---|---|---|
| IFC disclosure pages | Automated script | `01_RAG_Public_Deal_Documents/IFC_Disclosure_Pages/` |
| ADB project pages/PDFs | Automated script | `01_RAG_Public_Deal_Documents/ADB_Project_Documents/` |
| NREL ATB | Automated script | `02_Benchmark_and_Market_Data/NREL_ATB/` |
| World Bank WDI | Automated script | `02_Benchmark_and_Market_Data/World_Bank_WDI/` |
| SEC EDGAR submissions / 10-K / XBRL | Automated script | `01_RAG_Public_Deal_Documents/SEC_Annual_Reports_and_Filings/`, `02_Benchmark_and_Market_Data/SEC_XBRL/` |
| World Bank PPI | Manual UI export | `02_Benchmark_and_Market_Data/World_Bank_PPI/` |
| IRENASTAT | Manual UI export / PxWeb API | `02_Benchmark_and_Market_Data/IRENASTAT/` |

## Minimum viable demo pack

For a fast 1-week POC, the minimum useful corpus is:

1. 5-7 IFC disclosure pages
2. 3-5 ADB PDFs/project pages
3. NREL ATB model parameters
4. WDI macro CSVs
5. Seed checklist, IC question library, and risk taxonomy

This is sufficient for:
- RAG-based completeness review
- source-cited Q&A
- financial metric extraction
- likely IC question generation
- risk prompts and mitigants
- benchmark reasonableness checks
