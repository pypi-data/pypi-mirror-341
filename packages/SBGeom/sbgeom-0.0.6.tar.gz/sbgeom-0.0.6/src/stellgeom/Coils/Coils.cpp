#include "Coils.h"
#include <fstream>
#include "json.h"
#include "Utility.h"
#include "Flux_Surface_Coords.h"

Discrete_Coil::Discrete_Coil(VectorArray vertices) : m_vertices(vertices){
    Vector sum_vertices(0.0,0.0,0.0);
    for(unsigned i = 0; i < m_vertices.rows(); ++i){
        sum_vertices[0] += m_vertices(i,0);
        sum_vertices[1] += m_vertices(i,1);
        sum_vertices[2] += m_vertices(i,2);
    }

    m_centre = sum_vertices / double(m_vertices.rows());
};
void Discrete_Coil::Write() const{
    std::cout<<"Discrete_Coil at "<<this<<" with vertices:\n"<<m_vertices;
};

/*

void Coil_Set::Save_HDF5(std::string filename){
    auto file_id = H5Fcreate(filename.c_str(), H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);
    HDF5_Add_Unsigned_Attribute("Number_of_Coils", file_id, m_coils.size());
    for(unsigned i =0; i< m_coils.size(); ++i){
        auto coil_id = H5Gcreate(file_id, ("/Coil_" +std::to_string(i)).c_str(), H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
        m_coils[i]->Save_HDF5(coil_id);
        H5Gclose(coil_id);
    }
    auto status = H5Fclose(file_id);
};

std::unique_ptr<Coil_Set> Coil_Set::Load_HDF5(std::string hdf5_file){
    auto file_id = H5Fopen(hdf5_file.c_str(), H5F_ACC_RDONLY, H5P_DEFAULT);
    unsigned number_of_coils = HDF5_Load_Unsigned_Attribute(file_id,"Number_of_Coils");
    std::vector<std::shared_ptr<Coil>> resulting_coils;
    for(unsigned i = 0; i < number_of_coils; ++i){
        auto coil_id = H5Gopen(file_id, ("Coil_"+std::to_string(i)).c_str(), H5P_DEFAULT);
        resulting_coils.push_back(Coil::Load_HDF5(coil_id));
        H5Gclose(coil_id);
    }

    auto status = H5Fclose(file_id);

    return std::make_unique<Coil_Set>(resulting_coils);
};*/

/*
std::unique_ptr<Coil> Coil::Load_HDF5(hid_t group_id){
    auto type = HDF5_Load_Unsigned_Attribute(group_id, "Type");
    std::unique_ptr<Coil> result = NULL;
    switch(type){
        case Discrete_Coil_type_H5:
        {
            VectorArray vertices = HDF5_Load_Array(group_id, "Vertices");
            result = std::make_unique<Discrete_Coil>(vertices);
            break;
        }
        case Fourier_Coil_type_H5:
        {
            VectorArray cos_xyz = HDF5_Load_Array(group_id, "Cosine_xyz");
            VectorArray sin_xyz = HDF5_Load_Array(group_id, "Sine_xyz");
            Vector      vec     = HDF5_Load_Array(group_id, "Centre");
            result = std::make_unique<Fourier_Coil>(cos_xyz, sin_xyz, vec);
            break;
        }
        default:
        {
            throw std::runtime_error("Type " + std::to_string(type) + " not recognized in Coil::Load_HDF5..." );
        }
    }

    return result;
}
*/

std::array<Vector, 4> Coil::Finite_Size_Centroid(Arc_Length arc_length, double width_phi, double width_R) const{
   std::array<Vector,4> result;
    auto location      = this->Position(arc_length);

    auto tang_vector   = this->Tangent(arc_length);

    Vector di          = location - this->Get_Centre();    

    auto Ni           =  Unit_Vector(di - tang_vector * di.dot(tang_vector));
    auto e_phi         = Unit_Vector(tang_vector.cross(Ni));
    
    Vector disp_R   = Ni * width_R;
    Vector disp_phi = e_phi * width_phi;
    result[0] = location + disp_R + disp_phi;
    result[1] = location - disp_R + disp_phi;
    result[2] = location + disp_R - disp_phi;
    result[3] = location - disp_R - disp_phi;

    return result;
    
};

