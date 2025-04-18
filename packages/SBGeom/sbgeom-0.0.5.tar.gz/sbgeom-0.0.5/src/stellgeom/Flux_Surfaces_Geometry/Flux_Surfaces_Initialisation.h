#pragma once
#include "Flux_Surfaces.h"
namespace Initialisation{

    template<typename T>
    std::unique_ptr<T> Construct(const nlohmann::json& json_in);

    template<>
    std::unique_ptr<Flux_Surfaces> Construct<Flux_Surfaces>(const nlohmann::json& json_in);
     
}