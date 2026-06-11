# Manual download steps for non-trivial public portals

These two sources are best downloaded manually for the first POC run because the browser UI lets you confirm the exact filters and exported tables.

## 1. World Bank PPI

Target folder:
`Demo_Data_Folder/02_Benchmark_and_Market_Data/World_Bank_PPI/`

Open:
`https://ppi.worldbank.org/en/ppidata`

Steps:
1. Click / open the custom query or data download option.
2. Select Sector = Energy.
3. Select Subsector = Electricity / electricity generation where available.
4. Select years = 2010 to latest available.
5. Select all countries / all regions.
6. Download the result as Excel or CSV.
7. Save as: `WorldBank_PPI_Energy_Renewables_2010_Latest.xlsx`.
8. If a STATA full database is available, download and save as: `WorldBank_PPI_Full_Database.dta`.

Key columns to keep for K-means / comparable project analytics:
- project_name
- country
- region
- sector
- subsector
- technology
- financial_closure_year
- investment_commitment_usd
- capacity_mw
- private_participation_type
- sponsor
- debt_provider
- development_bank_support
- government_support
- status

## 2. IRENASTAT

Target folder:
`Demo_Data_Folder/02_Benchmark_and_Market_Data/IRENASTAT/`

Open:
`https://pxweb.irena.org/pxweb/en/IRENASTAT/`

Steps for generation data:
1. Click `Power Capacity and Generation`.
2. Select the electricity generation statistics table.
3. Select countries:
   - India
   - United Arab Emirates
   - Saudi Arabia
   - Egypt
   - Jordan
   - South Africa
   - Thailand
   - Cambodia
   - Uzbekistan
   - Australia
4. Select technologies:
   - Solar energy
   - Wind energy
   - Total renewable energy
5. Select data type = Electricity generation.
6. Select grid connection = Total or On-grid.
7. Select years = 2010 to latest available.
8. Show table.
9. Download as CSV.
10. Save as: `IRENASTAT_Electricity_Generation_By_Country_Technology_2010_Latest.csv`.

Repeat for installed capacity and save as:
`IRENASTAT_Installed_Capacity_By_Country_Technology_2010_Latest.csv`.

Use for:
- ARIMA time-series market trend analysis
- renewable penetration/growth overlays
- regression reasonableness checks
