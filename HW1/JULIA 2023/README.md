# Homework 1: Julia Solutions

This directory contains **Julia** scripts (`prob1.jl` through `prob5.jl`) that replicate the solutions to Problems 1–5 using ETOPO1 / WOA data and TEOS‑10 routines. Even if you’re new to Julia, just follow these steps to get started.

---

## 0. Installing Julia and Required Packages

1. **Download Julia** from the official site: https://julialang.org/downloads/
   - Pick the latest **stable** release for your OS (Windows, macOS, Linux).
   - Run the installer and follow the prompts.

2. **Add Julia to your PATH** (usually done by the installer).

3. **Launch the Julia REPL** (open a terminal and type `julia`).

4. **Install the required packages** by entering the package manager. At the `julia>` prompt, type `]` to enter pkg mode, then:
   ```julia
   (v1.x) pkg> add NetCDF          # for reading ETOPO NetCDF files
   (v1.x) pkg> add GibbsSeaWater   # TEOS‑10 seawater routines
   (v1.x) pkg> add Plots           # optional, for any plotting
   (v1.x) pkg> activate .          # (optional) makes this folder a project environment
   (v1.x) pkg> instantiate         # (optional) install from Project.toml if provided
   ```
   Then press Backspace or Ctrl+C to exit pkg mode.

5. **Verify** that you can `using NetCDF, GSW, Plots` without errors.

---

## 1. Problem 1: Ocean Surface Area (prob1.jl)

Computes the total surface area of the oceans and of the entire Earth using the ETOPO1 data and
\[dA = a^2 \cos(φ)\,dφ\,dλ\].

**Usage**:
```bash
julia --project=. prob1.jl
```
**Output**:
- Ocean area (m²)
- Earth surface area (m²)
- Fraction covered by ocean

---

## 2. Problem 2: Ocean Volume (prob2.jl)

Calculates the volume of the world’s oceans via
\[dV = a^2 \cos(φ)\,dφ\,dλ\,dz\].

**Usage**:
```bash
julia --project=. prob2.jl
```
**Output**:
- Ocean volume (m³)

---

## 3. Problem 3: Volumetric Averages (prob3.jl)

Uses WOA data to compute the volumetrically averaged temperature and salinity:
\[\langle X\rangle = \frac{\int_V X\,dV}{\int_V dV}.\]

**Usage**:
```bash
julia --project=. prob3.jl
```
**Output**:
- Total volume (m³)
- Average temperature (°C)
- Average salinity (PSU)

---

## 4. Problem 4: Seasonal Profiles (prob4.jl)

Plots winter, spring, summer, and fall vertical profiles of temperature and salinity at ~45° N using WOA CSV data and TEOS‑10.

**Usage**:
```bash
julia --project=. prob4.jl
```
**Output**:
- Two-panel plot (you will need Plots.jl)

---

## 5. Problem 5: TEOS‑10 Coefficients & Mass (prob5.jl)

Computes over the top 200 m:
1. Volumetric average thermal expansion (α)
2. Volumetric average haline contraction (β)

And over full depth:
3. Total salt mass
4. Total freshwater mass

**Usage**:
```bash
julia --project=. prob5.jl
```
**Output**:
- α (1/K), β (per PSU) for top 200 m
- Salt mass (kg)
- Freshwater mass (kg)

---

### Tips
- Run `julia --project=. --color=yes` to ensure you’re using the local project environment.
- If you need help with a package at the REPL, type `?NetCDF` or `?gsw` to enter help mode.

Good luck and happy coding in Julia! 🚀

