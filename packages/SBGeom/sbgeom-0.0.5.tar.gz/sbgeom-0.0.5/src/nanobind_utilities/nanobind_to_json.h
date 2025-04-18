/***************************************************************************
* Copyright (c) 2019, Martin Renou                                         *
*                                                                          *
* Distributed under the terms of the BSD 3-Clause License.                 *
*                                                                          *
* The full license is in the file LICENSE, distributed with this software. *
****************************************************************************/

#pragma once

#include <string>
#include <vector>

#include "json.h"

#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <iostream>
#include "Matrix.h"
#include <nanobind/eigen/dense.h>
#include <nanobind/ndarray.h>

#include "json_utility.h"



template<typename T>
nanobind::object BJData_to_nanobind(const nlohmann::json& json_in){
    
    auto data = json_in.at("_ArrayData_").get<std::vector<T>>();
    if(json_in.at("_ArraySize_").size() == 1){        
        auto eigen_array = Eigen::Map<Eigen::Array<T, Eigen::Dynamic, 1>>(data.data(), json_in.at("_ArraySize_")[0].get<size_t>());
        return nanobind::cast(eigen_array, nanobind::rv_policy::copy);
    }
    else if(json_in.at("_ArraySize_").size() == 2){
        auto eigen_array = Eigen::Map<Eigen::Array<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>>(data.data(), json_in.at("_ArraySize_")[0].get<size_t>(), json_in.at("_ArraySize_")[1].get<size_t>());
        return nanobind::cast(eigen_array, nanobind::rv_policy::copy);        
    }
    else if(json_in.at("_ArraySize_").size() == 3){         
        std::vector<size_t> sizes;
        for(unsigned i = 0; i < 3; ++i){
            sizes.push_back( json_in.at("_ArraySize_")[i].get<size_t>());
        }
        auto result = nanobind::ndarray<nanobind::numpy, T, nanobind::ndim<3>, nanobind::c_contig, nanobind::device::cpu>(data.data(),{sizes[0], sizes[1], sizes[2]});
        return result.cast(nanobind::rv_policy::copy);        
    }
    else{
        throw std::invalid_argument("Array dimensions up to 3 are supported (input = " + std::to_string(json_in.at("_ArraySize_").size())+")" );
    }

    auto eigen_array = Eigen::Array<T, 1,1>().template setZero();
    return nanobind::cast(eigen_array, nanobind::rv_policy::copy);
}

template<typename T>
nlohmann::json nanobind_ndarray_to_BJData(const nanobind::handle& obj){
    typedef nanobind::ndarray<T, nanobind::device::cpu, nanobind::c_contig> ndarr;
    
    if(!nanobind::isinstance<ndarr>(obj)){
        throw std::invalid_argument("Wrong type of array used: ensure the data is Row-major ordered and on the cpu");
    }
    nlohmann::json result;

    result["_ArrayType_"] = BJDataType<T>();

    ndarr array_nd = nanobind::cast<ndarr>(obj);                    

    std::vector<size_t> dimension_sizes;
    size_t total_size = 1;
    for(unsigned i = 0; i < array_nd.ndim(); ++i){
        dimension_sizes.push_back(array_nd.shape(i));
        total_size = total_size * array_nd.shape(i);
    }
    result["_ArraySize_"] = dimension_sizes;

    result["_ArrayData_"] = Eigen::Map<Eigen::Array<T, Eigen::Dynamic, 1>>(array_nd.data(), total_size);
 

    return result;
}


