WITH affordability AS (
    SELECT * FROM {{ ref('mart_affordability_index_annual') }}
)
SELECT
    geo_id,
    state_abbrev,
    year,
    income_real / 12.0 AS monthly_income_real,
    income_real_cpi_2023 / 12.0 AS monthly_income_real_cpi_2023,
    healthcare_pc / 12.0 AS healthcare_monthly,
    healthcare_pc_cpi_2023 / 12.0 AS healthcare_monthly_cpi_2023,
    childcare_annual / 12.0 AS childcare_monthly,
    childcare_annual_cpi_2023 / 12.0 AS childcare_monthly_cpi_2023,
    ((healthcare_pc / 12.0) / NULLIF(income_real / 12.0, 0)) * 100.0 AS healthcare_share_pct_of_monthly_income,
    ((childcare_annual / 12.0) / NULLIF(income_real / 12.0, 0)) * 100.0 AS childcare_share_pct_of_monthly_income,
    (((healthcare_pc + childcare_annual) / 12.0) / NULLIF(income_real / 12.0, 0)) * 100.0 AS known_expense_share_pct_of_monthly_income,
    ((healthcare_pc_cpi_2023 / 12.0) / NULLIF(income_real_cpi_2023 / 12.0, 0)) * 100.0 AS healthcare_share_cpi_2023_pct_of_monthly_income,
    ((childcare_annual_cpi_2023 / 12.0) / NULLIF(income_real_cpi_2023 / 12.0, 0)) * 100.0 AS childcare_share_cpi_2023_pct_of_monthly_income,
    (((healthcare_pc_cpi_2023 + childcare_annual_cpi_2023) / 12.0) / NULLIF(income_real_cpi_2023 / 12.0, 0)) * 100.0 AS known_expense_share_cpi_2023_pct_of_monthly_income,
    -- Housing is represented in this MVP as an index, not monthly dollars.
    -- This proxy compares housing index to income index.
    (housing_index / NULLIF(income_index, 0)) * 100.0 AS housing_to_income_index_ratio_pct,
    (housing_index / NULLIF(income_cpi_2023_index, 0)) * 100.0 AS housing_to_income_cpi_2023_index_ratio_pct
FROM affordability
ORDER BY geo_id, year
