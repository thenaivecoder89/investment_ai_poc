"""
Download public demo corpus for the Renewable Energy Investment Review Copilot POC.

Run from the parent folder that contains Demo_Data_Folder:
    python Demo_Data_Folder/scripts/download_all_data.py

The script downloads sources that are practical to automate:
- IFC disclosure HTML pages + extracted text
- ADB PDFs / HTML pages
- NREL ATB CSV/workbook from OEDI endpoints
- World Bank WDI API CSVs
- SEC submissions, company facts, and latest 10-K HTMLs

For World Bank PPI and IRENASTAT, use MANUAL_DOWNLOAD_STEPS.md because those portals may require UI-based table filtering/export.
"""

from __future__ import annotations

import csv
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "00_Source_Register" / "download_run_log.csv"

HEADERS_DEFAULT = {
    "User-Agent": "Alchemy-POC-Research/1.0 (contact: anuragsarangi13@gmail.com)",
}
SEC_HEADERS = {
    "User-Agent": "Alchemy POC Research anuragsarangi13@gmail.com",
    "Accept-Encoding": "gzip, deflate",
}


def ensure_dirs() -> None:
    folders = [
        "00_Source_Register",
        "01_RAG_Public_Deal_Documents/IFC_Disclosure_Pages",
        "01_RAG_Public_Deal_Documents/ADB_Project_Documents",
        "01_RAG_Public_Deal_Documents/SEC_Annual_Reports_and_Filings",
        "02_Benchmark_and_Market_Data/World_Bank_PPI",
        "02_Benchmark_and_Market_Data/NREL_ATB",
        "02_Benchmark_and_Market_Data/IRENASTAT",
        "02_Benchmark_and_Market_Data/World_Bank_WDI",
        "02_Benchmark_and_Market_Data/SEC_XBRL",
        "03_ML_Input_Datasets/ARIMA_Time_Series",
        "03_ML_Input_Datasets/KMeans_Cost_and_Project_Clusters",
        "03_ML_Input_Datasets/Regression_Revenue_Reasonableness",
        "04_Seed_Libraries",
        "05_Processed_Output/parsed_text",
        "05_Processed_Output/extracted_financial_metrics",
        "05_Processed_Output/embeddings_ready_chunks",
        "05_Processed_Output/demo_reports",
    ]
    for folder in folders:
        (ROOT / folder).mkdir(parents=True, exist_ok=True)


def log(rows: list[list[str]]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    new = not LOG_PATH.exists()
    with LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["source_id", "target_filename", "status", "url", "message"])
        w.writerows(rows)


def fetch(url: str, headers: dict | None = None, timeout: int = 120) -> requests.Response:
    h = headers or HEADERS_DEFAULT
    r = requests.get(url, headers=h, timeout=timeout)
    r.raise_for_status()
    return r


def save_html_and_text(source_id: str, url: str, target_dir: Path, filename: str) -> None:
    rows = []
    try:
        r = fetch(url)
        html_path = target_dir / filename
        html_path.write_text(r.text, encoding="utf-8")
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()
        text = soup.get_text("\n", strip=True)
        txt_path = target_dir / filename.rsplit(".", 1)[0] + ".txt"
        txt_path.write_text(text, encoding="utf-8")
        rows.append([source_id, filename, "downloaded", url, "HTML and TXT saved"])
    except Exception as e:
        rows.append([source_id, filename, "failed", url, str(e)])
    log(rows)


def save_binary(source_id: str, url: str, target_dir: Path, filename: str) -> None:
    rows = []
    try:
        r = fetch(url)
        (target_dir / filename).write_bytes(r.content)
        rows.append([source_id, filename, "downloaded", url, f"{len(r.content)} bytes"])
    except Exception as e:
        rows.append([source_id, filename, "failed", url, str(e)])
    log(rows)


