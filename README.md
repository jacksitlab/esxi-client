# Esxi-client

This is a python cli using only http. So no need for enableing SSH on Esxi host.

tested with esxi server version:

  * 6.5
  * 7.0

## dev env

```
$ python 3 -m venv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

## usage

```
$ python3 esxi-client.py params command

params:
  * --host your-host-ip 
  * --user your-user-or-root 
  * --password your-password(otional) - if not given it will be asked for
  * --output-format (json|yaml|str) (optional| default=str)

commands:
  * test
  * get-list
```
if password is not given it will be asked for.

## License

MIT License