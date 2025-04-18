# AZQL SPECS

The `azql` is a cli tool that can create sql scripts based on data or configuration files (toml, json).

## Features

### Data to DDL

> As a user I want to create a `create table` script based on a data sample.

- read folders -> read file
- read file
  - csv (and a like, i.e. tsv)
  - json
  - excel
- guess data types -> TSQL
- rename columns
  - style presets: PascalCase, snake_case, camelCase
- create scripts
  - only create table if not exists
    - (maybe add force flag to cli to drop tables)
  - table layers: stage, core
  - view layers: dm, xui_reporting

- What are the naming convetions? Name of the file == name of the table?

### DDL to DB
> As a user I want to execute the scripts that were created

- authorize (azure.identity)
- execute (pyodbc)


### Data to DB
> As a user I want to load data using the scripts created