# Welcome to Snowboard
Welcome to Project Snowboard

We will be using a Dash by Plotly Dashboard to replace Tableau as our visualisation tool.

Further documentation on the structure and architecture will be available on confluence in due time.

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

## Usage

To serve the code locally, use the below.

```Shell
poetry run python -m app
```

Then proceed to the route ```http://127.0.0.1:8050/``` to load up the dash by plotly dashboard.

This will update when we add additional routes and a landing page to navigate routes.

## Testing

To test the repository, we are using a combination of `pytest` and `dash.testing` toolkits

Pytest will be used to test python functions as part of our unit testing approach

Dash.testing will be used to test rendering and callback responses.

Both testing suites can be run via the below command:

```Shell
pytest
```

## Contributing

Please ensure that you follow the below steps to contribute to this repository.

If you have installed new dependancies to the venv, then run the below command:

```Shell
poetry add {pagckage name} # to add new package
poetry update # to update dependancies
```

This will allow other developers to install these dependancies on their system as well as update production.

Next, when creating a new `.py` file or fixing an existing file, please create a branch, and open a pull request to add this to the master branch.

Ensure all code is documented and tested as per the above testing documentation, and new unit tests are implemented for new functions.