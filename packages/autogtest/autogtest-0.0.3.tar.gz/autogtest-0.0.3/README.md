# autogtest

[![Release](https://img.shields.io/github/v/release/10-neon/autogtest)](https://img.shields.io/github/v/release/10-neon/autogtest)
[![Build status](https://img.shields.io/github/actions/workflow/status/10-neon/autogtest/main.yml?branch=main)](https://github.com/10-neon/autogtest/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/10-neon/autogtest)](https://img.shields.io/github/commit-activity/m/10-neon/autogtest)
[![License](https://img.shields.io/github/license/10-neon/autogtest)](https://img.shields.io/github/license/10-neon/autogtest)

Autogtest is a CLI tool for auto-generating Google Mock test code from C++ header files.

- **Github repository**: <https://github.com/10-neon/autogtest/>
- **Documentation** <https://10-neon.github.io/autogtest/>

## Features

- Automatically generates Google Mock classes from C++ abstract interfaces
- Supports both single file and batch processing modes
- Customizable Jinja2 templates for mock generation
- Handles nested namespaces and nested class

## Installation

```bash
pip install autogtest
```
## Basic Usage
Generate mock for a single header:
```bash
autogtest path/to/header.h --mock output/mock.h --include base/include
```
Batch process a directory:
```bash
autogtest path/to/headers/ --mock output/mocks/ --include base/include
```
## Command Options
```txt
autogtest [HEADER]
  --mock TEXT     Output path (file or directory)
  --include TEXT  Base include directory
  --template TEXT Custom template path
```
