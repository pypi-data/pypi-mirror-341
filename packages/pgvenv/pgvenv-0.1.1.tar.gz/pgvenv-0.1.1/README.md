# Install PostgreSQL with pip install pgvenv

[![Github](https://img.shields.io/static/v1?label=GitHub&message=Repo&logo=GitHub&color=green)](https://github.com/Florents-Tselai/pgvenv)
[![PyPI](https://img.shields.io/pypi/v/pgvenv.svg)](https://pypi.org/project/pgvenv/)
[![pip installs](https://img.shields.io/pypi/dm/pgvenv?label=pip%20installs)](https://pypi.org/project/pgvenv/)

`pgvenv` is a Python package that embeds a fully isolated PostgreSQL installation
in your virtual environmnent.

```shell
pip install pgvenv
```

PostgreSQL will be built from source,
using `--prefix=$VENVPATH`.
Its binaries (`psql`,`pg_config`,`postgres` etc.)
will be put under `venv/bin` along with the `pip`, `python3` binaries.

```shell
python3.11 -m venv ./venv

PGVERSION=17.4 CFLAGS="-O2" PGCONFIGUREFLAGS="--without-icu" \
./venv/bin/pip install pgvenv
```

You can now use your favorite scripts
 
```shell
./venv/bin/pg_config --version # PostgreSQL 17.4
./venv/bin/initdb ./pgdata
./venv/bin/postgres -D ./pgdata
```

## Installation

This requires:

* Autoreconf
* The normal C compiler toolchain, such as gcc and make.
