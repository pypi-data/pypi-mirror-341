# EntroPy Sim

EntroPy Sim is a Python library for fast and simple simulations of chemical mixtures.

## Background

A ton of thermodynamics and chemical libraries exist, but have the following issues:
- They are very large or have many large dependencies, preventing us from using them in a serverless environment
- They're suited for scripts and scientific analysis, but not use in a production application
- They don't have a very convenient API. For example, to use Cantera we have to write a YAML file that it can load in
- They're not written in Python, requiring a build step (usually a Python wrapper around C++). Our Cantera build usually takes 10 minutes to run

We wanted a library that has a well-designed Python API, is very small, and is suited to fast, approximate simulations.

## Installation

```bash
pip install entropy-sim
```