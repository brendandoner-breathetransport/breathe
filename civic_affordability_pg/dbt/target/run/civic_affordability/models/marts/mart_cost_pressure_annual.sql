
  create view "postgres"."analytics"."mart_cost_pressure_annual__dbt_tmp"
    
    
  as (
    WITH affordability AS (
    SELECT * FROM "postgres"."analytics"."mart_affordability_index_annual"
)
SELECT
    geo_id,
    state_abbrev,
    year,
    (housing_index + healthcare_index + childcare_index) / 3.0 AS cost_pressure_index,
    ((housing_index + healthcare_index + childcare_index) / 3.0) - income_index AS affordability_gap_index
FROM affordability
ORDER BY geo_id, year
  );