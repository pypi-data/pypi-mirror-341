#pragma once
#include <Eigen/Dense>

typedef Eigen::Matrix<double,3,3,Eigen::RowMajor> Square_3x3_Matrix;

typedef Eigen::Matrix<double,4,4,Eigen::RowMajor> Square_4x4_Matrix;

typedef Eigen::Matrix<double,4,3,Eigen::RowMajor> Matrix_4x3;

typedef Eigen::Matrix<double,4,1>                 Matrix_4x1;

typedef Eigen::Array<double,Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> Array;
typedef Eigen::Array<std::complex<double>,Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> ComplexArray;

typedef Eigen::Array<unsigned,Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> UnsignedArray;
typedef Eigen::Array<int     ,Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> IntArray;

typedef Eigen::Array<double,Eigen::Dynamic,1> DynamicVector;
typedef Eigen::Array<std::complex<double>,Eigen::Dynamic,1> DynamicComplexVector;
typedef Eigen::Array<unsigned, Eigen::Dynamic,1> DynamicUnsignedVector;

typedef Eigen::Array<double, Eigen::Dynamic, 3, Eigen::RowMajor> VectorArray;
typedef Eigen::Array<unsigned, Eigen::Dynamic, 3, Eigen::RowMajor> UnsignedVectorArray;