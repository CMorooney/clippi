voltage-controlled Video clip player for video synth fodder


on power up/after network connection there should be a local web site accessible for managing clips


note -- in order for this to succeed there must be an `.env` file at App root with the folling variables
```
WEB_APP_SECRET_KEY=your_secret_key
BANK_COUNT=number
BANK_SIZE=number
APP_PATH=path_to_root_of_application
BANKS_PATH=path_to_banks
```


for my working prototype the values (outside of the secret, lol) are:
```
BANK_COUNT=12
BANK_SIZE=12
APP_PATH='/home/calvin/App'
BANKS_PATH='/home/calvin/App/__CONTENT'
```


theoretically they should be able to be defined as whatever but the .gitignore importantly include the `__CONTENT` directory that is my BANKS_PATH. An important but unenforced coupling so just make sure whatever you use as your BANKS_PATH is in your .gitignore
