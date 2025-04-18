
mkdir src
mkdir src/nanobind_utilities
cp $1/src/nanobind_utilities/nanobind_to_json.cpp src/nanobind_utilities/
cp $1/src/nanobind_utilities/nanobind_to_json.h src/nanobind_utilities/
cp $1/src/nanobind_utilities/nd_array_tensor.h src/nanobind_utilities/
cp $1/src/nanobind_utilities/nd_array_tensor.cpp src/nanobind_utilities/

cp $1/src/nanobind_utilities/python_print.h src/nanobind_utilities/
cp $1/src/nanobind_utilities/python_print.cpp src/nanobind_utilities/

cp -r $1/src/SBGeom src/

cp -r $1/src/stellgeom src/

cp $1/src/StellBlanket/SBGeom/* src/SBGeom

mkdir examples
cp $1/src/Tests/Flux_Surfaces.ipynb examples/
cp $1/src/Tests/Coils.ipynb examples/
