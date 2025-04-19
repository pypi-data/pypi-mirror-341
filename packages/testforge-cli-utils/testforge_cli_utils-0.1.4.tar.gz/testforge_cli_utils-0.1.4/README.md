# TestForge

**TestForge** is a modular, CLI-based hardware/system-level test automation framework for validating technologies like CXL, PCIe, BMC, and firmware.

## Features

- Modular protocol support (CXL, IPMI/Redfish, PCIe)
- YAML-based configuration
- Rich CLI interface
- Scalable and pip-installable

## Installation
```bash
git clone [https://github.com/your-org/testforge.git](https://github.com/MARIOREDFOX/TestForge.git)
cd testforge
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
testforge version
```

## 📁 Project Structure

```text
testforge/
├── src/
│   └── testforge/
│       ├── cli.py
│       ├── core/
│       │   ├── executor.py
│       │   ├── loader.py
│       │   ├── reporter.py
│       │   └── logger.py
│       ├── protocols/
│       │   ├── __init__.py
│       │   ├── bmc/
│       │   │   ├── redfish.py
│       │   │   └── ipmi.py
│       │   ├── cxl.py
│       │   └── pcie.py
│       ├── tests/
│       │   ├── __init__.py
│       │   ├── firmware/
│       │   ├── stress/
│       │   ├── health/
│       │   └── regression/
│       ├── config/
│       │   └── config_loader.py
│       ├── utils/
│       │   ├── ssh.py
│       │   ├── retry.py
│       │   └── parser.py
├── tests/
│   └── test_executor.py
├── examples/
│   ├── env.yaml
│   └── test_config.yaml
├── docs/
│   └── architecture.md
├── LICENSE
├── README.md
├── setup.py
├── setup.cfg
└── pyproject.toml
```
## Usage

```bash
pip install testforge
testforge run --tag firmware
testforge run --env examples/env.yaml

python3 -m unittest discover tests
```
## License
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

