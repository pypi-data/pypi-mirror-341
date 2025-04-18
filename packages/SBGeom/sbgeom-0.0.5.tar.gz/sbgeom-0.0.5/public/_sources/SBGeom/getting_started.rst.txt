Getting Started
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Internally, C++ is used for functions calls. To install this package, ensure 
you have `Eigen3 <https://gitlab.com/libeigen/eigen.git>`_ downloaded somewhere, e.g. using::

    git clone https://gitlab.com/libeigen/eigen.git

Then, the environment variable should be set as::
    
    export EIGEN3_INCLUDE_DIR=$PWD/eigen/

After this, simply run::
    
    pip install nanobind
    pip install .

which will compile the SBGeom package and install it (nanobind has to be installed before compiling).

Stubs are provided as well, so a suitable IDE can pick up on them and provide autocomplete and suggestions.


For development, an editable install can be used with::

    pip install -e .

where the package will reflect the changes in the repository.
