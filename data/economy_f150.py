"""
Auto-generated data file from : economy.f150
Generated at: 2026-03-08T14:59:20.495667
Rows: 74
Columns: ['year', 'price', 'notes']
"""

import polars as pl

METADATA = {
    "source": "economy.f150",
    "generated_at": "2026-03-08T14:59:20.495667",
    "row_count": 74,
    "filter_options": {
        "notes": [' ', ' 10th generation begins ', ' 11th generation begins ', ' 12th generation begins (aluminum body) ', ' 13th generation begins ', ' 2nd generation F-Series begins ', ' 3rd generation begins with styling changes ', ' 4th generation begins, integrated cab/box ', ' 50th anniversary of Ford Motor Company ', ' 5th generation begins ', ' 6th generation begins ', ' 7th generation begins ', ' 8th generation begins ', ' 9th generation begins ', ' F-150 introduced as heavy half-ton model ', ' Final year of 10th generation ', ' Final year of 11th generation ', ' Final year of 2nd generation ', ' Final year of 3rd generation ', ' Final year of 4th generation ', ' Final year of 5th generation ', ' Final year of 6th generation ', ' Final year of 7th generation ', ' Final year of 8th generation ', ' Final year of 9th generation ', ' Twin I-Beam suspension introduced '],
    },
    "kpis": {
        "year_sum": 147001,
        "year_mean": 1986.5,
        "year_min": 1950,
        "year_max": 2023,
        "price_sum": 1883395.0,
        "price_mean": 25451.28,
        "price_min": 15237.0,
        "price_max": 43925.0,
    },
}

f150 = pl.DataFrame({
    "year": [
        1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959,
        1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969,
        1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979,
        1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989,
        1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999,
        2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
        2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019,
        2020, 2021, 2022, 2023,
    ],
    "price": [
        16044.0, 15237.0, 15268.0, 15772.0, 15811.0, 16077.0, 16804.0, 18839.0, 18926.0, 19017.0,
        19358.0, 19778.0, 19892.0, 19962.0, 20010.0, 20121.0, 20024.0, 20680.0, 20399.0, 19838.0,
        19188.0, 18862.0, 19140.0, 19509.0, 19866.0, 20810.0, 21149.0, 21447.0, 21317.0, 21322.0,
        21033.0, 20661.0, 20392.0, 20944.0, 21159.0, 21529.0, 22251.0, 22878.0, 23133.0, 23252.0,
        23102.0, 23175.0, 23284.0, 23649.0, 24063.0, 25021.0, 26151.0, 27219.0, 27310.0, 27429.0,
        27598.0, 28263.0, 28931.0, 29280.0, 32616.0, 32430.0, 32221.0, 32179.0, 32256.0, 33365.0,
        33874.0, 33846.0, 34283.0, 35611.0, 35883.0, 38337.0, 38944.0, 39100.0, 39215.0, 39696.0,
        39763.0, 41902.0, 41775.0, 43925.0,
    ],
    "notes": [
        " 2nd generation F-Series begins ", " ", " ", " 50th anniversary of Ford Motor Company ", " ", " ", " Final year of 2nd generation ", " 3rd generation begins with styling changes ", " ", " ",
        " Final year of 3rd generation ", " 4th generation begins, integrated cab/box ", " ", " ", " ", " Twin I-Beam suspension introduced ", " Final year of 4th generation ", " 5th generation begins ", " ", " ",
        " ", " ", " Final year of 5th generation ", " 6th generation begins ", " ", " F-150 introduced as heavy half-ton model ", " ", " ", " ", " Final year of 6th generation ",
        " 7th generation begins ", " ", " ", " ", " ", " ", " Final year of 7th generation ", " 8th generation begins ", " ", " ",
        " ", " ", " ", " ", " ", " Final year of 8th generation ", " 9th generation begins ", " ", " ", " ",
        " ", " ", " ", " Final year of 9th generation ", " 10th generation begins ", " ", " ", " ", " Final year of 10th generation ", " 11th generation begins ",
        " ", " ", " ", " ", " Final year of 11th generation ", " 12th generation begins (aluminum body) ", " ", " ", " ", " ",
        " ", " 13th generation begins ", " ", " ",
    ],
})
