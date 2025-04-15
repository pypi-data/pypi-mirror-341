# Purem - High-Performance Mapping Operations
[![PyPI version](https://badge.fury.io/py/purem.svg)](https://pypi.org/project/purem/)
[![License: BUSL-1.1](https://img.shields.io/badge/license-BUSL--1.1-blue.svg)](https://worktif.com/documents/terms-of-service)

## Overview

**Purem** is an advanced high-performance computational library optimized for vectorized mathematical operations. This project focuses on efficient execution of element-wise transformations, including `softmax`, `exp`, and other mathematical functions, leveraging highly optimized assembly code for modern architectures.

## Key Features

Purem is a blazing-fast AI math engine that turns your Python formulas into native-speed vectorized execution. Achieve up to 80× faster performance on CPU/GPU/TPU — no rewrites, no dependencies, just speed. Designed for ML researchers, scientific computing, and production-grade workloads that can’t afford to wait.

---

## 🔧 Installation

Install the Python wrapper via pip:

```bash
pip install purem
```

📦 **Note:** Installation is quick, but `purem` must be initialized with a license before use.
[Setup](https://worktif.com/#start) takes less than a minute – we’re ready when you are.

---

## 🚀 Quickstart

### 1. Import and Initialize

```python
from purem import purem

purem.configure(license_key='your-license-key') # Auto-downloads and configures backend
```

Alternatively, if you already have the backend `.so` file:

```python
from purem import purem

purem.softmax([...])  # Initialized from local ./lib/libpurem.so
```

---

## 📁 Local Library Structure

If the backend `.so` is already downloaded manually, place it here:

```
your_project/
├── main.py
├── lib/
│   └── libpurem.so
```

---

## 🔐 License-Based Activation

To automatically download and configure the backend library:

1. Call `purem.configure(license_key='<your-license-key>')`
2. The system will download the `.so` file to `./lib/`
3. All functions will become available instantly after initialization

Without a valid license key:
- No `.so` will be downloaded
- The library won't work unless you provide the `.so` manually

---

## 🧠 Available Functions

After initialization, you can call:

```python
from purem import purem

purem.softmax([...])
...
```

> Full function list: See [API Reference](https://worktif.com/docs/basic-usage)

---

## 📦 Packaging Notes

This package does **not** bundle the `.so` file. You are required to:
- Use a license key to download it dynamically
- Alternatively, place it manually into `./lib/` folder before calling `init()`

---

## 🧪 Benchmark Tutorial

Visit the [Benchmark Tutorial](https://worktif.com/#benchmarks) to learn:
- How `Purem` compares to NumPy, PyTorch and Numba
- How it reaches low-level performance via native execution
- Why it's faster than traditional Python-based computation

---

## 📧 Distribution and Licensing

We **do not provide direct download links** for the backend.  
All users must either:
- Use their license key to install  
- Or receive `.so` file from verified sources

For access, contact us or visit: https://worktif.com/documents/terms-of-service

---

## 📚 Full Example

```python
import numpy as np
from purem import purem

# Automatic setup using license key
try:
    purem.configure(license_key='<your-license-key>')
except Exception as e:
    print(f"Setup failed: {e}")

data = np.array([1.0, 2.0, 3.0], dtype=float)
output = purem.softmax(data)

print(output)
```

---

## 🧠 Why Purem?

- 🔥 High level performance with zero Python overhead
- 🧪 Built-in benchmarking and scientific accuracy
- 🧩 Easy plug-and-play design
- 🔐 Secure and license-aware system

---

## 🛠 Advanced Usage & API Docs

Coming soon...