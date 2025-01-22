
## Python Environment

Install a virtual python environment, probably in the home folder

`$ python -m venv python-venv`

Install all used `pip`-libraries:

```
$ ../../python-venv/bin/pip install requests
$ ../../python-venv/bin/pip install RPi.GPIO
$ ../../python-venv/bin/pip install python-dotenv
```

## Move files to raspberry pi zero

`$ scp working/directory/led-activator/main.py username@192.168.1.20:/home/username/projects/led-activator/main.py`

## Run files

`$ ../../python-venv/bin/python main.py`