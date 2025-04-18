# SBGeom

Documentation available at  https://s1668021.pages.tue.nl/sbgeom_v2/index.html (requires TU/e account)



### Eigen3

Eigen3 is used in the underlying linear algebra routines, so it should be available somewhere. Clone the repository:

```
git clone https://gitlab.com/libeigen/eigen.git
```
and set the environment variable as 

```
export EIGEN3_INCLUDE_DIR=$PWD/eigen/
```
### Nanobind

nanobind is used to provide python bindings so it should be installed (e.g. in a conda environment):

``` 
pip install nanobind
```

### Compilation
Ensure you have a C++20 compatible compiler.

Then, simply run, in an appropriate virtual environment:

```
pip install .
```

An editable install for modifying python scripts:

```
pip install -e . 
```
