#pragma once
#include <functional>
#include "Matrix.h"

typedef std::function<double(DynamicVector)> Norm;
namespace Norms{
    extern std::function<double(DynamicVector)> L_2;     
    extern std::function<double(DynamicVector)> RMSE;
    extern std::function<double(DynamicVector)> L_inf;   
}

Norm String_to_Norm(std::string);