<h1 align="center">

**Giter**
</h1>
<h2 align="center">

![License](https://img.shields.io/github/license/Xcal1bur/Giter?style=flat-square)

![](giter.gif)
</h2>

# Table of Contents
- [Table of Contents](#table-of-contents)
- [Description](#description)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Github](#github)
  - [pip](#pip)
- [Usage](#usage)
- [Contribution](#contribution)
- [License](#license)

# Description
Command line application to quickly set up new repositories on Github and add
it as origin to your local repo.

# Requirements
- Python 3.6+
- git
- pygithub
- beautifulsoup4

# Installation
## Github
1. Check whether you have the correct version of python installed with ``python3 --version``
2. Clone the repository with ``git clone git@github.com:Xcal1bur/Giter.git``
## pip
- ``pip install -i https://test.pypi.org/simple/ giter``

# Usage
```
usage: giter.py [-h] [--init] [--https] [--create] [--doc]

Command line application to quickly set up a new remote repository, initialize
a local git repository and add the remote repo.

optional arguments:
  -h, --help    show this help message and exit
  --init, -i
  --https
  --create, -c
  --doc
```

# Contribution
Please feel free to report bugs, request features or add examples by submitting a pull request.

# License
Copyright (C) 2019  Xcal1bur

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/.
