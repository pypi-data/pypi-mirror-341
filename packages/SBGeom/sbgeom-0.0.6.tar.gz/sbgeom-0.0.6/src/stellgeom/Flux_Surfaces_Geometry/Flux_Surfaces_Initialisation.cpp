
#include "Flux_Surfaces_Initialisation.h"
#include "json_utility.h"
#include "Flux_Surfaces_Extended.h"
template<>
std::unique_ptr<Flux_Surfaces> Initialisation::Construct<Flux_Surfaces>(const nlohmann::json& json_in){
    std::string type = json_in.at("Type").get<std::string>();
    auto init_param  = json_in.at("Initialisation_Parameters");
    auto settings = Flux_Surface_Settings(init_param.at("Settings"));
    auto Rmnc     = BJData_to_Eigen_2D<double>(init_param.at("Rmnc"));
    auto Zmns     = BJData_to_Eigen_2D<double>(init_param.at("Zmns"));
    
    if(type == "Flux_Surfaces"){                
        return std::make_unique<Flux_Surfaces>(Rmnc, Zmns, settings);
    }
    else if(type == "Flux_Surfaces_Normal_Extended"){
        return std::make_unique<Flux_Surfaces_Normal_Extended>(Rmnc, Zmns, settings);
    }
    else if(type == "Flux_Surfaces_Normal_Extended_Constant_Phi"){
        return std::make_unique<Flux_Surfaces_Normal_Extended_Constant_Phi>(Rmnc, Zmns, settings);
    }
    else if(type == "Flux_Surfaces_Fourier_Extended"){
        auto d_extension        = BJData_to_Eigen_1D<double>(init_param.at("d_extension"));
        auto Rmnc_extension     = BJData_to_Eigen_2D<double>(init_param.at("Extension").at("Initialisation_Parameters").at("Rmnc"));
        auto Zmns_extension     = BJData_to_Eigen_2D<double>(init_param.at("Extension").at("Initialisation_Parameters").at("Zmns"));
        auto settings_extension = Flux_Surface_Settings(init_param.at("Extension").at("Initialisation_Parameters").at("Settings"));
        return std::make_unique<Flux_Surfaces_Fourier_Extended>(Rmnc, Zmns,settings, d_extension, Rmnc_extension, Zmns_extension, settings_extension);
    }
    else{
        throw std::invalid_argument("Type (" + type+") not recognized in Construct<Flux_Surfaces>!");
    }
    throw std::runtime_error("REEE");
    return NULL;    
}