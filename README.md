# TRE-server 🕰️
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

## Start the TRE server

Please set the environment variable `MASTER_KEY` in advance. 
If it is not set, a default value will be used.

The server will start with the following command:
```bash
$ make run
```

## References

- D. Boneh and M. Franklin, “Identity-based encryption from the Weil pairing,” Advances in cryptology - CRYPTO 2001. 21st annual international cryptology conference, Santa Barbara, CA, USA, August 19–23, 2001. Proceedings, pp.213–229, Berlin: Springer, 2001. link.springer.de/link/service/series/0558/bibs/2139/21390213
- D. Boneh and M. Franklin, “Identity-based encryption from the Weil pairing,” SIAM J. Comput., vol.32, no.3, pp.586–615, 2003.
- K. Takahashi, "E-Quality: Neutral Lotteries With Multiple Time-Release Cryptography on Blockchains," 2024 IEEE 13th Global Conference on Consumer Electronics (GCCE), Kitakyushu, Japan, 2024, pp. 1401-1402, doi: 10.1109/GCCE62371.2024.10760807.