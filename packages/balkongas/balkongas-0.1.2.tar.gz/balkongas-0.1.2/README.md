# BalkonGas Python

A small library to interact with the BalkonGas API for a reactor. It allows you to get the latest values for a reactor.


## 📦 Installation

```sh
pip install balkongas
```

## 🚀 Quick start

In this example, we create a reactor based on the data from this URL https://api.balkongas.de/metrics/6f1d3382-6b95-4adc-9d6f-6785ae0456f3/json/latest/


```python
from balkongas import Reactor
r = Reactor('6f1d3382-6b95-4adc-9d6f-6785ae0456f3')
r.refresh()
print(r.data["uptime_sec"])
```


## 🚀 Development

### 1️⃣ Setup a Local Development Environment

1. **Clone the repository**
   ```sh
   git clone https://github.com/balkongas/BalkonGas-Python.git
   cd balkongas
   ```
2. **Create a virtual environment**
   ```sh
   python -m venv .venv
   ```
3. **Activate the virtual environment**
   - **macOS/Linux:**
     ```sh
     source .venv/bin/activate
     ```
   - **Windows (CMD):**
     ```sh
     .venv\Scripts\activate
     ```
   - **Windows (PowerShell):**
     ```sh
     .venv\Scripts\Activate.ps1
     ```
4. **Install dependencies**
   ```sh
   pip install -e .[dev]
   ```

### 2️⃣ Running Tests
To run tests using `pytest`, use:
```sh
pytest
```

### 3️⃣ Building the Package
To build the package, run:
```sh
python -m build
```
This will generate a `dist/` directory with `.tar.gz` and `.whl` files.

### 4️⃣ Uploading to PyPI
1. **Ensure you have Twine installed**
   ```sh
   pip install twine
   ```
2. **Upload the package**
   ```sh
   twine upload dist/*
   ```
3. **Verify installation from PyPI**
   ```sh
   pip install balkongas
   ```

---

Now you're ready to develop, test, and distribute `balkongas`! 🚀



