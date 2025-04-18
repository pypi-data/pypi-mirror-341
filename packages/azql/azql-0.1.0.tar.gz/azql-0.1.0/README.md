# AZQL

AZQL is a tool for converting data files (CSV, TSV, JSON) to SQL DDL (Data Definition Language) scripts. It analyzes data files, detects data types, and generates appropriate SQL scripts for table creation.

## Features

- Analyzes data from CSV and JSON files
- Automatically detects column data types
- Generates SQL DDL scripts for table creation
- Supports multiple SQL dialects (including TSQL)
- Validates data integrity before conversion
- Customizable SQL formatting options
- CLI and Python module interfaces

## Installation

```bash
pip install azql
```

## CLI Usage

AZQL can be used as a command-line tool to convert data files to SQL DDL scripts:

```bash
# Convert a single CSV file to SQL DDL
azql convert data.csv --dialect tsql --schema dbo

# Process all supported files in a directory
azql convert ./data_directory ./sql_scripts

# Customize the conversion with options
azql convert users.json \
    --dialect tsql \
    --schema app \
    --sample-size 1000 \
    --drop-table
```

### CLI Options

- `--dialect`: SQL dialect to use (default: "tsql")
- `--schema`: Database schema name (default: "dbo")
- `--sample-size`: Number of rows to sample for type detection (default: 100)
- `--drop-table`: Include DROP TABLE statement in DDL
- `--style`: SQL formatting style (default: "input" [, "camel", "pascal", "snake"])
- `--skip-validatione`: Skip data validation (default: False)

## Python Module Usage

AZQL can also be imported and used as a Python module:

```python
from pathlib import Path
import azql

# Convert a single CSV file to a SQL DDL script
ddl = azql.convert("data.csv", dialect="tsql", schema="dbo")
print(ddl)

# Process all supported files in a directory
azql.convert(Path("data_directory"), export=True)

# Customize the conversion with parameters
ddl = azql.convert(
    "users.json",
    validate=True,
    sample_size=1000,
    dialect="tsql",
    schema="app",
    drop_table=True,
    style="default",
    export=False
)
```

## Example Output

```sql
IF OBJECT_ID('dbo.users', 'U') IS NOT NULL
    DROP TABLE [dbo].[users];

CREATE TABLE [dbo].[users] (
      [id] INT NOT NULL
    , [name] NVARCHAR(100) NOT NULL
    , [email] NVARCHAR(255) NOT NULL
    , [created_at] DATETIME
    , [is_active] BIT NOT NULL
);
```

## License

[GNU General Public License v3.0](LICENSE)

## Developer Notice

This package was developed with the assistance of GitHub Copilot for documentation and testing purposes. However, every line of code has been manually reviewed and verified by the developers to ensure quality and security.