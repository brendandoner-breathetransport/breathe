# Maps Section Documentation

This document describes the interactive maps available in the Breathe dashboard and their data sources, metrics, and usage.

## Overview
The dashboard provides several choropleth maps to visualize key metrics by US state. These maps help users explore differences in education spending, prison spending, income gaps, and mobility outcomes across the country.

## Maps Available

### 1. Education vs Prison %
**Key:** `education_vs_prison_investment`
- **Description:** Shows the percentage of per capita state spending allocated to education versus prison for each state.
- **Metric:** Education % of Total = Education Per Capita / (Education Per Capita + Prison Per Capita)
- **Data Source:** per_capita_spending_by_state.csv
- **Source:** U.S. Census Bureau, State and Local Government Finance
- **Visualization:** Plotly choropleth map, static (no zoom/pan), centered on the US.

### 2. Mobility Efficiency
**Key:** `mobility_efficiency`
- **Description:** Displays the "mobility efficiency score" for each state, defined as upward mobility rank per $10,000 spent on education.
- **Metric:** Mobility Efficiency Score = Upward Mobility (P25 Income Rank) / Education Per Capita * 10,000
- **Data Sources:** per_capita_spending_by_state.csv, tract_outcomes_state.csv
- **Source:** Opportunity Atlas, U.S. Census Bureau
- **Visualization:** Plotly choropleth map, static, centered on the US.

### 3. Upward Mobility Rank
**Key:** `mobility_rank`
- **Description:** Shows the average income rank of children from low-income families by state (upward mobility).
- **Metric:** Upward Mobility (P25 Income Rank)
- **Data Sources:** per_capita_spending_by_state.csv, tract_outcomes_state.csv
- **Source:** Opportunity Atlas
- **Visualization:** Plotly choropleth map, static, centered on the US.

### 4. White-Black Income Gap
**Key:** `race_income_gap`
- **Description:** Visualizes the gap in household income between white and black families by state.
- **Metric:** Income Gap ($)
- **Data Source:** state_income_wb.csv
- **Source:** U.S. Census Bureau, American Community Survey
- **Visualization:** Plotly choropleth map, static, centered on the US.

## Usage
- Select a map from the dropdown menu to view the corresponding visualization.
- All maps are interactive Plotly figures but have zoom/pan disabled for a consistent view.
- Hover over states to see detailed metric values.

## Data Sources
- All data files are located in the `data_raw/` or `data/` directories of the repository.
- Data is loaded using Pandas and mapped to state abbreviations using the `us` Python package.
- **Opportunity Atlas:** https://www.opportunityatlas.org/
- **U.S. Census Bureau:** https://www.census.gov/
- **American Community Survey:** https://www.census.gov/programs-surveys/acs/

## Technical Notes
- Maps are rendered using Plotly Express `choropleth` with `locationmode="USA-states"`.
- The dashboard is built with Shiny for Python and shinywidgets for interactive output.
- All map figures are created at the global scope and referenced in the output logic.

## Customization
- To add new maps, define a new function to create the Plotly figure and add its key to the dropdown and output logic.
- To change centering or scale, adjust the `projection_scale` and `center` parameters in the Plotly layout.

---

For more details or to contribute, see the [Breathe GitHub repository](https://github.com/brendandoner-breathetransport/breathe).
