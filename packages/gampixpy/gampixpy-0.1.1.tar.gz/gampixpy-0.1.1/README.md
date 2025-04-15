# GAMPixPy
Detector Simulation for GAMPix-based LArTPC designs, including GammaTPC and DUNE

## Getting Started

### Installation

Installation should be handled by `pip` and `setuptools`.  To install an editable version of the package, simply do

```
pip install -e [path containing setup.py]
```

### Minimal Simulation Example

An implementation of the simulation workflow is shown in `gampixpy/gampix_sim.py`

Minimally, one needs to instantiate a `DetectorModel` object (with configurations speciying the details of the TPC conditions).  Next, one makes an input parser from one of the pre-defined classes.  At this time, there are four planned parsers, but contributions are welcome!

  - Penelope (low-energy electron scattering, *planned*)
  - RooTracker (medium-energy GEANT4 tracking record, *implemented*)
  - QPix (a GEANT4-derived file format designed for input to a QPix-style detector simulation, *planned*)
  - EdepSim (medium-energy GEANT4 track record, *implemented*)

From the input parser, one then simply needs to get an event (or use the parser's `__iter__` method) and pass it to the DetectorModel object's `drift` and `readout` methods, which simulate the drift and detector/electronic response processes, respectively.  The representation of the input ionization image is updated and saved to the `Track` object at each step.

### Plotting

Also included in this package are some tools for producing plots of the simulation inputs and products.  See `plotting.py` for more details.  An example of how to use this tool is also shown in `gampix_sim.py`