std::array<Vector, 4> Coil::Finite_Size_Rotated_From_Centroid(Arc_Length arc_length, double width_phi, double width_R, double angle_tan) const{
    auto result = this->Finite_Size_Centroid(arc_length,width_phi, width_R);
    auto position = this->Position(arc_length);
    Eigen::AngleAxis<double> tanv(angle_tan, this->Tangent(arc_length));
    for(unsigned i =0; i <4; ++i){
        result[i] = tanv* (result[i] - position) + position;
    }
    return result;
};
Vector Discrete_Coil::Position(Arc_Length arc_length) const{
    // Interpolating between two points. But an arc length of 1.0 should be back at the 0 index point I think. 
    // So we multiply by the total number of rows instead of maximum index and then modulo the number of rows.
    // i.e. 100 points, arc length of 1 will be index 100 % 100 = 0 as we want. 
    // We also need to take the modulo of the + 1 index, since this can be too large as well (i.e. point 99 & point "100" index)
    unsigned index      =  unsigned(arc_length.Get_Arc_Length()* double(m_vertices.rows()));
    unsigned index_2    = (index + 1);
    double fraction_top = arc_length.Get_Arc_Length() * double(m_vertices.rows()) - double(index);
    unsigned nrows = m_vertices.rows();
    return Vector(m_vertices(index%nrows,0), m_vertices(index%nrows,1),m_vertices(index%nrows,2)) * (1.0 - fraction_top) + Vector(m_vertices(index_2%nrows,0), m_vertices(index_2%nrows,1),m_vertices(index_2%nrows,2)) * fraction_top;
}



Unit_Vector Discrete_Coil::Tangent(Arc_Length arc_length) const{
    unsigned index      =  unsigned(arc_length.Get_Arc_Length()* double(m_vertices.rows()));
    unsigned index_2    = (index + 1);
    unsigned nrows = m_vertices.rows();
    return Unit_Vector(Vector(m_vertices(index%nrows,0), m_vertices(index%nrows,1),m_vertices(index%nrows,2)) - Vector(m_vertices(index_2%nrows,0), m_vertices(index_2%nrows,1),m_vertices(index_2%nrows,2)));
};

std::array<Vector, 4> Discrete_Coil::Finite_Size_Centroid(Arc_Length arc_length, double width_phi, double width_R) const{
    std::array<Vector,4> result;
    unsigned index      =  unsigned(arc_length.Get_Arc_Length()* double(m_vertices.rows()));
    unsigned index_2    = (index + 1);
    double fraction_top = arc_length.Get_Arc_Length() * double(m_vertices.rows()) - double(index);
    unsigned nrows = m_vertices.rows();

    auto fsize_0 = Coil::Finite_Size_Centroid(double(index%nrows)/ double(m_vertices.rows()),width_phi, width_R);
    auto fsize_1 =  Coil::Finite_Size_Centroid(double(index_2%nrows)/ double(m_vertices.rows()),width_phi, width_R);

    for(unsigned i=0; i < 4; ++i){
        result[i] = fsize_0[i] * (1.0 - fraction_top) + fsize_1[i] * fraction_top;
    }
    return result;
};


/*
void Discrete_Coil::Save_HDF5(hid_t group_id) const{
    HDF5_Add_Unsigned_Attribute("Type", group_id, Discrete_Coil_type_H5);
    HDF5_Store_Array(m_vertices, group_id, "Vertices");

};
void Fourier_Coil::Save_HDF5(hid_t group_id) const{
    HDF5_Add_Unsigned_Attribute("Type", group_id, Fourier_Coil_type_H5);
    HDF5_Store_Array(m_xyz_f_cos, group_id, "Cosine_xyz");
    HDF5_Store_Array(m_xyz_f_sin, group_id, "Sine_xyz");
    HDF5_Store_Array(m_centre, group_id, "Centre");

};
*/
/*
std::array<Vector, 4> Harmonic_RMF_Fourier_Coil::Finite_Size_Centroid(Arc_Length arc_length, double width_phi, double width_R) const{
    std::array<Vector,4> result;
    auto location      = this->Position(arc_length);

    auto tang_vector   = this->Tangent(arc_length);

    Vector r = m_rmf_centre;
    double tv = arc_length.Get_Arc_Length() * 2 * Constants::pi;
        
    // fourier coefficient starts with $n=1$
    for(unsigned i_f = 1 ; i_f < m_rmf_f_cos.rows() + 1; ++i_f){
        double i_fd = double(i_f);
        r[0] += m_rmf_f_cos(i_f - 1, 0) * cos(i_fd  * tv) + m_rmf_f_sin(i_f - 1, 0) * sin(i_fd * tv);
        r[1] += m_rmf_f_cos(i_f - 1, 1) * cos(i_fd  * tv) + m_rmf_f_sin(i_f - 1, 1) * sin(i_fd * tv);
        r[2] += m_rmf_f_cos(i_f - 1, 2) * cos(i_fd  * tv) + m_rmf_f_sin(i_f - 1, 2) * sin(i_fd * tv);
    }
    
    auto Ni           =  Unit_Vector(r);
    auto e_phi         = Unit_Vector(tang_vector.cross(Ni));
    
    Vector disp_R   = Ni * width_R;
    Vector disp_phi = e_phi * width_phi;
    result[0] = location + disp_R + disp_phi;
    result[1] = location - disp_R + disp_phi;
    result[2] = location + disp_R - disp_phi;
    result[3] = location - disp_R - disp_phi;

    return result;
    
};*/

