# SBGeom

SBGeom is a package for creating parametric stellarator geometry from VMEC files and filament coils. 


Current features:

- Flux surfaces position including beyond the last closed flux surface
- Constant $\phi$ radial extension from last closed flux surface
- Discrete and fourier coils position and tangent
- Meshing of surfaces inside the plasma
- Meshing of surfaces outside the plasma by specifying a distance from the last closed flux surface
- Fourier transforming surfaces outside the plasma using equal-arclength parametrisation and non-equidistant surfaces
- Finite build coils using rotation-minimized frames
- Fourier transforming discrete coil filaments using equal-arclength parametrisation
- Meshing of watertight surfaces
- Meshing of layered geometries using tetrahedrons

Documentation at the moment only available at  https://s1668021.pages.tue.nl/sbgeom_v2/index.html (requires TU/e account).

## Installation

### Linux

Linux wheels are available on PyPi:

```
pip install sbgeom
```

For manual compilation, see below. 

### Windows and MacOS

No wheels are available. Compilation can be done by first cloning Eigen3 and setting the environment variable as :

```
git clone https://gitlab.com/libeigen/eigen.git
export EIGEN3_INCLUDE_DIR=$PWD/eigen/
```

Nanobind is used for binding generation:

``` 
pip install nanobind
```

Some C++20 features are used, so a compatible compiler is required. Then, install using 

```
pip install .
```

## TODO

This package was developed solely to satisfy the requirements I had at that time, and thus, some desirable features are not present.
Some features that could be especially useful include:

- Ports, divertors, intra-coil support structures
- Automated DAGMC conversions
- 