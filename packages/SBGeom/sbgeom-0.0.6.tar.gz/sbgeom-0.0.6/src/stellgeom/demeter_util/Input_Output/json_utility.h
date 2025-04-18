#pragma once
#include "json.h"
#include "iostream"
#include "fstream"
#include <string>
#include "Matrix.h"
#include <unsupported/Eigen/CXX11/Tensor>

nlohmann::json Parse_Input_JSON(char* argv);



void Output_Terminal_Header(std::string name);


/**
 * @brief Function that maps C++ types to BJData types
 * 
 * @tparam T 
 * @return std::string 
 */
template<typename T>
std::string BJDataType();



/**
 * @brief Function to map Eigen 2D array to BJData array
 * 
 * Rowmajor is enforced as this is the case in the BJData format.
 * Copies the data
 * 
 * @tparam T 
 * @param array 
 * @return nlohmann::json 
 */
template<typename T>
nlohmann::json Eigen_to_BJData(const Eigen::Array<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>& array){
    nlohmann::json result;
    result["_ArrayType_"] = BJDataType<T>();
    result["_ArraySize_"] = std::array<size_t, 2>({size_t(array.rows()), size_t(array.cols())});
    Eigen::Map<const Eigen::Array<T,Eigen::Dynamic,1>> map_data =Eigen::Map<const Eigen::Array<T,Eigen::Dynamic,1>>(array.data(), array.size());
    result["_ArrayData_"] = map_data;
    return result;
}


/**
 * @brief Function to map Eigen row vector to BJData array
 *  
 * Copies the data.
 * 
 * @tparam T 
 * @param array 
 * @return nlohmann::json 
 */
template<typename T>
nlohmann::json Eigen_to_BJData(const Eigen::Array<T, Eigen::Dynamic, 1>& array){
    nlohmann::json result;
    result["_ArrayType_"] = BJDataType<T>();
    result["_ArraySize_"] = std::array<size_t, 1>({size_t(array.rows())});

    Eigen::Map<const Eigen::Array<T,Eigen::Dynamic,1>> map_data =Eigen::Map<const Eigen::Array<T,Eigen::Dynamic,1>>(array.data(), array.size());
    result["_ArrayData_"] = map_data;
    return result;
}



/**
 * @brief Function to map Eigen column vector to BJData array
 * 
 * The column vector information is lost as it is converted to a 1D vector.
 * Copies the data.  
 * 
 * @tparam T 
 * @param array 
 * @return nlohmann::json 
 */
template<typename T>
nlohmann::json Eigen_to_BJData(const Eigen::Array<T, 1, Eigen::Dynamic>& array){
    nlohmann::json result;
    result["_ArrayType_"] = BJDataType<T>();
    result["_ArraySize_"] = std::array<size_t, 1>({size_t(array.cols())});

    Eigen::Map<const Eigen::Array<T,Eigen::Dynamic,1>> map_data =Eigen::Map<const Eigen::Array<T,Eigen::Dynamic,1>>(array.data(), array.size());
    result["_ArrayData_"] = map_data;
    return result;
}

template<typename T, int N>
nlohmann::json Eigen_to_BJData(const Eigen::Array<T, Eigen::Dynamic, N, Eigen::RowMajor>& array){
    nlohmann::json result;
    result["_ArrayType_"] = BJDataType<T>();
    result["_ArraySize_"] = std::array<size_t, 2>({size_t(array.rows()), size_t(array.cols())});
    Eigen::Map<const Eigen::Array<T,Eigen::Dynamic,1>> map_data =Eigen::Map<const Eigen::Array<T,Eigen::Dynamic,1>>(array.data(), array.size());
    result["_ArrayData_"] = map_data;
    return result;
}

template<typename T, int N>
nlohmann::json Eigen_to_BJData(const Eigen::Tensor<T,N, Eigen::RowMajor>& array){
    nlohmann::json result;
    result["_ArrayType_"] = BJDataType<T>();

    std::vector<size_t> shape;
    for(int i =0; i < N; ++i){
        shape.push_back(array.dimension(i));
    }
    result["_ArraySize_"] = shape;
    Eigen::Map<const Eigen::Array<T,Eigen::Dynamic,1>> map_data =Eigen::Map<const Eigen::Array<T,Eigen::Dynamic,1>>(array.data(), array.size());
    result["_ArrayData_"] = map_data;
    return result;
}


/**
 * @brief Function to check whether the called Type corresponds to the actual type in the BJData array.
 * 
 * @tparam T 
 * @param json_in 
 */
