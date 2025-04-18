#pragma once 
#include "Contiguous_Arrays.h"
#include <vector>
#include <array>
#include "Vector.h"
#include "json.h"
#include "Constants.h"
#include "Matrix.h"
#include "Mesh_Tools.h"
#include "Flux_Surface_Coords.h"
#include "Iterators.h"
class Coil_Set;

struct Arc_Length {
    Arc_Length(double a_in) :  m_arc(a_in){if(a_in < 0.0 || a_in > 1.0) throw std::invalid_argument("Trying to construct an arclength outside 0 or 1");}
    double Get_Arc_Length()const{return m_arc;}
    private:
    double m_arc;
};

class Coil{
    public:
    Coil(){};


    /**
    * @brief Returns a finite size rectangle at a specific point index
    * 
    * The finite size is constructed by first defining the tangential vector \f$\mathbf{T}_i\f$  (\f$ i \f$ the index of the considered vertex) 
    * as the  difference vector to the next point (normalised). The radial vector \f$\mathbf{N}_i\f$ is then defined using 
    * the centre of mass of the coil, \f$\mathbf{R}_c =  \frac{1}{N}\sum_j ^ N \mathbf{r}_j \f$
    * as \f$ \mathbf{N_i} = (\mathbf{r}_i  - R_c)  -  [(\mathbf{r}_i  - R_c)\cdot \mathbf{T}_i]\mathbf{T_i} \f$ which is after the fact normalised.
    * 
    * Then, the four finite size vertices are obtained by \f$ \pm \f$ combining \f$w_R \mathbf{N_i}\f$  and \f$ w_\phi \mathbf{N_i} \times \mathbf{T_i}\f$, 
    * where \f$ w_R \f$ is the width in radial direction (Coil::m_width_R) and \f$ w_\phi \f$ the width in toroidal direction (Coil::m_width_phi).
    * 
    * Note that the toroidal width is not full toroidal; it would only be the case for planar coils, but in general it corresponds to an intuitive toroidal direction width.
    * 
    * Virtual because it can be overriden by other finite sizes.
    * 
    * @param index vertex number
    * @return std::array<Vector,4> rectangle
    */
    virtual std::array<Vector, 4> Finite_Size_Centroid(Arc_Length arc_length, double width_phi, double width_R) const;

    virtual std::array<Vector, 4> Finite_Size_Frenet(Arc_Length arc_length, double width_phi, double width_R) const = 0;

    std::array<Vector, 4> Finite_Size_Rotated_From_Centroid(Arc_Length arc_length, double width_phi, double width_R, double angle_tan) const;

    VectorArray           Finite_Size_Lines_Centroid             (unsigned no_of_points, double width_phi, double width_R)                    const;    
    VectorArray           Finite_Size_Lines_RMF                  (unsigned no_of_points, double width_phi, double width_R)                    const;
    VectorArray           Finite_Size_Lines_Frenet               (unsigned no_of_points, double width_phi, double width_R)                    const;
    VectorArray           Finite_Size_Lines_Rotated_From_Centroid(unsigned no_of_points, double width_phi, double width_r, DynamicVector rot) const;
    
    virtual VectorArray Return_Sampling_Curve() const = 0;
    virtual Vector Position(Arc_Length arc_length) const = 0 ;

    virtual Unit_Vector Tangent(Arc_Length arc_length) const = 0;


    virtual void Write() const = 0;

    virtual ~Coil(){}

    Vector Get_Centre() const { return m_centre;}; 
    void Set_Centre(Vector centre)      { m_centre = centre;}; 


    
    Triangle_Vertices Mesh_Triangles_Centroid             (double width_phi, double width_R, unsigned number_of_vertices)                    const;
    Triangle_Vertices Mesh_Triangles_RMF                  (double width_phi, double width_R, unsigned number_of_vertices)                    const;
    Triangle_Vertices Mesh_Triangles_Frenet               (double width_phi, double width_R, unsigned number_of_vertices)                    const;
    Triangle_Vertices Mesh_Triangles_Rotated_From_Centroid(double width_phi, double width_r, unsigned number_of_vertices, DynamicVector rot) const;
    /**
     * @brief Returns the \f$\phi\f$ coordinate of the centre of the coil
     * 
     * Can be useful for selecting coils for a half module.
     * 
     * @return double 
     */ 
    double Phi() const {auto centre = this->Get_Centre();  double phi = atan2(centre[1], centre[0]); return phi > 0 ? phi : phi + 2 * Constants::pi;}

    // meaningless if it is continuous
    virtual unsigned Number_of_Vertices() const = 0;

    virtual void Scale_Points(double factor);


    virtual std::string Write_str() const = 0;
    protected:
        Vector m_centre = {0.0,0.0,0.0}; // responsibility of constructor to make this meaningful
};

/**
 * @brief Abstract Class for handling stellarator coil geometry
 * 
 * 
 */
class Discrete_Coil : public Coil{
    public: 

        Discrete_Coil(VectorArray vertices);

