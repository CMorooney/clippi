The web app will start automatically on pi boot/once a network connection is established

the auto-start is registered as app.service in
/lib/systemd/system/

(followed instructions [here](https://www.makeuseof.com/what-is-systemd-launch-programs-raspberry-pi/))

all the boot service does is start RaspWebInterface
