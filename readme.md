# Welcome to Snowboard
Welcome to Project Snowboard

We will be using a Dash by Plotly Dashboard to replace Tableau as our visualisation tool

== THIS IS CURRENTLY A POC AND SHOULD NOT BE USED FOR EXTERNAL REPORTING ==

## Installation

Firstly, ensure that Python3, Poetry, and Git are installed on your system. Then clone the repository:

```Shell
git clone {SSH/URL}
```

Then proceed to set up the `env.py` file with your snowflake connection for local development.

```Python
import snowflake.connector

# Connecting to Snowflake using the default authenticator
conn = snowflake.connector.connect(
    user="USERNAME",
    password="PASSWORD",
    account="PROD URL",
    warehouse="WAREHOUSE",
    database="DATABASE",
    schema="SCHEMA"
)
```
Finally, run the virtual environment via Poetry to begin development.
```Shell
poetry shell
poetry install
```

To serve the code locally, use the below.

```Shell
poetry run python -m main
```

Then proceed to the route ```/dashboard``` to load up the dash by plotly dashboard.

## Usage


## Testing

## Contributing
