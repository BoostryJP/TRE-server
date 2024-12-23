# TRE-server
This product is a time server designed for Timed-Release Encryption.
As a cutting-edge application, it includes sample implementations of Multiple Timed-Release-Encryption and "E-Quality".

## Installation

### Create virtual environment
```bash
$ uv venv
```

### Install packages
```bash
$ make install
```

### Update lock file
```bash
$ make update
```

## Start the API server

Please set the environment variable `MASTER_KEY` in advance. 
If it is not set, a default value will be used.

The server will start with the following command:
```bash
$ make run
```
