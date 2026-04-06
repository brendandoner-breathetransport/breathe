# Economy
## make_economy_income
### Sources
* **Income Share**: [World Inequality Database](https://wid.world/country/usa/). Click on "By Country", select a country, select "Bottom 50% share" and "Top 1% share", then download the csv format.
* **Income U.S. Total**: U.S. Bureau of Economic Analysis, Personal income [A065RC1A027NBEA], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/A065RC1A027NBEA, March 1, 2025.
* **Population U.S. Total**: World Bank, Population, Total for United States [POPTOTUSA647NWDB], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/POPTOTUSA647NWDB, March 1, 2025.
* **Population Workers Ratio**: U.S. Bureau of Labor Statistics, Employment-Population Ratio [EMRATIO], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/EMRATIO, March 1, 2025.
* **Population Part-Time vs Full-Time Workers**: Brundage, Vernon - U.S. Bureau of Labor Statistics. USUAL WEEKLY EARNINGS of WAGE and SALARY WORKERS THIRD QUARTER 2016. 2024. www.bls.gov/news.release/pdf/wkyeng.pdf
* **Tax Rates Personal**: [U.S. Internal Revenue Service](https://www.irs.gov/statistics/soi-tax-stats-historical-table-23)

### Steps
1. Download data from the sources
2. Use the income share data and the total income data with the population data to calculate the average income for each slice of the income pie.

### Internal Notes
* Pipeline located in breathe/notebooks/pipeline_economy.ipynb

## make_economy_house_purchase
### Sources
* **House Purchase Cost**: [Zillow](https://www.zillow.com/research/data/). Select "ZHVI All Homes (SFR, Condo/Co-op) Time Series, Smoothed, Seasonally Adjusted ($)" for Geography of "Metro & U.S.".

## make_american_dream_kids
### Sources
* **The Long Run Evolution of Absolute Intergenerational Mobility**: [The Long Run Evolution of Absolute Intergenerational Mobility](https://www.openicpsr.org/openicpsr/project/141761/version/V1/view)

## make_mobility_international
### Sources
* **The Long Run Evolution of Absolute Intergenerational Mobility**: [The Long Run Evolution of Absolute Intergenerational Mobility](https://www.openicpsr.org/openicpsr/project/141761/version/V1/view)

## Additional
### Sources
* **Fading American Dream: Baseline Estimates of Absolute Mobility by Parent Income Percentile and Child Birth Cohort**: [Opportunity Insights based at Harvard University](https://opportunityinsights.org/data/).

## make_economy_f150
### Internal Notes:
- Data compiled by https://claude.ai/
- Prices are for the base model/standard cab configuration at time of introduction
- The F-150 designation specifically began in 1975 (previously F-100)
- Pricing may vary by region and throughout the model year
- Prices do not account for inflation - $1,332 in 1950 would be equivalent to approximately $15,900 in 2025 dollars
- Generation changes typically represent significant redesigns of the vehicle
- Data compiled from multiple historical sources and may have some variation from dealer-specific pricing
### Sources
  * **NADA Guides** - Contains historical vehicle pricing information, though their free online access may be limited for very old models
    * https://www.nadaguides.com/
  * **Kelley Blue Book (KBB)** - May have historical MSRP data in their archives
    * https://www.kbb.com/
  * **Hagerty** - Specializes in classic and collector cars with valuation tools
    * https://www.hagerty.com/
  * **Old Car Brochures** - Contains scanned original sales literature with period pricing
    * http://www.oldcarbrochures.com/
  * **The Henry Ford Museum** - Has extensive Ford archives, including pricing information
    * https://www.thehenryford.org/
  * **Ford Motor Company Archives** - While not all publicly accessible, they maintain historical records
  * **Classic car forums** - Communities like Ford-Trucks.com often have members who share original documentation

# Healthcare
## make_healthcare
### Sources
* **Healthcare Cost Per Capita**: [World Bank](https://data.worldbank.org/indicator/SH.XPD.CHEX.PC.CD).
* **Life Expectancy**: [World Health Organization](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/life-expectancy-at-birth-(years)).

# Environment
## make_electricity_cost
### Sources
* **Cost of Energy**: [Lazard’s Levelized Cost of Energy Analysis](https://www.lazard.com/media/xemfey0k/lazards-lcoeplus-june-2024-_vf.pdf).
