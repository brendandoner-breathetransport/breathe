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

## make_state_income
### Sources
* **AGI Percentile Data by State (2013–2022)**: [IRS Statistics of Income — Adjusted Gross Income (AGI) Percentile Data by State](https://www.irs.gov/statistics/soi-tax-stats-agi-percentile-data-by-state). Tax years 2013–2022. Files named `{YY}instateshares.csv`. Provides counts and total AGI for the top 1% and top 50% of filers by state, used to derive average income for Bottom 50%, Upper 51–99%, and Top 1% brackets directly by subtraction.
* **Historic Table 2 by State (1997–2012)**: [IRS Statistics of Income — Historic Table 2](https://www.irs.gov/statistics/soi-tax-stats-historic-table-2). Tax years 1997–2012. Files named `{YY}in54cm.xls[x]` (XLS) and `12in54cmcsv.csv` (CSV). Provides counts and total AGI by fixed AGI size bracket (not percentile), requiring bracket interpolation to estimate Bottom 50%, Upper 51–99%, and Top 1% averages. All dollar amounts are in thousands of dollars as stated in each file's header.
* **U.S. National Historical (WID)**: [World Inequality Database](https://wid.world/country/usa/). Long-run U.S. national income series covering 1820–2023, used as a third comparison line extending before and after the IRS state data window.

### Steps
1. Go to the [IRS Statistics of Income — AGI Percentile Data by State](https://www.irs.gov/statistics/soi-tax-stats-agi-percentile-data-by-state) page and download the CSV file for each tax year 2013–2022.
2. Go to the [IRS SOI Historic Table 2](https://www.irs.gov/statistics/soi-tax-stats-historic-table-2) page and download the XLS/CSV file for each tax year 1997–2012. File names follow the pattern `{YY}in54cm.xls`.
3. **For 2013–2022 (percentile format):** The IRS reports cumulative top-percentile slices (top 50% and top 1%). Derive the three brackets by subtraction: Bottom 50% = all filers minus top 50%; Upper 51–99% = top 50% minus top 1%; Top 1% = top 1% directly. Caution: 2014, 2016, and 2017 files publish AGI in full dollars (not thousands) — detect this by checking if the U.S. national total AGI exceeds $1 trillion, then divide by 1,000 to normalize.
4. **For 1997–2012 (bracket format):** The data is organized by fixed AGI size brackets (e.g., Under $50k, $50k–$75k, …, $1M+). Use uniform-within-bracket interpolation to find the 50th and 99th percentile boundaries: walk brackets from lowest to highest, accumulating return counts until you reach 50% of total returns (for the Bottom 50% cutpoint); repeat from the top to find the Top 1% cutpoint. The Upper 51–99% AGI is the remainder.
5. Divide each bracket's total AGI (in $000s) by its return count to get average income per return in nominal dollars. Note these are per tax return, not per person — a married couple filing jointly counts as one return.
6. Concatenate the 1997–2012 interpolated results with the 2013–2022 direct calculations into a single dataset.
7. The WID long-run U.S. series is already processed (see `make_economy_income` pipeline) and is plotted as-is alongside the IRS state data to provide historical context.

### Internal Notes
* **2013–2022 data:** All AGI columns are in thousands of dollars for most years; 2014, 2016, and 2017 files are in full dollars — the pipeline normalizes this automatically by checking the U.S. national row magnitude.
* **1997–2012 data:** Five distinct file formats exist across these years (14-col vertical, stacked, wide stride-6, wide stride-10, and machine-readable CSV). Each requires a different parser; see `notebooks/pipeline_state_income_historic.ipynb` for details.
* **Accuracy caveat (2004–2009):** The 2004–2009 Historic Table 2 files have only 5 AGI brackets with the entire bottom of the distribution in "Under $50,000". Bottom 50% estimates for those years equal the mean of that bracket, which tends to overestimate the true value by ~$3–6k.
* The IRS `US` row (state == 'US') is used as the short-run U.S. comparison line; the WID data provides the long-run U.S. line.
* Pipeline for 2013–2022: `notebooks/pipeline_state_income.ipynb`
* Pipeline for 1997–2012: `notebooks/pipeline_state_income_historic.ipynb`

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

# Ballot
<!-- Live ballot sources are served from BALLOT_SOURCES in breathe_fastapi/main.py.
     This section documents the same sources for human reference.
     To add a new ballot cycle: add a new (area, year, None) entry to BALLOT_SOURCES.
     Naming convention: {area_lower}_ballot_{year}  (e.g. co_ballot_2025, mt_ballot_2026) -->

## co_ballot_2025
### Notes
Colorado 2025 statewide ballot measures — Healthy School Meals for All (Proposition LL and Proposition MM). Analysis covers ballot measure details from the Colorado Blue Book, peer-reviewed research on student outcomes, downstream effects of attendance and academic gains, program cost-benefit analysis, and limitations of the evidence. See docs/co_ballot_2025_analysis.md for full methodology, evidence-strength ratings, and areas needing further research.
### Sources
#### Ballot Measures & Program Data
* **Colorado 2025 Blue Book**: [Colorado Secretary of State, 2025 State Ballot Information Booklet](https://leg.colorado.gov/bluebook) — Official measure text, fiscal notes, and vote language for Prop LL and Prop MM
* **Proposition LL Fiscal Note**: Colorado Legislative Council Staff, *Fiscal Note: Proposition LL* (2025) — TABOR retention of $12.4M already collected; no new taxes
* **Proposition MM Fiscal Note**: Colorado Legislative Council Staff, *Fiscal Note: Proposition MM* (2025) — Income tax deduction limit change raising ~$95M/year for school meals and SNAP
* **Colorado 2023-24 Attendance**: [CDE News Release: "Colorado student attendance data from 2023-24 shows continued improvement" (August 2024)](https://cde.state.co.us/communications/newsrelease082224-attendance) — chronic absenteeism fell 3.4 pp (31.1% → 27.7%) in first year; 70% of districts improved
* **Colorado Program Page**: [CDE, Healthy School Meals for All Program](https://ed.cde.state.co.us/nutrition/nutrition-programs/healthy-school-meals-for-all-program) — program structure, eligibility, and participation data
#### Evidence on Attendance & Chronic Absenteeism
* **Attendance — NYC Kindergarteners**: [Schwartz & Trajkovski, *Exposure to Free School Meals in Kindergarten Has Lasting Positive Effects on Students’ Attendance*, Syracuse University Lerner Center (2023)](https://surface.syr.edu/lerner/208/) — Chronic absenteeism fell 5.4 pp; 1.8 additional school days/year
* **Systematic Review — Attendance & Outcomes**: [Vercammen et al., *Universal Free School Meals and School and Student Outcomes: A Systematic Review*, JAMA Network Open (2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11316229/) — Attendance "did not change or modestly improved" across 6 studies; certainty of evidence rated low
* **Massachusetts Attendance**: [Healey-Driscoll Administration, *Massachusetts Schools with Biggest Drop in Chronic Absenteeism* (2024)](https://www.mass.gov/news/healey-driscoll-administration-celebrates-massachusetts-schools-with-biggest-drop-in-chronic-absenteeism) — Chronic absenteeism fell 4.9 pp in year 2; largest single-year decline in state history
* **Minnesota First Year**: [Minnesota Department of Education, *Free School Meals: First Year Preliminary Summary* (2024)](https://education.mn.gov/mdeprod/idcplg?IdcService=GET_FILE&dDocName=PROD085180&RevisionSelectionMethod=latestReleased&Rendition=primary) — Chronic absenteeism down 1 pp; breakfast +40%, lunch +15%
* **California Trends**: [PACE, *Unpacking California’s Chronic Absence Crisis Through 2023-24*](https://edpolicyinca.org/publications/unpacking-californias-chronic-absence-crisis-through-2023-24) — Chronic absenteeism fell from 30% (2022) to 20.4% (2024); meals cited among multiple contributing factors
#### Evidence on Test Scores & Academic Performance
* **Test Scores — CEP South Carolina**: [Gordanier et al., *Free Lunch for All! The Effect of the Community Eligibility Provision on Academic Outcomes*, Economics of Education Review (2020)](https://www.sciencedirect.com/science/article/abs/pii/S0272775719307605) — Math scores +0.06 SD in elementary schools
* **Test Scores — CEP National**: [Ruffini, *Universal Access to Free School Meals and Student Achievement: Evidence from the CEP*, Journal of Human Resources, Vol. 57(3) (2022)](https://jhr.uwpress.org/content/57/3/776) — Effects concentrated in districts with low baseline free-meal eligibility; smaller effects in already-high-participation districts
* **Test Scores — Classroom Breakfast**: Imberman & Kugler, *The Effect of Providing Breakfast on Student Performance*, Journal of Policy Analysis and Management (2014) — Math and reading +0.10 SD vs. cafeteria breakfast
* **California Academic Evaluation**: [UC ANR Nutrition Policy Institute, *Evaluation of Universal School Meals in California* (2024–25)](https://ucanr.edu/program/nutrition-policy-institute/article/evaluation-universal-school-meals-california) — Multi-year longitudinal evaluation ongoing; no test score data published yet
* **Universal Meals Systematic Review**: [*Universal School Meals and Associations with Student Participation, Attendance, Academic Performance, Diet Quality, Food Security, and BMI: A Systematic Review*, Nutrients (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8000006/) — 12 studies; mixed results; positive attendance associations in Wisconsin and NYC
#### Evidence on Food Insecurity & Mental Health
* **Food Insecurity & State Meal Policies**: [AJPM (2025), *Statewide Universal School Meal Policies and Food Insecurity in Households With Children*](https://www.ajpmonline.org/article/S0749-3797(25)00433-7/fulltext) — States with universal meal policies had significantly lower household food insecurity rates
* **Food Insecurity & Child Mental Health**: Gundersen & Ziliak, *Food Insecurity and Health Outcomes*, Health Affairs (2015) — food-insecure children are ~2x as likely to experience anxiety, depression, and behavioral problems; review of 22 studies
* **Cognitive Tax of Scarcity**: Mani, Mullainathan, Shafir & Zhao, *Poverty Impedes Cognitive Function*, Science (2013) — financial scarcity imposes a cognitive bandwidth tax; note: specific magnitude has failed pre-registered replication (see Limitations)
* **Food Insecurity & Behavioral Problems**: Shanafelt et al., *Food Insecurity and Child Behavioral Problems in Fragile Families*, Maternal and Child Health Journal (2016) — food-insecure children more likely to exhibit behaviors leading to suspensions and reduced instructional time
* **Stigma & School Belonging**: Rosen et al., *Removing Stigma from School Meals*, Journal of School Health (2019) — economic stigma of free lunch receipt negatively affects self-concept and school engagement; universal programs eliminate this distinction
#### Why These Outcomes Matter — Downstream Effects
* **Early Grades Attendance & Reading**: Chang & Romero, *Present, Engaged, and Accounted For*, National Center for Children in Poverty / Columbia University (2008) — chronic absence in K–3 predicts 3rd grade reading; students not reading proficiently by 3rd grade are 4x more likely to drop out
* **Middle School Absenteeism & Dropout**: Balfanz & Byrnes, *Chronic Absenteeism: Summarizing What We Know*, Everyone Graduates Center, Johns Hopkins University (2012) — students chronically absent in 6th grade are 3x more likely to drop out
* **Dropout & Lifetime Earnings**: Rouse, *The Labor Market Consequences of an Inadequate Education*, Princeton University / Future of Children (2007) — dropouts earn $300,000–$400,000 less than graduates over their lifetimes
* **Effect Size Benchmarks**: Hattie, *Visible Learning: A Synthesis of Over 800 Meta-Analyses Relating to Achievement*, Routledge (2009) — 0.10 SD gain ≈ 3–4 months of additional learning; meta-analysis of 800+ educational interventions
* **Test Scores & Lifetime Earnings**: Chetty, Friedman & Rockoff, *Measuring the Impacts of Teachers II*, American Economic Review (2014) — 1 SD improvement in test scores raises lifetime earnings by ~$39,000; implies ~$3,900 per 0.10 SD gain
* **Test Scores & Economic Growth**: Hanushek & Woessmann, *The Role of Cognitive Skills in Economic Development*, Journal of Economic Literature (2008) — student test scores are the strongest single predictor of long-run GDP growth
* **Cost-Effectiveness Benchmark**: Kraft, *Interpreting Effect Sizes of Education Interventions*, Educational Researcher (2020) — 0.06–0.10 SD is comparable to class size reduction and extended learning time at far lower per-student cost
#### Program Cost vs. Societal Return
* **Lifetime Cost of a Dropout to Society**: Belfield & Levin, *The Price We Pay*, Brookings Institution Press (2007) — each dropout costs society an estimated $260,000–$290,000 in foregone taxes, increased welfare, and criminal justice costs (note: selection bias concerns; see Limitations)
* **Education & Crime Reduction**: Lochner & Moretti, *The Effect of Education on Crime*, American Economic Review (2004) — graduation reduces male arrest rates 10–20%; social savings from reduced crime estimated at $14,000–$26,000 per additional male graduate
* **Dropout & Government Assistance Dependence**: Alliance for Excellent Education, *The High Cost of High School Dropouts* (2011) — dropouts are 63% more likely to be incarcerated; significantly higher Medicaid, SNAP, and housing assistance use
* **School Meal Program Cost**: USDA Food and Nutrition Service, *National School Lunch Program: Reimbursement Rates* (2023–24) — ~$3.91/meal for free lunches; combined federal + state cost ~$500–$700/student/year
* **U.S. Global Competitiveness — Test Scores & GDP**: Hanushek & Woessmann, *The Knowledge Capital of Nations*, MIT Press (2015) — test scores are the single strongest predictor of long-run GDP growth; human capital quality drives economic productivity
* **U.S. PISA Rankings**: OECD, *PISA 2022 Results* (2023) — U.S. ranked ~26th in math out of 37 OECD countries; declined from 2018 to 2022
* **Achievement Gap & Economic Cost**: McKinsey Global Institute, *The Economic Impact of the Achievement Gap in America’s Schools* (2009) — closing the international achievement gap could add $1.3–$2.3T to GDP
* **Return on Education Investment**: Moretti, *The New Geography of Jobs*, Houghton Mifflin Harcourt (2012) — each additional graduate creates positive spillover effects; social returns exceed private returns
#### Limitations & Evidence Quality — Areas Needing Further Research
* **State attendance trends are descriptive, not causal** — No study isolates the meal effect from COVID recovery and concurrent policies in the 2022–23 programs. All state trend data is multi-causal. Needed: quasi-experimental studies with district-level controls within these states.
* **$260K dropout cost — selection bias concern** — Belfield & Levin (2007) aggregates outcomes without fully controlling for pre-existing disadvantage. Actual causal effect is likely lower ($100K–$150K). Needed: instrumental variable estimates.
* **CEP research may not generalize to statewide universal programs** — Ruffini (2022) found effects concentrate in low-participation districts. States with already-high uptake may see smaller marginal effects. Needed: statewide-specific evaluations; California UC ANR study forthcoming.
* **Cognitive tax of scarcity (Mani et al. 2013) — replication failure** — The "13 IQ point" finding was not reproduced in a 2021 pre-registered replication. Directional claim (stress impairs cognition) holds; specific magnitude is contested.
* **Mental health causal chain established in parts, not end-to-end** — No single study measures the full path from universal meals to clinical mental health outcomes to academic improvement. Needed: longitudinal studies with validated instruments (e.g., PHQ-A, GAD-7).
* **U.S. competitiveness — inferential chain too long for direct attribution** — Hanushek & Woessmann operate at national level over decades; 0.06–0.10 SD is small relative to the ~1.5 SD international gap. Appropriate as broad educational investment context, not a direct attribution to this program.
