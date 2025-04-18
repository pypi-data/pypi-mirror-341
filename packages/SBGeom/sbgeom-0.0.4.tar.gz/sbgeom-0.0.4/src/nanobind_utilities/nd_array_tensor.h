#pragma once
#include "Matrix.h"
#include "Vector.h"
#include <unsupported/Eigen/CXX11/Tensor>
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <filesystem>

#include "json.h"
namespace nb = nanobind;
Eigen::Tensor<double,3, Eigen::RowMajor> ND_Array_To_Tensor(nb::ndarray<double, nb::ndim<3>, nb::c_contig, nb::device::cpu> arg);

