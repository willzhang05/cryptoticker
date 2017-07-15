# Cryptocurrency Market Ticker #

## Setting up environment ##

* `virtualenv env -p python3`

* `source env/bin/activate`

* `pip install -r requirements.txt` will install the required packages.

* `aws configure` if not done already, set up IAM user for Zappa before this step.

* `zappa init`

* `zappa deploy <your branch>`

* `zappa update <your branch>` to update Lambda function.
