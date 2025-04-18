# Climalysis: Your Toolkit for Climate Impact Analysis ☁️🌞
[![PyPI](https://img.shields.io/pypi/v/climalysis.svg)](https://pypi.org/project/climalysis/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Read the Docs](https://readthedocs.org/projects/climalysis/badge/?version=latest)](https://climalysis.readthedocs.io/en/latest/)
[![codebeat badge](https://codebeat.co/badges/1e41f852-36fb-456c-a4ac-27812db8082c)](https://codebeat.co/projects/github-com-climalysis-climalysis-main)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8105734.svg)](https://doi.org/10.5281/zenodo.8105734)
[![Tests](https://github.com/Climalysis/climalysis/actions/workflows/tests.yml/badge.svg)](https://github.com/Climalysis/climalysis/actions)



Developed by an assortment of active and past climate researchers, Climalysis is more than just a project – it's your one-stop platform for comprehensive climate impact analysis tools. 

**Project Lead:** Jake Casselman ([GitHub](https://github.com/jake-casselman))

---
## 🚀 Quickstart

Install Climalysis:

    pip install climalysis

Try your first analysis:

    from climalysis import nino_index, normalize_longitudes

    sst = nino_index("data/sst_monthly.nc", region="3.4").load_and_process_data()
    sst.plot()
---

**Our Mission:**

Climalysis seeks to propel climate research forward by democratizing access to advanced analytical tools. Our primary mission is to provide a robust, open-source platform that encourages both established researchers and novice enthusiasts to run their own analyses, fostering innovation and reproducibility in climate studies. We aim to eliminate duplicated effort, enabling our users to focus on fresh discoveries and insights. Through building a collaborative community, we aspire to continually identify and open-source new tools, accelerating the pace of climate research and enriching the understanding of our world's climate.

**What We Offer:**

Dive into our code, explore complex climate data, learn with us, and contribute your insights. Climalysis empowers you to extract insights from complex climate data.

---
Whether you're a climate scientist seeking advanced research tools, a data enthusiast, or simply curious about climate impacts, Climalysis invites you to join us. Explore, learn, contribute, and together, let's deepen our understanding of the world's climate and drive towards a sustainable future.

## Table of Contents

1. [Installation](#installation)
2. [Dependencies](#dependencies)
3. [Usage](#usage)
4. [Contributing](#contributing)
5. [License](#license)
6. [Contact](#contact)
7. [Acknowledgments](#acknowledgments)
8. [Supporters](#supporters)
9. [Conflict of Interest](#conflict-of-interest)

## Installation

Climalysis can be accessed either directly from the GitHub repository or through the Python package.

### GitHub Repository

First, clone the repository:

```shell
git clone https://github.com/Climalysis/climalysis.git
```

Next, navigate to the cloned repository and install the package:

```shell
cd climalysis
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install .
```

Ensure you have Python 3.7 or higher installed on your system before installation.

### Installing Python Package

You can also install Climalysis directly as a Python package:

```shell
pip install climalysis
```

## Dependencies

Climalysis requires the following Python packages:

- numpy==1.23.5
- scikit_learn==1.2.1
- scipy==1.9.3
- setuptools==67.8.0
- statsmodels==0.13.5
- xarray==2023.3.0

These packages can be installed using pip by running the following command in your terminal:

```bash
pip install climalysis
```

## Usage

After installation, you can import and use our package in your Python scripts:

```python
from climalysis import nino_index, normalize_longitudes

sst = nino_index("data/sst_monthly.nc", region="3.4").load_and_process_data()
sst.plot()

```

You can now access the functions/classes in these modules.

## Contributing

We warmly welcome contributions! Please see [here](CONTRIBUTING.md) for details on how to contribute. Have a look at the discussions if you need any ideas for where to contribute.

## License

This project is licensed under the terms of the GNU General Public License. See [LICENSE](LICENSE) for more details.

## Contact

If you have any questions, feel free to reach out to us. For major decisions, please consult with our project lead, Jake Casselman (jake.w.casselman@gmail.com).

## Acknowledgments

We would like to express our gratitude to all contributors and users of Climalysis. Your support is greatly appreciated.


## Conflict of Interest

We declare that there is no conflict of interest. The direction and goals of Climalysis are determined solely by the project team, independent of any external organizations.