def download_ifc() -> None:
    target = ROOT / "01_RAG_Public_Deal_Documents" / "IFC_Disclosure_Pages"
    sources = [
        ("IFC_001", "https://disclosures.ifc.org/project-detail/SII/39151/frv-solar-india", "IFC_FRV_Solar_India_SII.html"),
        ("IFC_002", "https://disclosures.ifc.org/project-detail/SII/40099/azure-rg-project", "IFC_Azure_RG_Project_SII.html"),
        ("IFC_003", "https://disclosures.ifc.org/project-detail/SII/49802/pcr-renewables", "IFC_PCR_Renewables_SII.html"),
        ("IFC_004", "https://disclosures.ifc.org/project-detail/SII/48551/fp-energy-ef", "IFC_FP_Energy_EF_SII.html"),
        ("IFC_005", "https://disclosures.ifc.org/project-detail/SII/49109/candi-solar-ci", "IFC_Candi_Solar_CI_SII.html"),
        ("IFC_006", "https://disclosures.ifc.org/project-detail/SII/49272/elementum-debt", "IFC_Elementum_Debt_SII.html"),
        ("IFC_007", "https://disclosures.ifc.org/project-detail/ESRS/49907/indigrid-bess", "IFC_IndiGrid_BESS_ESRS.html"),
    ]
    for source_id, url, filename in sources:
        save_html_and_text(source_id, url, target, filename)


def download_adb() -> None:
    target = ROOT / "01_RAG_Public_Deal_Documents" / "ADB_Project_Documents"
    html_pages = [
        ("ADB_001", "https://www.adb.org/projects/58094-001/main", "ADB_Guzar_Solar_BESS_Project_Page.html"),
        ("ADB_004", "https://www.adb.org/projects/57173-001/main", "ADB_Gulf_Solar_BESS_Project_Page.html"),
        ("ADB_007", "https://www.adb.org/projects/59110-001/main", "ADB_Utility_Scale_BESS_Project_Page.html"),
        ("ADB_009", "https://www.adb.org/projects/54448-001/main", "ADB_Energy_Storage_Green_Hydrogen_Project_Page.html"),
        ("ADB_010", "https://www.adb.org/projects/51327-001/main", "ADB_Floating_Solar_Project_Page.html"),
    ]
    for source_id, url, filename in html_pages:
        save_html_and_text(source_id, url, target, filename)
    pdfs = [
        ("ADB_002", "https://www.adb.org/sites/default/files/project-documents/58094/58094-001-esia-en_0.pdf", "ADB_Guzar_Solar_BESS_ESIA_Part_2.pdf"),
        ("ADB_003", "https://www.adb.org/sites/default/files/project-documents/58094/58094-001-esia-en_2.pdf", "ADB_Guzar_Solar_BESS_ESIA_Part_4.pdf"),
        ("ADB_005", "https://www.adb.org/sites/default/files/project-documents/57173/57173-001-scar-en.pdf", "ADB_Gulf_Solar_BESS_SCAR.pdf"),
        ("ADB_006", "https://www.adb.org/sites/default/files/project-documents/57173/57173-001-iee-en_1.pdf", "ADB_Gulf_Solar_BESS_IEE.pdf"),
        ("ADB_008", "https://www.adb.org/node/1065411/printable/pdf", "ADB_Utility_Scale_BESS_Project_Printable.pdf"),
    ]
    for source_id, url, filename in pdfs:
        save_binary(source_id, url, target, filename)


def download_nrel_atb() -> None:
    target = ROOT / "02_Benchmark_and_Market_Data" / "NREL_ATB"
    sources = [
        ("NREL_001", "https://data.openei.org/files/6006/2024_v3_Model_Parameters.csv", "2024_v3_Model_Parameters.csv"),
        ("NREL_002", "https://data.openei.org/files/6006/2024_v3_Workbook.xlsx", "2024_v3_Workbook_Corrected_04_02_2025.xlsx"),
    ]
    for source_id, url, filename in sources:
        save_binary(source_id, url, target, filename)


