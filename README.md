# Dora the DNS explorer

## Dora

Dora is a DNS exfiltration tool that stores all DNS requests received that follow this syntax:

```<base64 data>.<line number>.<context>.<your domain>```

## Swiper

Swiper can be used to generate extraction payloads suitable for Dora.

## Requirements
- Python 3.x (tested with 3.8)
- Python requirements (I recommend to use `pipenv`)
- `tcpdump`

## Running

Dora uses `Scapy` to sniff on the specified interface on port `53` and parses all DNS requests it receives.
They can either be stored within a in-memory sqlite database, or saved to any database supported by `peewee`.

For Dora to receive those requests, make sure that your firewall does not block traffic to `UDP 53`.

`Scapy`'s sniffing uses `tcpdump` to read the packages so you don't need anything to actually listen on that port for Dora to work.
Therefore, you either need to start the tool with root privileges or utilize ambient capabilities as described below.

Help for the parameters can be retrieved by running `python dora.py -h` 

### Ambient capabilities

Since kernel version 4.3 capabilities can be passed to sub-processed.
For this to work, the included `ambient.c` file needs to be build and then capabilities need to be set on the binary.

For more information and source see: https://stackoverflow.com/a/47982075/920010

## Usage

As stated above, all DNS requests are simply saved into a database.
Using the API the entries can be retrieved, duplicate lines can be filtered and data can be aggregated.

### Contexts

A context is a 32 character hex string representing a UUIDv4 (although the last bit is not checked).

To create a random context ~~use the following snippet:~~ go to `/swiper/context`

## Further work

Working the API requires some manual work for choosing the correct lines. Therefore, open tasks include:
- If all available lines contain the same data, automatically select one at random
- Create a small web interface to instrument the API
- ~~Tool for random context generation~~
- (Add CLI)
