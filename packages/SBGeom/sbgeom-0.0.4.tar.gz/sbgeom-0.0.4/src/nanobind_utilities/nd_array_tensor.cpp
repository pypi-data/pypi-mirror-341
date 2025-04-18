#include "nd_array_tensor.h"

namespace nb = nanobind;
Eigen::Tensor<double,3, Eigen::RowMajor> ND_Array_To_Tensor(nb::ndarray<double, nb::ndim<3>, nb::c_contig, nb::device::cpu> arg){
    Eigen::Tensor<double,3, Eigen::RowMajor> result(Eigen::Index(arg.shape(0)), Eigen::Index(arg.shape(1)), Eigen::Index(arg.shape(2)));
    for(Eigen::Index i =0; i < arg.shape(0); ++i){
        for(Eigen::Index j =0; j < arg.shape(1); ++j){
            for(Eigen::Index k =0; k < arg.shape(2); ++k){
                result(i,j,k) = arg(i,j,k);
            }
        }
    }
    return result;
}