template<typename T>
void Check_Type_BJData(nlohmann::json json_in){
    if(json_in.at("_ArrayType_") != BJDataType<T>()) {
        throw std::invalid_argument("Data type (" + json_in.at("_ArrayType_").get<std::string>()+") not equal to desired datatype ("+BJDataType<T>()+").");
    }
}

/**
 * @brief Function to create an 2D (rowmajor) Eigen Array by coping a BJData object
 * 
 * @tparam T 
 * @param json_in 
 * @return Eigen::Array<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> 
 */
template<typename T>
Eigen::Array<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> BJData_to_Eigen_2D(const nlohmann::json& json_in){    
    Check_Type_BJData<T>(json_in);
    if(json_in.at("_ArraySize_").size() != 2){
        throw std::invalid_argument("Data has dimensionality ("+std::to_string(json_in.at("_ArraySize_").size()) +") while 2 was required.");
    }
    auto vector_data = json_in.at("_ArrayData_").get<std::vector<T>>();
    
    return Eigen::Map<Eigen::Array<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>>(vector_data.data(), json_in.at("_ArraySize_")[0].get<size_t>(),json_in.at("_ArraySize_")[1].get<size_t>());
};

/**
 * @brief Function to create an 2D (rowmajor) Eigen Array by coping a BJData object
 * 
 * @tparam T 
 * @param json_in 
 * @return Eigen::Array<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> 
 */
template<typename T, int N>
Eigen::Array<T, Eigen::Dynamic, N, Eigen::RowMajor> BJData_to_Eigen_2D(const nlohmann::json& json_in){    
    Check_Type_BJData<T>(json_in);
    if(json_in.at("_ArraySize_").size() != 2){
        throw std::invalid_argument("Data has dimensionality ("+std::to_string(json_in.at("_ArraySize_").size()) +") while 2 was required.");
    }
    if(json_in.at("_ArraySize_")[1].get<size_t>() != N){
        throw std::invalid_argument("Data has second dimension " + std::to_string(json_in.at("_ArraySize_")[1].get<size_t>()) + "while "+std::to_string(N)+" is required.");
    }
    auto vector_data = json_in.at("_ArrayData_").get<std::vector<T>>();
    
    return Eigen::Map<Eigen::Array<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>>(vector_data.data(), json_in.at("_ArraySize_")[0].get<size_t>(),json_in.at("_ArraySize_")[1].get<size_t>());
};

/**
 * @brief Function to create an 1D (rowvector) Eigen Array by coping a BJData object
 * 
 * @tparam T 
 * @param json_in 
 * @return Eigen::Array<T, Eigen::Dynamic, 1> 
 */
template<typename T>
Eigen::Array<T, Eigen::Dynamic, 1> BJData_to_Eigen_1D(const nlohmann::json& json_in){    
    Check_Type_BJData<T>(json_in);
    if(json_in.at("_ArraySize_").size() != 1){
        throw std::invalid_argument("Data has dimensionality ("+std::to_string(json_in.at("_ArraySize_").size()) +") while 1 was required.");
    }
    auto vector_data = json_in.at("_ArrayData_").get<std::vector<T>>();
    return Eigen::Map<Eigen::Array<T, Eigen::Dynamic, 1>>(vector_data.data(), json_in.at("_ArraySize_")[0].get<size_t>());
};


/**
 * @brief Function to create an 2D (rowmajor) Eigen Array by coping a BJData object
 * 
 * @tparam T 
 * @param json_in 
 * @return Eigen::Array<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> 
 */
template<typename T>
Eigen::Tensor<T, 3, Eigen::RowMajor> BJData_to_Eigen_3D(const nlohmann::json& json_in){    
    Check_Type_BJData<T>(json_in);
    if(json_in.at("_ArraySize_").size() != 3){
        throw std::invalid_argument("Data has dimensionality ("+std::to_string(json_in.at("_ArraySize_").size()) +") while 3 was required.");
    }
    auto vector_data = json_in.at("_ArrayData_").get<std::vector<T>>();    
    auto vector_sizes  = json_in.at("_ArraySize_").get<std::vector<size_t>>();    
    return Eigen::TensorMap<Eigen::Tensor<T,3,Eigen::RowMajor>>(vector_data.data(), Eigen::Index(vector_sizes[0]),Eigen::Index(vector_sizes[1]),Eigen::Index(vector_sizes[2]));                
};
