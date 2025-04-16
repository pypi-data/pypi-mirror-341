# Steps to get started
Thanks for your interest in the Fianchetto TradeBot!
This QuickStart project is the perfect way to get started. Just follow the instructions below
and you'll be up & running in 2 minutes or less!

## Set up credentials
### Create credential files
Create the files that the application needs to connect to your exchange.

#### Exchange Account Information
`$> cp ./config/accounts.example.ini ./config/accounts.ini`

#### Exchange-Specific Credentials
For the exchange(s) you'd like to use, just copy the files and update them
with your credentials.

`$> cp ./config/etrade_config.example.ini ./config/etrade_config.ini`

`$> cp ./config/etrade_config.example.ini ./config/schwab_config.ini`

`$> cp ./config/ikbr_config.example.ini ./config/ikbr_config.ini`

`$> cp ./config/accounts.example.ini ./config/accounts.ini`

Note: These files contain your sensitive credentials. Please be sure to 
not check them in. The `.gitignore` file should automatically exclude them, but please be vigilant.

## Run & Enjoy!
`$> python ./main.py`
The services should be up on the default ports.
Order Execution Service (OEX) - Port `:8080`
[Coming Soon] Quote Service (Quotes) Port `:8081`
[Coming Soon] Trade Identification Service (Trident) `:8082`
[Coming Soon] Helm Service `:8083`

### The example here uses E*Trade. You will be prompted on the shell to enter the auth code
retrieved from the browser after the redirect. This code is valid for two hours, after which
you will be prompted again.

`$> curl -X GET localhost:8080/`