Triangle_Vertices Mesh_Triangles_From_Lines(VectorArray& lines){

    auto result = Triangle_Vertices();

    auto N_vertices = lines.rows() / 4; 

    for(unsigned i_v = 0; i_v < N_vertices; ++i_v){
        
            for(unsigned i_f_v = 0; i_f_v < 4; ++i_f_v){
                result.nodes.push_back(std::make_unique<Node>(lines.row(i_f_v * N_vertices + i_v)));            
            }
       }

       // 8 triangles per coil poloidal block, each triangle 3 indices
    auto indices    = Contiguous3D<unsigned>(N_vertices, 8 , 3 ); 

    auto vertex_number= [](unsigned i_block, unsigned finite_size_i){
                   return 4 * i_block +  finite_size_i;
    };
       
    for(unsigned i_v_b = 0; i_v_b < N_vertices; ++i_v_b){
              unsigned i_v_b0 = i_v_b;
              unsigned i_v_b1 = (i_v_b + 1) % N_vertices;

              result.vertices.push_back({vertex_number(i_v_b1, 0), vertex_number(i_v_b0, 0), vertex_number(i_v_b0, 1)});

              result.vertices.push_back({vertex_number(i_v_b1, 0), vertex_number(i_v_b0, 1), vertex_number(i_v_b1, 1)});

              result.vertices.push_back({vertex_number(i_v_b0, 2), vertex_number(i_v_b0, 0),  vertex_number(i_v_b1, 0)});

              result.vertices.push_back({vertex_number(i_v_b1, 2), vertex_number(i_v_b0, 2), vertex_number(i_v_b1, 0)});

              result.vertices.push_back({vertex_number(i_v_b0, 1), vertex_number(i_v_b0, 3), vertex_number(i_v_b1, 1)});

              result.vertices.push_back({vertex_number(i_v_b1, 1), vertex_number(i_v_b0, 3), vertex_number(i_v_b1, 3)});

              result.vertices.push_back({vertex_number(i_v_b0, 3), vertex_number(i_v_b0, 2), vertex_number(i_v_b1, 3)});
              
              result.vertices.push_back({vertex_number(i_v_b0, 2), vertex_number(i_v_b1, 2), vertex_number(i_v_b1, 3)});

       }
    
    return result;    
}

VectorArray  Coil::Finite_Size_Lines_Centroid(unsigned no_of_points, double width_phi, double width_R)const{
    auto result = VectorArray(4 * no_of_points, 3).setZero();
    auto t = Eigen::ArrayXd::LinSpaced(no_of_points + 1, 0.0, 1.0); // avoiding endpoint
    for(unsigned i = 0; i < no_of_points; ++i){
        
        auto finite_size = this->Finite_Size_Centroid(Arc_Length(t[i]), width_phi, width_R);
        result.row(i + 0 * no_of_points) = finite_size[0];
        result.row(i + 1 * no_of_points) = finite_size[1];
        result.row(i + 2 * no_of_points) = finite_size[2];
        result.row(i + 3 * no_of_points) = finite_size[3];
    }
    return result;
};

