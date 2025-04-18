#include "Norms.h"

namespace Norms{
    std::function<double(DynamicVector)> L_2   = [](DynamicVector diff_data){ return diff_data.matrix().squaredNorm();};
    std::function<double(DynamicVector)> RMSE  = [](DynamicVector diff_data){auto n_data = diff_data.rows(); return diff_data.matrix().squaredNorm() / sqrt(double(n_data));};
    std::function<double(DynamicVector)> L_inf = [](DynamicVector diff_data){return diff_data.matrix().lpNorm<Eigen::Infinity>(); };    
}
Norm String_to_Norm(std::string type){
    if(type == "L_2"){
        return Norms::L_2;
    }
    else if (type == "L_inf")
    {
        return Norms::L_inf;
    }
    else if(type == "RMSE")
    {
        return Norms::RMSE;
    }
    throw std::invalid_argument("Norm_Type " + type + " not recognized in Update_Energy_Group_Normed.");
    return Norms::L_2;
};