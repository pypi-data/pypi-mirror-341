#include "Conversion_Tools.h"
#include "custom_assert.h"
std::vector<Unit_Vector> Unit_Vectors_From_Array(const VectorArray& array_in){
    auto result = std::vector<Unit_Vector>();

    for(unsigned i =0; i < array_in.rows(); ++i){
        result.push_back(Unit_Vector(array_in(i,0),array_in(i,1), array_in(i,2)));
    }
    return result;
}

DynamicVector Vector_to_Dynamic_Vector(const std::vector<double>& vec){
		auto result = DynamicVector(vec.size());
		for(unsigned i= 0; i < vec.size(); ++i){
			result[i] = vec[i];
		}
		return result;
};

std::vector<double> DynamicVector_to_Vector(const DynamicVector& vec_in){
    auto result = std::vector<double>();

    for(unsigned i =0; i < vec_in.rows(); ++i){
        result.push_back(vec_in[i]);
    }

    return result;
}

std::vector<unsigned> DynamicVector_to_Vector(const DynamicUnsignedVector& vec_in){
    auto result = std::vector<unsigned>();

    for(unsigned i =0; i < vec_in.rows(); ++i){
        result.push_back(vec_in[i]);
    }

    return result;
}

std::string Write(const Vector& v_in){
    std::stringstream os;
    os << "["<<v_in[0]<<", "<<v_in[1]<<", "<<v_in[2]<<"]";
    return os.str();
}



VectorArray Vector_Vector_to_VectorArray(const std::vector<std::vector<double>>& vec){
    auto result = VectorArray(vec.size(), 3);

    for(unsigned i = 0; i < vec.size(); ++i){
        sb_assert_message(vec[i].size() == 3, "Vector_Vector_to_VectorArray: Array second dimension ("+std::to_string(vec[i].size())+" not equal to 3");
        for(unsigned j = 0; j < vec[i].size(); ++j){
            result(i,j) = vec[i][j];
        }
    }
    return result;
};

std::vector<std::vector<DynamicVector>> VectorVectorDynamicVector_From_Contiguous3D(const Contiguous3D<double>& input) {
    auto output = std::vector<std::vector<DynamicVector>>();
        for(unsigned l = 0; l < input.Number_of_First_Index(); ++l){

            auto temporary_gout_gin = std::vector<DynamicVector>();
            for(unsigned gout = 0; gout < input.Number_of_Second_Index(); ++gout){
                
                auto temporary_gin = DynamicVector(input.Number_of_Third_Index(),1);

                for(unsigned gin = 0; gin < input.Number_of_Third_Index(); ++gin){
                    temporary_gin[gin] = input(l,gout,gin);
                }                    
                temporary_gout_gin.push_back(temporary_gin);
            }
            output.push_back(temporary_gout_gin);
        }
    return output;
}