VectorArray  Coil::Finite_Size_Lines_Rotated_From_Centroid(unsigned no_of_points, double width_phi, double width_R, DynamicVector rot)const{
    auto result = VectorArray(4 * no_of_points, 3).setZero();
    auto t = Eigen::ArrayXd::LinSpaced(no_of_points + 1, 0.0, 1.0); // avoiding endpoint
    if(rot.rows() != no_of_points){
        throw std::invalid_argument("Rotation vector does not have the same dimension ("+std::to_string(rot.rows())+") as the number of points (" + std::to_string(no_of_points)+")");
    }
    for(unsigned i = 0; i < no_of_points; ++i){
        
        auto finite_size = this->Finite_Size_Rotated_From_Centroid(Arc_Length(t[i]), width_phi, width_R, rot[i]);
        result.row(i + 0 * no_of_points) = finite_size[0];
        result.row(i + 1 * no_of_points) = finite_size[1];
        result.row(i + 2 * no_of_points) = finite_size[2];
        result.row(i + 3 * no_of_points) = finite_size[3];
    }
    return result;
};

VectorArray  Coil::Finite_Size_Lines_Frenet(unsigned no_of_points, double width_phi, double width_R)const{
    auto result = VectorArray(4 * no_of_points, 3).setZero();
    auto t = Eigen::ArrayXd::LinSpaced(no_of_points + 1, 0.0, 1.0); // avoiding endpoint
    for(unsigned i = 0; i < no_of_points; ++i){
        
        auto finite_size = this->Finite_Size_Frenet(Arc_Length(t[i]), width_phi, width_R);
        result.row(i + 0 * no_of_points) = finite_size[0];
        result.row(i + 1 * no_of_points) = finite_size[1];
        result.row(i + 2 * no_of_points) = finite_size[2];
        result.row(i + 3 * no_of_points) = finite_size[3];
    }
    return result;
};

VectorArray  Coil::Finite_Size_Lines_RMF(unsigned no_of_points, double width_phi, double width_R)const{
    auto result = VectorArray(4 * no_of_points, 3).setZero();
    
    auto r_rmf = Compute_RMF(*this, no_of_points);

    auto t = Eigen::ArrayXd::LinSpaced(no_of_points + 1, 0.0, 1.0); // avoiding endpoint

    for(unsigned i = 0; i < no_of_points; ++i){
        
        auto ri= Vector(r_rmf.row(i));
        auto pos = this->Position(t[i]);
        auto ti = Unit_Vector(this->Tangent(t[i]));
        auto si = Unit_Vector(ti.cross(ri));

        Vector disp_R   = si * width_R; // they are different here: the base r vector is tang x centroid = phi;
        Vector disp_phi = ri * width_phi;
        result.row(i + 0 * no_of_points) = pos + disp_R + disp_phi;
        result.row(i + 1 * no_of_points) = pos - disp_R + disp_phi;
        result.row(i + 2 * no_of_points) = pos + disp_R - disp_phi;
        result.row(i + 3 * no_of_points) = pos - disp_R - disp_phi;
    }
    return result;
};

Triangle_Vertices Coil::Mesh_Triangles_Centroid(double width_phi, double width_R, unsigned number_of_vertices)const{    
    auto lines = this->Finite_Size_Lines_Centroid(number_of_vertices, width_phi, width_R);
    return Mesh_Triangles_From_Lines(lines);
};
Triangle_Vertices Coil::Mesh_Triangles_RMF(double width_phi, double width_R, unsigned number_of_vertices)const{
    auto lines = this->Finite_Size_Lines_RMF(number_of_vertices, width_phi, width_R);
    return Mesh_Triangles_From_Lines(lines);
};
Triangle_Vertices Coil::Mesh_Triangles_Frenet(double width_phi, double width_R, unsigned number_of_vertices)const{
    auto lines = this->Finite_Size_Lines_Frenet(number_of_vertices, width_phi, width_R);
    return Mesh_Triangles_From_Lines(lines);
};

Triangle_Vertices Coil::Mesh_Triangles_Rotated_From_Centroid(double width_phi, double width_R, unsigned number_of_vertices, DynamicVector rot)const{
    auto lines = this->Finite_Size_Lines_Rotated_From_Centroid(number_of_vertices, width_phi, width_R, rot);
    return Mesh_Triangles_From_Lines(lines);
};

