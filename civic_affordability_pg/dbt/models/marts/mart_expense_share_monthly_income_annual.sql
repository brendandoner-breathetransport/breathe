WITH affordability AS (
    SELECT * FROM {{ ref('mart_affordability_index_annual') }}
),
assumptions AS (
    SELECT
        {{ var('mortgage_base_home_price', 400000) }}::numeric AS mortgage_base_home_price,
        {{ var('mortgage_down_payment_pct', 0.20) }}::numeric AS mortgage_down_payment_pct,
        {{ var('mortgage_annual_rate', 0.065) }}::numeric AS mortgage_annual_rate,
        {{ var('mortgage_term_years', 30) }}::numeric AS mortgage_term_years
),
mortgage_inputs AS (
    SELECT
        a.geo_id,
        a.state_abbrev,
        a.year,
        a.income_real,
        a.income_real_cpi_2023,
        a.healthcare_pc,
        a.healthcare_pc_cpi_2023,
        a.childcare_annual,
        a.childcare_annual_cpi_2023,
        ass.mortgage_base_home_price,
        ass.mortgage_down_payment_pct,
        ass.mortgage_annual_rate,
        ass.mortgage_term_years,
        ass.mortgage_base_home_price * (a.housing_index / 100.0) AS estimated_home_price,
        ass.mortgage_annual_rate / 12.0 AS monthly_rate,
        ass.mortgage_term_years * 12.0 AS num_payments
    FROM affordability a
    CROSS JOIN assumptions ass
),
mortgage_calc AS (
    SELECT
        *,
        estimated_home_price * (1.0 - mortgage_down_payment_pct) AS estimated_loan_amount
    FROM mortgage_inputs
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
    estimated_home_price,
    estimated_loan_amount,
    CASE
        WHEN monthly_rate = 0 THEN estimated_loan_amount / NULLIF(num_payments, 0)
        ELSE
            estimated_loan_amount
            * (
                monthly_rate * POWER(1 + monthly_rate, num_payments)
            )
            / NULLIF(POWER(1 + monthly_rate, num_payments) - 1, 0)
    END AS estimated_monthly_mortgage_payment,
    ((healthcare_pc / 12.0) / NULLIF(income_real / 12.0, 0)) * 100.0 AS healthcare_share_pct_of_monthly_income,
    ((childcare_annual / 12.0) / NULLIF(income_real / 12.0, 0)) * 100.0 AS childcare_share_pct_of_monthly_income,
    (
        (
            (healthcare_pc + childcare_annual) / 12.0
            + (
                CASE
                    WHEN monthly_rate = 0 THEN estimated_loan_amount / NULLIF(num_payments, 0)
                    ELSE
                        estimated_loan_amount
                        * (
                            monthly_rate * POWER(1 + monthly_rate, num_payments)
                        )
                        / NULLIF(POWER(1 + monthly_rate, num_payments) - 1, 0)
                END
            )
        ) / NULLIF(income_real / 12.0, 0)
    ) * 100.0 AS known_expense_share_pct_of_monthly_income,
    ((healthcare_pc_cpi_2023 / 12.0) / NULLIF(income_real_cpi_2023 / 12.0, 0)) * 100.0 AS healthcare_share_cpi_2023_pct_of_monthly_income,
    ((childcare_annual_cpi_2023 / 12.0) / NULLIF(income_real_cpi_2023 / 12.0, 0)) * 100.0 AS childcare_share_cpi_2023_pct_of_monthly_income,
    (
        (
            (healthcare_pc_cpi_2023 + childcare_annual_cpi_2023) / 12.0
            + (
                CASE
                    WHEN monthly_rate = 0 THEN estimated_loan_amount / NULLIF(num_payments, 0)
                    ELSE
                        estimated_loan_amount
                        * (
                            monthly_rate * POWER(1 + monthly_rate, num_payments)
                        )
                        / NULLIF(POWER(1 + monthly_rate, num_payments) - 1, 0)
                END
            )
        ) / NULLIF(income_real_cpi_2023 / 12.0, 0)
    ) * 100.0 AS known_expense_share_cpi_2023_pct_of_monthly_income,
    (
        (
            CASE
                WHEN monthly_rate = 0 THEN estimated_loan_amount / NULLIF(num_payments, 0)
                ELSE
                    estimated_loan_amount
                    * (
                        monthly_rate * POWER(1 + monthly_rate, num_payments)
                    )
                    / NULLIF(POWER(1 + monthly_rate, num_payments) - 1, 0)
            END
        )
        / NULLIF(income_real / 12.0, 0)
    ) * 100.0 AS estimated_mortgage_share_pct_of_monthly_income,
    (
        (
            CASE
                WHEN monthly_rate = 0 THEN estimated_loan_amount / NULLIF(num_payments, 0)
                ELSE
                    estimated_loan_amount
                    * (
                        monthly_rate * POWER(1 + monthly_rate, num_payments)
                    )
                    / NULLIF(POWER(1 + monthly_rate, num_payments) - 1, 0)
            END
        )
        / NULLIF(income_real_cpi_2023 / 12.0, 0)
    ) * 100.0 AS estimated_mortgage_share_cpi_2023_pct_of_monthly_income
FROM mortgage_calc
ORDER BY geo_id, year
