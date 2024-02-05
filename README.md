# LZX/Eurorack compatible video clip player

![](https://github.com/CMorooney/clippi/blob/master/project_images/final_diagonal.jpg)
![](https://github.com/CMorooney/clippi/blob/master/project_images/blender_full_render_2.png)

# Features
- Store up to 12 banks of 12 clips via web interface
  - upload local videos or provide youtube links
- Visualize current clip playback % with neopixel ring
- Visualize current bank/clip with a 7 segment display
- Random/Sequential playback modes
- 'Hold' current clip mode
- All buttons/features can also be invoked with voltage triggers

# How to use
- clone repo onto RPi
- install python3 and set up virtual python env
- install [pexpect](https://pexpect.readthedocs.io/en/stable/install.html)
- install [mplayer](http://www.mplayerhq.hu/design7/dload.html)
- create alias for running python scripts with `sudo` and passing env variables to the virtual env
  - `alias supy='sudo -E env PATH=$PATH python3
- added this line to `/boot/config.txt`
  - `dtoverlay=gpio-shutdown,gpio_pin=21`
- create/enable system services to start web-app and clip player so they start on boot
- create `.env` file at repo root

player.service (the actual clip looper):
```
[Unit]
Description=clippi.player

[Service]
User=calvin
ExecStart=sudo -E env PATH=$PATH /home/calvin/env/bin/python3 /home/calvin/App/app.py
StartLimitIntervalSec=8
StartLimitBurst=1
Restart=always

[Install]
WantedBy=multi-user.target
```

app.service (the web-app):
```
[Unit]
Description=clippi

[Service]
ExecStart=/home/calvin/env/bin/python3 /home/calvin/App/web/RaspWebInterface.py
Restart=always

[Install]
WantedBy=default.target
```

I more/less followed instructions [here](https://www.makeuseof.com/what-is-systemd-launch-programs-raspberry-pi/)
to set up the system services

the content in the `.env` file you created should look like this:
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
