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
  * --password your-password(otional)
  * --output-format (json|yaml|str) (optional| default=str)

commands:
  * test
  * get-all
  * get-host
  * get-guests
```
if password is not given it will be asked for.


## Example output

```
{
    "host": {
        "vendor": "IBM",
        "model": "System x3650 M3 -[7945ZDN]-",
        "vCPUs": 24,
        "memory": 77297299456
    },
    "guests": {
        "guests": [
            {
                "id": "10",
                "name": "my-test-vm",
                "os": "Ubuntu Linux (64-bit)",
                "memory": "10240",
                "vCPUs": 6,
                "hdd": 53802445321,
                "ipAddresses": [
                    "10.20.11.228",
                    "2001:db8:1:2:20c:29ff:fe0b:3f16",
                    "fe80::20c:29ff:fe0b:3f16"
                ],
                "state": "running"
            },
            {
                "id": "9",
                "name": "another-vm",
                "os": "Ubuntu Linux (64-bit)",
                "memory": "8192",
                "vCPUs": 8,
                "hdd": 53802445321,
                "ipAddresses": [
                    "10.20.11.229",
                    "2001:db8:1:2:20c:29ff:fe0c:697d",
                    "fe80::20c:29ff:fe0c:697d"
                ],
                "state": "running"
            }
        ]
    }
}
```
## License

MIT License