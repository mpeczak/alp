# Axion-like Particles at the LHC: Kinematic Plots

Use LHE files as input to plot kinetics and avaluate vbf acceptance

## To run

```bash
python3 main.py
```

Plots are saved to the output directory in `config.py`

---

# Structure

## `config.py`

Configuration file containing information about:

- Input LHE files
- Sample labels and colors (lists must be same length as list of files)
- Output directory
- Histogram binning
- Run-3 and HL-LHC selection cuts

---

## `physics.py`

All physics calculations

---

## `histograms.py`

Creates the histograms

---

## `plotting.py`

Random plotting utils:

- Histogram normalization
- Axis limits
- Peak finding
- etc.
- 
---

## `main.py`

Read LHE files --> parse events --> fill histograms --> plot
