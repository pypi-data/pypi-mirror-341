#pragma once
#include "sstream"
#include "Matrix.h"
#include "Vector.h"
#include <unsupported/Eigen/CXX11/Tensor>
#include "Contiguous_Arrays.h"
#include <unsupported/Eigen/Splines>

std::vector<Unit_Vector> Unit_Vectors_From_Array(const VectorArray& array_in);
DynamicVector Vector_to_Dynamic_Vector(const std::vector<double>& vec);

VectorArray Vector_Vector_to_VectorArray(const std::vector<std::vector<double>>& vec);

std::vector<double> DynamicVector_to_Vector(const DynamicVector& vec_in);


std::string Write(const Vector& v_in);

std::vector<std::vector<DynamicVector>> VectorVectorDynamicVector_From_Contiguous3D(const Contiguous3D<double>& input) ;

template<typename T>
std::vector<Eigen::Array<T, Eigen::Dynamic, 1>> Array_to_VectorVector(const Eigen::Array<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>& array){
    std::vector<Eigen::Array<T, Eigen::Dynamic, 1>> result;
    for(size_t i = 0; i < array.rows(); ++i){
        result.push_back(Eigen::Array<T, Eigen::Dynamic, 1>(array.row(i)));
    }
    return result;
}

template<typename T>
Eigen::Array<T, Eigen::Dynamic, 1> Vector_to_Eigen_Array(const std::vector<T>& vec){
    Eigen::Array<T, Eigen::Dynamic, 1> result = Eigen::Array<T, Eigen::Dynamic, 1>(vec.size());
    for(size_t i = 0; i < vec.size(); ++i){
        result[i] = vec[i];
    }
    return result;
};

// Helper function to make it easier to interpolate values. However, it is rather slow for large input matrices (>1000), so use with care
template <typename T, unsigned k>
class SplineFunction
{
public:
    SplineFunction(const Eigen::Array<T, Eigen::Dynamic, 1> &x_vec, const Eigen::Array<T, Eigen::Dynamic, 1> &y_vec)
        : x_min(x_vec.minCoeff()), x_max(x_vec.maxCoeff()), m_spline(Eigen::SplineFitting<Eigen::Spline<T, 1>>::Interpolate(y_vec.transpose(), std::min<int>(x_vec.rows() - 1, k), scaled_values(x_vec)))
    {
    }

    double operator()(double x) const
    {
        // x values need to be scaled down in extraction as well.
        return m_spline(scaled_value(x))(0);
    }
    Eigen::Array<T, Eigen::Dynamic, 1> operator()(const Eigen::Array<T, Eigen::Dynamic, 1>& x){
        // auto result = Eigen::Array<T, Eigen::Dynamic, 1>(x.rows());
        // for(unsigned i = 0; i < x.rows(); ++i){
        //     result[i] = this->operator()(x[i]);
        // }
        // return result;
        return x.unaryExpr([this](T a){return this->operator()(a);});
    }

private:
    // Helpers to scale X values down to [0, 1]
    T scaled_value(T x) const
    {
        return (x - x_min) / (x_max - x_min);
    }

    Eigen::Array<T, 1, Eigen::Dynamic> scaled_values(const Eigen::Array<T, Eigen::Dynamic, 1>& x_vec) const
    {   
        return x_vec.unaryExpr([this](T x){ return scaled_value(x); }).transpose();
    }

    T x_min;
    T x_max;

    // Spline of one-dimensional "points."
    Eigen::Spline<T, 1> m_spline;
};