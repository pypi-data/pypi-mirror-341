#include "Vector.h"

#include <math.h>

Unit_Vector::Unit_Vector(const Vector& vector_in) : Vector(vector_in.normalized()){}

Unit_Vector::Unit_Vector(double m1, double m2, double m3) : Vector(Vector(m1,m2,m3).normalized()){}


void Unit_Vector::Write() const{
    std::cout<<"Vector at "<<this<<": ["<<this->operator()(0)<<","<<this->operator()(1)<<","<<this->operator()(2)<<"]"<<'\n';
};
Unit_Vector Stellarator_Symmetric_Unit_Vector(Unit_Vector uv_in, double phi_in){
    auto phi_uv = atan2(uv_in[1], uv_in[0]);
    auto d_phi  = phi_in - phi_uv;

    auto Z_uv   = uv_in[2];
    auto factor = sqrt(( 1.0 - Z_uv * Z_uv));
    auto result = Unit_Vector(cos( phi_uv + 2 * d_phi) * factor , sin( phi_uv + 2 * d_phi) * factor, -Z_uv);
    
    return result;
}