Vector Fourier_Coil::Position(Arc_Length arc_length) const{
    double tv = arc_length.Get_Arc_Length() * 2 * Constants::pi;
    Vector result = m_centre;
    // fourier coefficient starts with $n=1$
    for(unsigned i_f = 1 ; i_f < m_xyz_f_cos.rows() + 1; ++i_f){
        double i_fd = double(i_f);
        result[0] += m_xyz_f_cos(i_f - 1, 0) * cos(i_fd  * tv) + m_xyz_f_sin(i_f - 1, 0) * sin(i_fd * tv);
        result[1] += m_xyz_f_cos(i_f - 1, 1) * cos(i_fd  * tv) + m_xyz_f_sin(i_f - 1, 1) * sin(i_fd * tv);
        result[2] += m_xyz_f_cos(i_f - 1, 2) * cos(i_fd  * tv) + m_xyz_f_sin(i_f - 1, 2) * sin(i_fd * tv);
    }
    return result;
    
};
Unit_Vector Fourier_Coil::Tangent(Arc_Length arc_length) const{
    double tv = arc_length.Get_Arc_Length() * 2 * Constants::pi;

    Vector result(0.0,0.0,0.0);
    // fourier coefficient starts with $n=1$
    for(unsigned i_f = 1 ; i_f < m_xyz_f_cos.rows() + 1; ++i_f){
        double i_fd = double(i_f);
        result[0] += - m_xyz_f_cos(i_f - 1, 0) * i_fd * sin(i_fd  * tv) + m_xyz_f_sin(i_f - 1, 0) * i_fd * cos(i_fd * tv);
        result[1] += - m_xyz_f_cos(i_f - 1, 1) * i_fd * sin(i_fd  * tv) + m_xyz_f_sin(i_f - 1, 1) * i_fd * cos(i_fd * tv);
        result[2] += - m_xyz_f_cos(i_f - 1, 2) * i_fd * sin(i_fd  * tv) + m_xyz_f_sin(i_f - 1, 2) * i_fd * cos(i_fd * tv);
    }

    return Unit_Vector(result);
}

Unit_Vector Fourier_Coil::Normal(Arc_Length arc_length)const{
    double tv = arc_length.Get_Arc_Length() * 2 * Constants::pi;

    Vector result(0.0,0.0,0.0);
    // fourier coefficient starts with $n=1$
    for(unsigned i_f = 1 ; i_f < m_xyz_f_cos.rows() + 1; ++i_f){
        double i_fd = double(i_f);
        result[0] += - m_xyz_f_cos(i_f - 1, 0) * pow(i_fd,2) * cos(i_fd  * tv) - m_xyz_f_sin(i_f - 1, 0) * pow(i_fd,2) * sin(i_fd * tv);
        result[1] += - m_xyz_f_cos(i_f - 1, 1) * pow(i_fd,2) * cos(i_fd  * tv) - m_xyz_f_sin(i_f - 1, 1) * pow(i_fd,2) * sin(i_fd * tv);
        result[2] += - m_xyz_f_cos(i_f - 1, 2) * pow(i_fd,2) * cos(i_fd  * tv) - m_xyz_f_sin(i_f - 1, 2) * pow(i_fd,2) * sin(i_fd * tv);
    }

    return Unit_Vector(result);
};

std::array<Vector, 4> Fourier_Coil::Finite_Size_Frenet(Arc_Length arc_length, double width_phi, double width_R) const{
    std::array<Vector,4> result;
    auto tang   = this->Tangent(arc_length);
    auto norm   = this->Normal(arc_length);
    auto location=this->Position(arc_length);
    auto binorm = Unit_Vector(tang.cross(norm));
    
    Vector disp_R   = norm * width_R;
    Vector disp_phi = binorm * width_phi;
    result[0] = location + disp_R + disp_phi;
    result[1] = location - disp_R + disp_phi;
    result[2] = location + disp_R - disp_phi;
    result[3] = location - disp_R - disp_phi;

    return result;
    
};

void Coil_Set::Truncate_To_Angles(Toroidal_Extent tor_extent){
    std::vector<std::shared_ptr<Coil>> coils_trunc;
    for(auto coil : m_coils){
        auto phi_c = atan2(coil->Get_Centre()[1],coil->Get_Centre()[0]);
        auto end = tor_extent.max() - tor_extent.min() < 0.0 ? tor_extent.max() - tor_extent.min() + 2 * Constants::pi : tor_extent.max() - tor_extent.min();
        auto mid = phi_c - tor_extent.min() < 0.0 ? phi_c - tor_extent.min() + 2 * Constants::pi : phi_c - tor_extent.min();
        if(mid < end){
            coils_trunc.push_back(coil);
        }
    }
    m_coils = coils_trunc;;
};

