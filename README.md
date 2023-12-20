voltage-controlled Video clip player for video synth fodder

The clip-player app will start automatically on pi boot

the auto-start is registered as `player.service` in
> /lib/systemd/system/

(followed instructions [here](https://www.makeuseof.com/what-is-systemd-launch-programs-raspberry-pi/))

all the boot service does is start `app.py`

after the clip-player app starts a LAN website/server should start. check web/README.


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


## CHANGES OUTSIDE THE REPO
this was added to `/boot/config.txt`:
`dtoverlay=gpio-shutdown,gpio_pin=21`
so that I could use that pin for shut down (though I still have to use SCL pin for boot-up)


`consoleblank=1 vt.global_cursor_default=0` was appended to `/boot/cmdline.txt` to remove boot splash image and console/cursor