        /**
         * @brief Write out information about the coil
         * 
         */
        void Write() const override;

        /**
         * @brief Returns number of discrete vertices in Coil
         * 
         * @return unsigned number of discrete vertices in the Coil
         */
        unsigned Number_of_Vertices() const override { return m_vertices.rows();}

            
        VectorArray Return_Sampling_Curve() const override{return m_vertices;};
        void Set_Vertices(const VectorArray& v_in)                       {m_vertices = v_in;};

        Vector Position(Arc_Length arc_length) const override;

        Unit_Vector Tangent(Arc_Length arc_length) const override;

        std::array<Vector, 4> Finite_Size_Frenet(Arc_Length arc_length, double width_phi, double width_R) const override { throw std::invalid_argument("Discrete Coils can not have a Frenet frame; their curvature vanishes in the interpolation between two discrete points...");};
        
        std::array<Vector, 4> Finite_Size_Centroid(Arc_Length arc_length, double width_phi, double width_R) const override;
        
        std::string Write_str() const override{
            return "Discrete_Coil("+std::to_string(m_vertices.rows())+" points)";
        }
	    void Scale_Points( double factor) override;
    private:

        /**
         * @brief Vertices of the coils
         * 
         */
        VectorArray m_vertices;

};

class Fourier_Coil : public Coil{
    public:
        Fourier_Coil(VectorArray xyz_f_cos, VectorArray xyz_f_sin, Vector centre) : m_xyz_f_cos(xyz_f_cos), m_xyz_f_sin(xyz_f_sin){m_centre = centre;};

        void Write() const override{std::cout<<"Fourier coil at "<<this<<'\n';}
        unsigned Number_of_Vertices() const override{return 0;}

        Vector Position(Arc_Length arc_length) const override;

        Unit_Vector Tangent(Arc_Length arc_length) const override;

        std::array<Vector, 4> Finite_Size_Frenet(Arc_Length arc_length, double width_phi, double width_R) const override;
        VectorArray Return_Sampling_Curve() const override{
            unsigned nf = m_xyz_f_cos.rows();             
            unsigned nsamples = 2 * nf + 1;
            VectorArray result(nsamples, 3);
            for(unsigned i =0; i < nsamples; ++i){
                auto pos = this->Position(double(i) / double(nsamples));
                result(i,0) = pos[0];
                result(i,1) = pos[1];
                result(i,2) = pos[2];
            }
            return result;
        };                
        
        void Scale_Points(double factor) override;

        VectorArray  Get_Fourier_Cos() const {return m_xyz_f_cos;}
        void Set_Fourier_Cos(const VectorArray& vin)       {m_xyz_f_cos = vin;}

        VectorArray  Get_Fourier_Sin() const {return m_xyz_f_sin;}
        void Set_Fourier_Sin(const VectorArray& vin)       {m_xyz_f_sin = vin;}

        std::string Write_str() const override{
            return "Fourier_Coil("+std::to_string(m_xyz_f_cos.rows())+" harmonics)";
        }

    private:
        Unit_Vector Normal(Arc_Length arc_length) const;
        VectorArray m_xyz_f_cos;
        VectorArray m_xyz_f_sin;
};


/*
class Harmonic_RMF_Fourier_Coil : public Fourier_Coil{
    public:
        Harmonic_RMF_Fourier_Coil(VectorArray xyz_f_cos, VectorArray xyz_f_sin, Vector centre, VectorArray rmf_f_cos, VectorArray rmf_f_sin, Vector rmf_centre) : Fourier_Coil(xyz_f_cos, xyz_f_sin, centre), m_rmf_f_cos(rmf_f_cos), m_rmf_f_sin(rmf_f_sin){ m_rmf_centre = rmf_centre;}

        void Write() const override{std::cout<<"RMF Fourier coil at "<<this<<'\n';}
        std::array<Vector, 4> Finite_Size_Centroid(Arc_Length arc_length, double width_phi, double width_R) const override;
        

    private:

        VectorArray m_rmf_f_cos;
        VectorArray m_rmf_f_sin;
        Vector m_rmf_centre;
};
*/


class Coil_Set{
    public:
        
        Coil_Set(std::vector<std::shared_ptr<Coil>>& coil_vec) : m_coils(coil_vec) { };

        std::vector<std::shared_ptr<Coil>> m_coils;

        void Truncate_To_Angles(Toroidal_Extent tor_extent);

	    void Scale_Points(double factor);
        
        using iterator = Vector_Iterator<std::shared_ptr<Coil>>;
        iterator begin() const { return iterator(&(*m_coils.begin())); };
        iterator end() const { return iterator(&(*m_coils.end())); };

    private:
       
        
};

Triangle_Vertices Mesh_Triangles_From_Lines(VectorArray& lines);
VectorArray Compute_RMF(const Coil& coil, unsigned no_of_samples);\

DynamicVector Compute_Rotation_Finite_Sizes(VectorArray finite_size_1, VectorArray finite_size_2);