def download_wdi() -> None:
    target = ROOT / "02_Benchmark_and_Market_Data" / "World_Bank_WDI"
    countries = "ARE;SAU;IND;EGY;JOR;ZAF;THA;KHM;UZB;AUS"
    indicators = {
        "WDI_001_GDP_Growth": "NY.GDP.MKTP.KD.ZG",
        "WDI_002_Inflation": "FP.CPI.TOTL.ZG",
        "WDI_003_Official_Exchange_Rate": "PA.NUS.FCRF",
        "WDI_004_GDP_Current_USD": "NY.GDP.MKTP.CD",
    }
    for name, indicator in indicators.items():
        url = f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}?format=json&per_page=20000&date=2010:2025"
        filename = f"{name}_2010_2025.csv"
        try:
            data = fetch(url).json()
            rows = data[1] if isinstance(data, list) and len(data) > 1 else []
            df = pd.json_normalize(rows)
            df.to_csv(target / filename, index=False)
            log([[name, filename, "downloaded", url, f"{len(df)} rows"]])
            # copy to ARIMA/regression folders
            df.to_csv(ROOT / "03_ML_Input_Datasets" / "ARIMA_Time_Series" / filename, index=False)
            df.to_csv(ROOT / "03_ML_Input_Datasets" / "Regression_Revenue_Reasonableness" / filename, index=False)
        except Exception as e:
            log([[name, filename, "failed", url, str(e)]])


def latest_10k_url_from_submissions(sub: dict, cik: str) -> tuple[str | None, str | None]:
    recent = pd.DataFrame(sub.get("filings", {}).get("recent", {}))
    if recent.empty or "form" not in recent.columns:
        return None, None
    tenk = recent[recent["form"].eq("10-K")].head(1)
    if tenk.empty:
        return None, None
    row = tenk.iloc[0]
    accession = str(row["accessionNumber"])
    primary_doc = str(row["primaryDocument"])
    accession_clean = accession.replace("-", "")
    cik_no_zeros = str(int(cik))
    filing_url = f"https://www.sec.gov/Archives/edgar/data/{cik_no_zeros}/{accession_clean}/{primary_doc}"
    return filing_url, primary_doc


def download_sec() -> None:
    filings_target = ROOT / "01_RAG_Public_Deal_Documents" / "SEC_Annual_Reports_and_Filings"
    facts_target = ROOT / "02_Benchmark_and_Market_Data" / "SEC_XBRL"
    companies = {
        "NextEra_Energy": "0000753308",
        "AES_Corporation": "0000874761",
        "First_Solar": "0001274494",
        "Ormat_Technologies": "0001296445",
        "Enphase_Energy": "0001463101",
    }
    for company, cik in companies.items():
        sub_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        facts_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
        try:
            sub = fetch(sub_url, headers=SEC_HEADERS).json()
            (filings_target / f"{company}_submissions.json").write_text(json.dumps(sub, indent=2), encoding="utf-8")
            log([[company, f"{company}_submissions.json", "downloaded", sub_url, "SEC submissions JSON saved"]])
            filing_url, primary_doc = latest_10k_url_from_submissions(sub, cik)
            if filing_url:
                html = fetch(filing_url, headers=SEC_HEADERS).text
                (filings_target / f"{company}_Latest_10K.html").write_text(html, encoding="utf-8")
                soup = BeautifulSoup(html, "html.parser")
                for tag in soup(["script", "style", "noscript"]):
                    tag.extract()
                (filings_target / f"{company}_Latest_10K.txt").write_text(soup.get_text("\n", strip=True), encoding="utf-8")
                log([[company, f"{company}_Latest_10K.html", "downloaded", filing_url, "Latest 10-K HTML/TXT saved"]])
            else:
                log([[company, "Latest_10K", "not_found", sub_url, "No recent 10-K found in submissions"]])
        except Exception as e:
            log([[company, f"{company}_submissions.json", "failed", sub_url, str(e)]])

        time.sleep(0.2)  # SEC fair access: remain well below 10 req/sec.

        try:
            facts = fetch(facts_url, headers=SEC_HEADERS).json()
            (facts_target / f"{company}_companyfacts.json").write_text(json.dumps(facts, indent=2), encoding="utf-8")
            log([[company, f"{company}_companyfacts.json", "downloaded", facts_url, "SEC company facts JSON saved"]])
        except Exception as e:
            log([[company, f"{company}_companyfacts.json", "failed", facts_url, str(e)]])
        time.sleep(0.2)


def main() -> None:
    ensure_dirs()
    print("Starting public data downloads. Logs will be written to", LOG_PATH)
    download_ifc()
    download_adb()
    download_nrel_atb()
    download_wdi()
    download_sec()
    print("Completed automated download attempt. Check", LOG_PATH)
    print("For World Bank PPI and IRENASTAT, follow scripts/MANUAL_DOWNLOAD_STEPS.md")


if __name__ == "__main__":
    main()