VectorArray Compute_RMF(const Coil& coil, unsigned no_of_samples){
    auto result = VectorArray(no_of_samples,3).setZero();

    auto tan_arr = VectorArray(no_of_samples,3).setZero();
    auto pos_arr = VectorArray(no_of_samples,3).setZero();
    
    auto rL         =  VectorArray(no_of_samples,3).setZero();
    auto tL         =  VectorArray(no_of_samples,3).setZero();
    
    
    
    auto t          = Eigen::ArrayXd::LinSpaced(no_of_samples  + 1, 0.0, 1.0); // don't include endpoint...
    for(unsigned i = 0; i < no_of_samples; ++i){
        pos_arr.row(i) = coil.Position(Arc_Length(t[i]));
        tan_arr.row(i) = Unit_Vector(coil.Tangent(Arc_Length(t[i])));
    }

    result.row(0)   = Unit_Vector(tan_arr.row(0)).cross(Unit_Vector(Vector(pos_arr.row(0)) - coil.Get_Centre()));

    for(unsigned i =0; i < no_of_samples - 1; ++i){
        Vector v1 = pos_arr.row(i + 1) - pos_arr.row(i);
        double c1 = v1.dot(v1);

        rL.row(i) = Vector(result.row(i))  - 2.0 / c1 * v1.dot(Vector(result.row(i))) * v1;
        tL.row(i) = Vector(tan_arr.row(i)) - 2.0 / c1 * v1.dot(Vector(tan_arr.row(i))) * v1;

        Vector v2 = tan_arr.row(i+1) - tL.row(i);

        double c2 = v2.dot(v2);

        result.row(i+1) = Vector(rL.row(i))  - 2.0 / c2 * v2.dot(Vector(rL.row(i))) * v2;
        
    }
    // Periodic correction:

    Unit_Vector rlast(result.row(no_of_samples - 1));
    Unit_Vector rfirst(result.row(0));

    double angle =acos(rlast.dot(rfirst));
    
    
    Eigen::AngleAxis<double> tanv0(angle, Vector(tan_arr.row(tan_arr.rows() - 1)));

    if(acos(rfirst.dot(tanv0 * rlast) )> angle ){
        angle = - angle;
    }
    auto uniform_rot = Eigen::ArrayXd::LinSpaced(no_of_samples, 0.0,angle);
    for(unsigned i = 0; i < no_of_samples; ++i){
        Eigen::AngleAxis<double> tanv(uniform_rot[i], Vector(tan_arr.row(i)));
       
        result.row(i) = tanv * Vector(result.row(i));
    }
    
    Unit_Vector rlast2(result.row(no_of_samples - 1));
    Unit_Vector rfirst2(result.row(0));

    double angle2 =acos(rlast2.dot(rfirst2));

    return result;
};

DynamicVector Compute_Rotation_Finite_Sizes(VectorArray finite_size_1, VectorArray finite_size_2){
    // we assume here that all finite size vectors are orthogonal to the tangent vector. In all cases considered in the above code, this is the case..
    if(finite_size_1.rows() != finite_size_2.rows()){
        throw std::invalid_argument("Not the same sampled finite sizes");
    }
    
    unsigned no_points = finite_size_1.rows() /4; // other lines have same rotation 

    DynamicVector result(no_points);

    for(unsigned i =0; i < no_points; ++i){
        
        Vector position = Vector(finite_size_1.row(i)  + finite_size_1.row(i+ 1 * no_points) + finite_size_1.row(i+ 2 * no_points) + finite_size_1.row(i + 3 * no_points)) / 4.0;
        result[i] = acos(Unit_Vector(Vector(finite_size_1.row(i)) - position).dot(Unit_Vector(Vector(finite_size_2.row(i)) - position)));
    }
    return result;
};

/* Generic functions required for HeliasGeom */
void Coil::Scale_Points( double factor){
   m_centre   = m_centre * factor;
}
void Discrete_Coil::Scale_Points( double factor){
   Coil::Scale_Points(factor);
   m_vertices = m_vertices * factor;
}

void Fourier_Coil::Scale_Points(double factor){
    Coil::Scale_Points(factor);
    m_xyz_f_cos = m_xyz_f_cos * factor;
    m_xyz_f_sin = m_xyz_f_sin * factor;
};

void Coil_Set::Scale_Points(double factor){
   /* For each coil in coil set, scale factor */
   for (auto& coil : m_coils){
     coil->Scale_Points(factor);
   }
}

