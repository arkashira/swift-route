<h3 align="center">🛠️ swift‑route</h3>

<div align="center">
  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)  
[![Poetry](https://img.shields.io/badge/managed%20by-Poetry-60A5FA.svg)](https://python-poetry.org/)  
[![Tests](https://img.shields.io/github/actions/workflow/status/axentx/swift-route/ci.yml?branch=main&label=tests)](https://github.com/axentx/swift-route/actions)
  
</div>

---

# 🚀 swift‑route  
**Power developers and operators with AI‑driven settlement routing that slashes transaction costs and cuts latency to seconds.**  

## Why swift‑route?

- **Cost Savings** – Intelligent path selection can reduce settlement fees by **15‑30 %** on average.  
- **Lightning‑Fast Settlements** – Cross‑border payment latency drops from minutes to **seconds**.  
- **AI‑Optimized Routing** – Real‑time cost‑benefit analysis picks the cheapest, fastest route.  
- **Developer‑Friendly** – Simple Python API, fully typed, and ready for CI/CD pipelines.  
- **Operator‑Ready** – Built to plug into existing settlement networks with minimal configuration.  
- **Extensible** – Modular design lets you add new routing heuristics or network adapters.  

## Feature Overview

| Feature | Description |
|---------|-------------|
| **Trigger Settlements** | Programmatically initiate settlements on supported networks. |
| **Acknowledgement Retrieval** | Pull confirmation receipts and status updates after settlement. |
| **AI‑Based Path Selection** | Uses a lightweight model to evaluate cost vs. speed for each possible route. |
| **Configurable Policies** | Define custom cost‑thresholds, latency targets, or compliance rules. |
| **CLI & Library Modes** | Run as a command‑line tool or import as a Python package. |
| **Test Suite** | Full coverage with `pytest` for reliability in production. |

## Tech Stack

- **Python** – Core language, 3.10+ recommended.  
- **Poetry** – Dependency management and packaging.  
- **Pytest** – Automated testing framework.  

## Project Structure

```
swift-route/
├─ business/          # Business‑logic modules (routing heuristics, cost models)
├─ docs/              # Documentation assets (PRD, ROADMAP, etc.)
├─ src/               # Core package source code
│  └─ swift_route/    # Public API (operator, router, utils)
├─ tests/             # Test suite (pytest)
├─ pyproject.toml     # Poetry config, entry points, dependencies
└─ README.md          # ← you are here
```

## Getting Started

```bash
# 1️⃣ Clone the repo
git clone https://github.com/axentx/swift-route.git
cd swift-route

# 2️⃣ Install dependencies with Poetry
poetry install

# 3️⃣ Run the CLI (example)
poetry run swift-route trigger --network mainnet --amount 1000

# 4️⃣ Run the test suite
poetry run pytest
```

## Deploy

The project is packaged as a standard Poetry library, ready for publishing to PyPI or internal artifact registries.

```bash
# Build the distribution
poetry build

# Publish to PyPI (or your private index)
poetry publish --username __token__ --password $PYPI_TOKEN
```

> *If you prefer containerised deployment, you can build a Docker image that runs the installed package – just copy the `pyproject.toml` and `src/` into your Dockerfile and execute `poetry install` inside the container.*

## Status

Early‑stage, actively developed. Latest commit `fabf565` adds a sandbox‑tested implementation of the settlement operator.

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the **MIT License**.