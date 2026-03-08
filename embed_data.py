import pandas as pd
import polars as pl
from pathlib import Path
from datetime import date, datetime

from htmltools.tags import table


def get_path(schema, table_name, filetype):
    path = str(Path(__file__).parent / f"data/{schema}/{table_name}{filetype}")
    return path

def read_data(schema, table_name, dtype=None):
    if table_name=='outcomes_upward_mobility_jail':
        data = pl.from_pandas(
            pd.read_csv(
                get_path(schema=schema, table_name=table_name, filetype=".csv"),
                delimiter=",",
                dtype={
                    'fips_county': str,
                    'fips_state': str,
                    'value': float,
                    'state': str
                },
            )
        )
    else:
        data = pl.from_pandas(
            pd.read_csv(
                get_path(schema=schema, table_name=table_name, filetype=".csv"),
                delimiter=",",
            )
        )
    return data

def format_value(val) -> str:
    """
    Convert a Python value to its literal strinc representation.
    :param val:
    :return:
    """

    if val is None:
        return "None"
    elif isinstance(val, str):
        # escape any quotes inside the stirng like "you're"
        escaped = val.replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'")
        return f'"{escaped}"'
    elif isinstance(val, bool):
        return str(val)
    elif isinstance(val, float):
        return repr(val) # repr preserves precision
    elif isinstance(val, (date, datetime)):
        return f'"{val}"'
    else:
        return str(val)


def write_data_to_python_data_file(
        schema: str,
        table_name: str,
        path_output: str,
    ):
    """
    Converts a Polars DataFrame into a Python file
    with hardcoded dict data that Polars can read instantly.
    :param data:
    :param path_output:

    :return:
    """
    data = read_data(schema=schema, table_name=table_name)

    lines = []

    # --- File header ---------------------------------------------
    lines.append('"""')
    lines.append(f"Auto-generated data file from : {schema}.{table_name}")
    lines.append(f"Generated at: {datetime.now().isoformat()}")
    lines.append(f"Rows: {len(data):,}")
    lines.append(f"Columns: {data.columns}")
    lines.append('"""')
    lines.append("")
    lines.append("import polars as pl")
    lines.append("")

    # --- Metadata dict -------------------------------------------
    lines.append("METADATA = {")
    lines.append(f'    "source": "{schema}.{table_name}",')
    lines.append(f'    "generated_at": "{datetime.now().isoformat()}",')
    lines.append(f'    "row_count": {len(data)},')
    
    # Unique values for each string column (for filter dropdowns)
    lines.append('    "filter_options": {')
    for col in data.columns:
        if data[col].dtype == pl.Utf8:
            unique_vals = sorted(data[col].unique().drop_nulls().to_list())
            lines.append(f'        "{col}": {unique_vals},')
    lines.append("    },")
    
    # Pre-coputed KPIs
    numeric_cols = [col for col in data.columns if data[col].dtype in (pl.Float64, pl.Int64)]
    if numeric_cols:
        lines.append('    "kpis": {')
        for col in numeric_cols:
            lines.append(f'        "{col}_sum": {data[col].sum()},')
            lines.append(f'        "{col}_mean": {round(data[col].mean(),2)},')
            lines.append(f'        "{col}_min": {data[col].min()},')
            lines.append(f'        "{col}_max": {data[col].max()},')
        lines.append("    },")
    
    lines.append("}")
    lines.append("")
    
    # --- Embed data as a dict of lists ---------------------------------------------
    lines.append(f"{table_name} = pl.DataFrame({{")
    
    for col in data.columns:
        values = data[col].to_list()
        formatted = [format_value(val) for val in values]
        
        # Write in chunchs for readability
        lines.append(f'    "{col}": [')
        chunk_size = 10
        for i in range(0, len(formatted), chunk_size):
            chunk = formatted[i:i + chunk_size]
            lines.append(f"        {', '.join(chunk)},")
        lines.append("    ],")
        
    lines.append("})")
    lines.append("")
    
    # --- Create python file, i.e. python_data_file.py
    output = Path(path_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    
    file_size = output.stat().st_size
    print(f"Generated {path_output}")
    print(f"    Rows: {len(data):,}")
    print(f"    File size: {file_size:,} bytes ({file_size/1024:.1f} KB")
    
# --- Run script -------------------------------------------------------------------------------
if __name__ == "__main__":

    datasets = [
        dict(schema='economy', table_name='n_workers_full_time'),
        dict(schema='economy', table_name='shares_wid'),
        dict(schema='economy', table_name='shares_wid_full_distribution'),
        dict(schema='economy', table_name='tax'),
        dict(schema='economy', table_name='income_total'),
        dict(schema='economy', table_name='population'),
        dict(schema='economy', table_name='workers_ratio'),
        dict(schema='economy', table_name='f150'),
        dict(schema='american_dream', table_name='american_dream_kids'),
        dict(schema='american_dream', table_name='mobility_international'),
        # Healthcare
        dict(schema='healthcare', table_name='healthcare_cost_per_capita'),
        dict(schema='healthcare', table_name='healthcare_life_expectancy'),
        dict(schema='healthcare', table_name='healthcare_infant_mortality'),
        dict(schema='healthcare', table_name='healthcare_maternal_mortality'),
        dict(schema='healthcare', table_name='healthcare_suicide_rates'),
        # Environment
        dict(schema='environment', table_name='electricity_cost'),
        # Race
        dict(schema='race', table_name='outcomes_upward_mobility_jail'),
    ]

    for dataset in datasets:
        schema=dataset['schema']
        table_name=dataset['table_name']

        write_data_to_python_data_file(
            schema=schema,
            table_name=table_name,
            path_output=f"data/{schema}_{table_name}.py"
        )