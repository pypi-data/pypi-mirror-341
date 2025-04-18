#pragma once
#include <iostream>
#include <vector>
#include <Eigen/Dense>

/**
 * @brief Three-dimensional double Vector
*/
typedef Eigen::Vector3d Vector;

typedef Eigen::Vector3i UnsignedVector;

/**
 * @brief A derived Vector class that is automatically normalised when initialised.
 * 
 */
class Unit_Vector : public Vector{
    public:
    Unit_Vector(const Vector& vector_in);
    Unit_Vector(double m1, double m2, double m3);

    void Write() const;
    private:
    Unit_Vector(){};
};

/**
 * Returns the stellarator symmetric Unit_Vector corresponding to 
*/
Unit_Vector Stellarator_Symmetric_Unit_Vector(Unit_Vector uv_in, double phi_in);

