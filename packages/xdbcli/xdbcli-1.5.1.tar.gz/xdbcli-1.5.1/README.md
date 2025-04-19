# About
Universal python client for MYSQL, ORACLE, POSTGRES.

### Features
<ul>
    <li>Inline CLI usage</li>
    <li>Script usage</li>
    <li>CSV Export</li>
    <li>ZIP export result</li>
</ul> 

# Requirements

Language: `python>=3.6`

## Install requirements from internet

```shell
pip install -r requirements.txt
```

## Install requirements from local

1. Download package to specific platform
```shell
pip download --platform=manylinux1_x86_64 -r requirements.txt
```

2. Copy to destination and install from downloaded packages
```shell
pip install -r requirements.txt --no-index --find-links file:///path/to/packages
```

# Install pydb package

### pip
1. Download `pydb-x.y.z-py3-none-any.whl`
2. Upgrade pip
3. Install use pip

```shell
pip install --upgrade pip
pip install pydb-x.y.z-py3-none-any.whl
```

> NOTE: `x`.`y`.`z` equal pydb package version.

# Usage package
### CLI example
```shell
dbclient -c "postgres://user:password@hostname:port/database"
command> SELECT * FROM systems ORDER BY id;
+----+-----------------+------------+------------+
| id | system          | system_key | system_eng |
+----+-----------------+------------+------------+
| 1  | Анализаторы SNT | SNT        | None       |
| 2  | Капкан          | KAPKAN     | None       |
| 3  | Спайдер         | SPIDER     | SPIDER     |
| 4  | Профит          | PROFIT     | PROFIT     |
+----+-----------------+------------+------------+
```

### Script example

```python
from pydb.exporter import Exporter
from pydb.dbms import UniDbConnector


cfg = dict(host='localhost', port=3306, user='', password='', database='profit', dbms='mysql')
u = UniDbConnector(config=cfg)

q = 'SELECT * FROM table ;'
data = u.fetchall(query=q)

e = Exporter(filename='data')
e.to_csv(data=data)
```

# Build

```shell
python -m pip install --upgrade build
python -m build
```