namespace pyjson
{
    constexpr bool use_jdata = true;
    inline nanobind::object from_json(const nlohmann::json& j){
        if (j.is_null())
        {
            return nanobind::none();
        }
        else if (j.is_boolean())
        {
            return nanobind::bool_(j.get<bool>());
        }
        else if (j.is_number_unsigned())
        {
            return nanobind::int_(j.get<nlohmann::json::number_unsigned_t>());
        }
        else if (j.is_number_integer())
        {
            return nanobind::int_(j.get<nlohmann::json::number_integer_t>());
        }
        else if (j.is_number_float())
        {
            return nanobind::float_(j.get<double>());
        }
        else if (j.is_string())
        {
            return nanobind::str(j.get<std::string>().c_str());
        }
        else if (j.is_array())
        {
            nanobind::list obj;
            for (std::size_t i = 0; i < j.size(); i++)
            {
                obj.append(from_json(j[i]));
            }
            return obj;
        }
        else if (j.is_binary())
        {
            throw std::runtime_error("JSON object is binary, cannot decode into python object");
        }
        else // Object
        {
            if(use_jdata && j.size() == 3 && j.find("_ArrayType_") != j.cend() && j.find("_ArraySize_") != j.end() && j.find("_ArrayData_") != j.end()){                                                
                std::string type = j.at("_ArrayType_").get<std::string>();
                if(type == "double"){
                    return BJData_to_nanobind<double>(j);
                }
                else if(type == "uint32"){
                    return BJData_to_nanobind<unsigned>(j);
                }
                
            }
            nanobind::dict obj;
            for (nlohmann::json::const_iterator it = j.cbegin(); it != j.cend(); ++it)
            {
                obj[nanobind::str(it.key().c_str())] = from_json(it.value());
            }
            return obj;
        }
    }

    inline nlohmann::json to_json(const nanobind::handle& obj)
    {
        typedef nanobind::ndarray<> ndarr;
        if (obj.ptr() == nullptr || obj.is_none())
        {
            return nullptr;
        }
        if (nanobind::isinstance<nanobind::bool_>(obj))
        {
            return nanobind::cast<bool>(obj);
        }
        if (nanobind::isinstance<nanobind::int_>(obj))
        {
            try
            {
                nlohmann::json::number_integer_t s = nanobind::cast<nlohmann::json::number_integer_t>(obj);
                if (nanobind::int_(s).equal(obj))
                {
                    return s;
                }
            }
            catch (...)
            {
            }
            try
            {
                nlohmann::json::number_unsigned_t u = nanobind::cast<nlohmann::json::number_unsigned_t>(obj);
                if (nanobind::int_(u).equal(obj))
                {
                    return u;
                }
            }
            catch (...)
            {
            }
            throw std::runtime_error("to_json received an integer out of range for both nlohmann::json::number_integer_t and nlohmann::json::number_unsigned_t type: " + nanobind::cast<std::string>(nanobind::repr(obj)));
        }
        if (nanobind::isinstance<nanobind::float_>(obj))
        {
            return nanobind::cast<double>(obj);
        }    
        if (nanobind::isinstance<nanobind::str>(obj))
        {
            return nanobind::cast<std::string>(obj);
        }
        if (nanobind::isinstance<nanobind::tuple>(obj) || nanobind::isinstance<nanobind::list>(obj))
        {
            auto out = nlohmann::json::array();
            for (const nanobind::handle value : obj)
            {
                out.push_back(to_json(value));
            }
            return out;
        }
        if (nanobind::isinstance<nanobind::dict>(obj))
        {
            auto out = nlohmann::json::object();
            for (const nanobind::handle key : obj)
            {
                out[nanobind::cast<std::string>(nanobind::str(key))] = to_json(obj[key]);
            }
            return out;
        }
        if(nanobind::isinstance<ndarr>(obj)){
            ndarr a = nanobind::cast<ndarr>(obj);                    
            if(a.dtype() == nanobind::dtype<double>()){
                return nanobind_ndarray_to_BJData<double>(obj);
            }
            else if(a.dtype() == nanobind::dtype<uint32_t>()){
                return nanobind_ndarray_to_BJData<uint32_t>(obj);
            }
            else if(a.dtype() == nanobind::dtype<uint64_t>()){
                return nanobind_ndarray_to_BJData<uint64_t>(obj);
            }
            else if(a.dtype() == nanobind::dtype<int32_t>()){
                return nanobind_ndarray_to_BJData<int32_t>(obj);
            }
            else if(a.dtype() == nanobind::dtype<int64_t>()){
                return nanobind_ndarray_to_BJData<int64_t>(obj);
            }            
            else{
                throw std::runtime_error("np.ndarray has type incompatible with to_json");    
            }
            throw std::runtime_error("NDARRAY");
        }
        throw std::runtime_error("to_json not implemented for this type of object: " + nanobind::cast<std::string>(nanobind::repr(obj)));
    }
}

