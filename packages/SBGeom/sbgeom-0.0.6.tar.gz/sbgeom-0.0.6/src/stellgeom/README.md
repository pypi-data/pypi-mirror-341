# StellGeom

Package for stellarator geometry with support for extensions beyond the last-closed flux surface in either normal-vector representation
or a fourier representation. Rather useless on its own, but its part of a to-be-released neutron code and thus seperated from there, while it is used 
by a simple python package SBGeom for creating and managing stellarator geometry objects.

# Setup

The Eigen library is used for the vector and array types. If already setup, simply add to your .bashrc

```
export EIGEN3_INCLUDE_DIR=path/to/eigen
```
(take care to point to the base directory, i.e. if you have the structure ~/eigen/eigen-3.4.0/Eigen the export should be ~/eigen/eigen-3.4.0)

Otherwise, use e.g. 

```
cd 
mkdir eigen
cd eigen
wget https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.zip 
unzip eigen-3.4.0.zip
```
and add to your .bashrc

```
export EIGEN3_INCLUDE_DIR="~/eigen/eigen-3.4.0/"
```

Now the subdirectories can be linked to from other cmake projects, e.g. 

```
add_subdirectory(stellgeom/demeter_util/math)    
add_subdirectory(stellgeom/demeter_util/Input_Output)
add_subdirectory(stellgeom/Flux_Surfaces_Geometry)
add_subdirectory(stellgeom/Coils)
```
