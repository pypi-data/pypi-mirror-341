#include "Flux_Surfaces.h"
  
#include "Matrix.h"
#include <math.h>
#include "Constants.h"

#include "Utility.h"
#include "Flux_Surface_Node.h"
#include "Flux_Surfaces_Extended.h"
#include "Conversion_Tools.h"
#include "json_utility.h"


Flux_Surfaces::~Flux_Surfaces(){};

/*
Flux_Surfaces::Flux_Surfaces(std::string filename_VMEC_NC4) : m_Rmnc(1,1), m_Zmns(1,1){
    // These are highly unsafe. They are not checked for type or existence so you might get garbage.
    auto read_0d_unsigned = [](std::string name, hid_t file_id){
        auto dataset_id = H5Dopen(file_id, name.c_str(), H5P_DEFAULT);
            auto dataspace_id = H5Dget_space(dataset_id); 
                unsigned result = 0;
                
                auto ndims     =  H5Sget_simple_extent_ndims(dataspace_id);
                if ( ndims > 0){throw std::invalid_argument(name + " is not a 0D dataset.");}
                auto type      =  H5Dget_type(dataset_id);
                H5Dread(dataset_id,type, H5S_ALL, H5S_ALL, H5P_DEFAULT,&result);
            auto status = H5Sclose(dataspace_id);
            status = H5Dclose(dataset_id);
        return result;
    };

    try{
        auto file_id = H5Fopen(filename_VMEC_NC4.c_str(),H5F_ACC_RDONLY,H5P_DEFAULT);
        if(file_id == H5I_INVALID_HID){throw std::invalid_argument("Cannot find" + filename_VMEC_NC4);}
        
        m_Rmnc = HDF5_Load_Array(file_id,"rmnc");
        m_Zmns = HDF5_Load_Array(file_id,"zmns");

        m_ntor_vector = HDF5_Load_Array(file_id, "xn");
        m_mpol_vector = HDF5_Load_Array(file_id, "xm");

        m_settings = Flux_Surface_Settings();
        m_settings.m_pol = read_0d_unsigned("mpol", file_id);
        m_settings.n_tor = read_0d_unsigned("ntor",file_id);
        m_settings.number_of_surfaces = read_0d_unsigned("ns", file_id);
        m_settings.symmetry = unsigned(m_ntor_vector[1]);

        auto status    = H5Fclose(file_id);
        this->Set_du_x_dv_sign();

    }
    catch(const std::exception& e){
        std::cout<<e.what()<<" in Flux_Surfaces(filename_VMEC_NC4). Aborting..."<<std::endl;
        abort();
    }
    



};

*/

void Flux_Surfaces::Set_Data_Members(const Flux_Surface_Settings& flux_surface_settings, const Array& Rmnc, const Array& Zmns){

    m_settings = flux_surface_settings;
    m_Rmnc     = Rmnc;
    m_Zmns     = Zmns;
    
    unsigned numbers_per_surface = (2*m_settings.n_tor)*m_settings.m_pol + m_settings.m_pol - m_settings.n_tor;

    m_ntor_vector = DynamicVector(numbers_per_surface);
    m_mpol_vector = DynamicVector(numbers_per_surface);

    if(numbers_per_surface != m_Rmnc.cols()){throw std::runtime_error("The numbers per surface are not equal to 2 * ntor * mpol + mpol - ntor. Unexpected shape.");}
    
    int ntor = m_settings.n_tor;
    int mpol = m_settings.m_pol;
    int symm = m_settings.symmetry;
    for(int i = 0; i < numbers_per_surface; i++){
        if(i < ( ntor + 1) ){
            m_mpol_vector[i] = 0.0;
        }
        else{
            m_mpol_vector[i] =  double( (i - (ntor + 1) ) / (2 * ntor + 1) + 1 ) ; //VMEC convention
        }
        int iteration = i % (2*ntor+1);
        if(iteration < (ntor+1) ){
            m_ntor_vector[i] =  double(iteration * symm);
        }
        else{
            m_ntor_vector[i] = double((iteration - (2 * ntor + 1) ) * symm); 
        }
    }
    
    this->Set_du_x_dv_sign();
};

Vector Flux_Surfaces::Return_Position(const Flux_Surface_Coordinates& flux_surface_coordinates) const{

    double s = flux_surface_coordinates.Get_s();
    double d = flux_surface_coordinates.Get_distance_LCFS();
    double u = flux_surface_coordinates.u;
    double v = flux_surface_coordinates.v;

    
    double R_i = 0.0;
    double Z_i = 0.0;
    double phi = v;
    
    double x = 0.0;
    double y = 0.0;
    double z = 0.0;
    
    
    for(unsigned i = 0; i < m_Rmnc.cols(); ++i){
        double ntor_i = m_ntor_vector[i];
        double mpol_i = m_mpol_vector[i];
        R_i += this->Get_Rmnc_Interp(s,i) * cos(u * mpol_i - v * ntor_i); 
        Z_i += this->Get_Zmns_Interp(s,i) * sin(u * mpol_i - v * ntor_i); 
    }
    x = R_i * cos(v);
    y = R_i * sin(v);
    z = Z_i;
    if(fabs(d) > 0.0){ throw std::invalid_argument("Trying to have a distance from the LCFS with the base Flux_Surfaces class.");}
    return Vector(x,y,z);
    
}

Vector Flux_Surfaces::Return_Position_Index(size_t index, double u, double v) const{
    double R_i = 0;
    double Z_i = 0;
    for(unsigned i = 0; i < m_Rmnc.cols(); ++i){
        double ntor_i = m_ntor_vector[i];
        double mpol_i = m_mpol_vector[i];
        R_i += m_Rmnc(index, i) * cos(u * mpol_i - v * ntor_i); 
        Z_i += m_Zmns(index, i) * sin(u * mpol_i - v * ntor_i); 
    }
    double x = R_i * cos(v);
    double y = R_i * sin(v);
    double z = Z_i;    
    return Vector(x,y,z);
};
Vector      Flux_Surfaces::Return_Axis_Position(double v) const{
    return this->Return_Position(Flux_Surface_Coordinates(Radial_Flux_Coordinate(0.0,0.0),0.0,v));
}
Unit_Vector Flux_Surfaces::Return_Surface_Normal(const Flux_Surface_Coordinates& flux_surface_coordinates) const{
    Vector normal;

    double s = flux_surface_coordinates.Get_s();
    double d = flux_surface_coordinates.Get_distance_LCFS();
    double u = flux_surface_coordinates.u;
    double v = flux_surface_coordinates.v;
    if( d > 0.0){throw std::invalid_argument("Cannot generate a surface normal beyond the LCFS in Flux_Surfaces::Return_Surface_Normal.");}

    double dR_du = 0.0;
    double dR_dv = 0.0;
    double dz_du = 0.0;
    double dz_dv = 0.0;
    double R     = 0.0;
    double z     = 0.0;
    double phi   = v;

    
    for(unsigned i = 0 ; i< m_Rmnc.cols(); ++i){
        double ntor_i = m_ntor_vector[i];
        double mpol_i = m_mpol_vector[i];
        R     +=            this->Get_Rmnc_Interp(s, i) * cos(u * mpol_i - v * ntor_i); 
        z     +=            this->Get_Zmns_Interp(s, i) * sin(u * mpol_i - v * ntor_i); 
        dR_du += - mpol_i * this->Get_Rmnc_Interp(s, i) * sin(u * mpol_i - v * ntor_i);
        dR_dv += + ntor_i * this->Get_Rmnc_Interp(s, i) * sin(u * mpol_i - v * ntor_i);
        dz_du += + mpol_i * this->Get_Zmns_Interp(s, i) * cos(u * mpol_i - v * ntor_i);
        dz_dv += - ntor_i * this->Get_Zmns_Interp(s, i) * cos(u * mpol_i - v * ntor_i);
    }
    Vector dr_du;

    dr_du[0] = dR_du * cos(v);
    dr_du[1] = dR_du * sin(v);
    dr_du[2] = dz_du;

    Vector dr_dv;

    dr_dv[0] = dR_dv * cos(v) - R * sin(v);
    dr_dv[1] = dR_dv * sin(v) + R * cos(v);
    dr_dv[2] = dz_dv;

    Unit_Vector result(dr_du.cross(dr_dv));


    return Unit_Vector( result * m_du_x_dv_sign);
}

void Flux_Surfaces::Set_du_x_dv_sign(){
    unsigned sampling_normals = 20;
    int      outward_distance = 0;
    for(unsigned i =0; i < sampling_normals; ++i){
        
        auto coords   = Coordinates_From_Discrete_Angles(Radial_Flux_Coordinate(1.0,0.0),i, 0,sampling_normals, 10,Half_Module(m_settings,0.0));
        auto pos_lcfs = this->Return_Position(coords);
        auto pos_d    = this->Return_Position(coords) + this->Return_Surface_Normal(coords) * 0.05;
        auto pos_axis = this->Return_Axis_Position(coords.v);

        outward_distance += (pos_d - pos_axis).norm() > (pos_lcfs - pos_axis).norm() ? 1 : -1;
       
    }
    m_du_x_dv_sign = outward_distance  > 0 ? 1.0 : -1.0;
};


UV_Manifold Flux_Surfaces::Return_UV_Manifold(Radial_Flux_Coordinate r, unsigned N_u, unsigned N_v) const{
    return this->Return_UV_Manifold(r,N_u,N_v, Toroidal_Extent(0.0, 2* Constants::pi));
};

UV_Manifold Flux_Surfaces::Return_UV_Manifold(Radial_Flux_Coordinate r, unsigned N_u, unsigned N_v, const Toroidal_Extent& toroidal_extent) const{
    double u = 0;
    double v = 0;
    

   sb_assert(N_u > 0 && N_v > 0);

    Contiguous3D<double> data(N_u, N_v, 3);

    for(unsigned u_i = 0 ; u_i < N_u; ++u_i){

        
        for(unsigned v_i= 0 ; v_i < N_v; ++v_i){
            auto position = this->Return_Position(Coordinates_From_Discrete_Angles(r,u_i, v_i, N_u, N_v, toroidal_extent));
            data(u_i, v_i, 0) = position[0];
            data(u_i, v_i, 1) = position[1];
            data(u_i, v_i, 2) = position[2];
        }
    }
    return UV_Manifold(std::move(data),r,toroidal_extent);
};
V_Axis      Flux_Surfaces::Return_V_Axis(unsigned N_v) const{return this->Return_V_Axis(N_v, Toroidal_Extent(0.0, 2* Constants::pi));};
V_Axis      Flux_Surfaces::Return_V_Axis(unsigned N_v, const Toroidal_Extent& toroidal_extent) const{
    Array data(N_v,3);
   sb_assert(N_v > 0);
    for(unsigned v_i = 0; v_i < N_v; ++v_i){
        auto position     = this->Return_Position(Coordinates_From_Discrete_Angles_Axis(v_i, N_v, toroidal_extent));
        
        data(v_i, 0) = position[0];
        data(v_i, 1) = position[1];
        data(v_i, 2) = position[2];
    }
    return V_Axis(std::move(data), toroidal_extent);

};


    
    
/*

void Flux_Surfaces::Save_HDF5(hid_t location_id) const{
    auto flux_surfaces_id = H5Gcreate(location_id, "Flux_Surfaces", H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);

    HDF5_Store_Array(m_Rmnc, flux_surfaces_id, "Rmnc" );
    HDF5_Store_Array(m_Zmns, flux_surfaces_id, "Zmns" );
    
    HDF5_Add_Unsigned_Attribute("Number_Of_Surfaces",flux_surfaces_id, m_settings.number_of_surfaces );
    HDF5_Add_Unsigned_Attribute("n_tor",flux_surfaces_id, m_settings.n_tor );
    HDF5_Add_Unsigned_Attribute("m_pol",flux_surfaces_id, m_settings.m_pol );
    HDF5_Add_Unsigned_Attribute("Symmetry",flux_surfaces_id, m_settings.symmetry);
    auto status      = H5Gclose(flux_surfaces_id);
};

std::unique_ptr<Flux_Surfaces> Flux_Surfaces::Load_HDF5(hid_t flux_surface_hid) {
    std::unique_ptr<Flux_Surfaces> result  = NULL;
    auto extension_type = HDF5_Load_Unsigned_Attribute(flux_surface_hid, "Extension");
    
    auto Rmnc   = HDF5_Load_Array(flux_surface_hid, "Rmnc");
    auto Zmns   = HDF5_Load_Array(flux_surface_hid, "Zmns");
    
    Flux_Surface_Settings settings;

    settings.m_pol              = HDF5_Load_Unsigned_Attribute(flux_surface_hid, "m_pol");
    settings.n_tor              = HDF5_Load_Unsigned_Attribute(flux_surface_hid, "n_tor");
    settings.symmetry           = HDF5_Load_Unsigned_Attribute(flux_surface_hid, "Symmetry");
    settings.number_of_surfaces = HDF5_Load_Unsigned_Attribute(flux_surface_hid, "Number_Of_Surfaces");
    

    if(extension_type == Flux_Surfaces_Normal_Extended_type_H5){
        result = std::make_unique<Flux_Surfaces_Normal_Extended>(std::move(Rmnc), std::move(Zmns), settings);
    }
    else if(extension_type == Flux_Surfaces_Fourier_Extended_type_H5){
        result = std::make_unique<Flux_Surfaces_Fourier_Extended>(std::move(Rmnc), std::move(Zmns), settings, flux_surface_hid);
    }
    else{
        throw std::invalid_argument("Type " + std::to_string(extension_type) + " not recognized in Flux_Surfaces::Load_HDF5");
    }
    return result;    
};

std::unique_ptr<Flux_Surfaces> Flux_Surfaces::Load_VMEC_NetCDF4(std::string filename_VMEC_NC4, const json& extension_json){
    std::unique_ptr<Flux_Surfaces> result = NULL;
    if      (extension_json.at("Type") == "Normal_Vector"){
        result = std::make_unique<Flux_Surfaces_Normal_Extended>(filename_VMEC_NC4);
    }
    else if ( extension_json.at("Type") == "Fourier"){
        result = std::make_unique<Flux_Surfaces_Fourier_Extended>(filename_VMEC_NC4, extension_json);
    }
    else{
        throw std::invalid_argument("Type " + extension_json.get<std::string>() + " not recognized in Flux_Surfaces::Load_VMEC_NetCDF4");
    }
    return result;
};
*/

// std::unique_ptr<Flux_Surfaces> Flux_Surfaces::Construct_Flux_Surface(const json& json_in){

//     std::unique_ptr<Flux_Surfaces> result = NULL;
//     try{
        
//         const auto& json_flux = json_in.at("Flux_Surfaces");
        
//         if(json_flux.at("Type") == "HDF5"){
            
//             auto filename = json_flux.at("Filenames").at("Filename_H5").get<std::string>();

//             auto fs_file_id = H5Fopen(filename.c_str(), H5F_ACC_RDONLY,H5P_DEFAULT);
//                 if( fs_file_id == H5I_INVALID_HID){throw std::invalid_argument(" Cannot find the HDF5 file specificed by " + filename);}
                
//                 auto domain_group_id = H5Gopen(fs_file_id, "Domain", H5P_DEFAULT);
//                     if(domain_group_id == H5I_INVALID_HID){throw std::invalid_argument(" Cannot find Domain in the HDF5 file specified by " + filename);}
                    
//                     auto fs_group_id    = H5Gopen(domain_group_id, "Flux_Surfaces", H5P_DEFAULT);                        
//                         if(fs_group_id == H5I_INVALID_HID){throw std::invalid_argument(" Cannot find Flux_Surfaces in the HDF5 file specified by " + filename);}                            
//                             result = Flux_Surfaces::Load_HDF5(fs_group_id);                                                                            
//                     auto status         = H5Gclose(fs_group_id);

//                 status              = H5Gclose(domain_group_id) ;

//             status         = H5Fclose(fs_file_id);

//         }
//         else if(json_flux.at("Type") == "netCDF4"){
//             result = Flux_Surfaces::Load_VMEC_NetCDF4(json_flux.at("Filenames").at("Filename_netCDF4").get<std::string>(), json_flux.at("Extension"));
//         }
//         else{
//             throw std::invalid_argument(" Type " + json_flux.at("Type").get<std::string>()+" not recognized");
//         }
//     }
//     catch(const std::exception& e){
//         std::cout<<e.what()<<" in Flux_Surfaces::Flux_Surfaces(const json& json_in), aborting..."<<std::endl;
//         abort();
//     }

//     return result;
// }


Triangle_Vertices Mesh_Closed_Flux_Surface(const Flux_Surfaces& flux_surface, std::array<Radial_Flux_Coordinate, 2> r_vector, unsigned N_u, unsigned N_v, const Toroidal_Extent& toroidal_extent){
    
    unsigned total_points = 0;
    
    bool includes_axis = false;
    Radial_Flux_Coordinate r_min(0.0,0.0);
    Radial_Flux_Coordinate r_max(0.0,0.0);
    
    
    r_min = r_vector[0];
    r_max = r_vector[1];
    if(r_min.Get_s() == 0.0){ includes_axis = true;}

    std::vector<Radial_Flux_Coordinate> r_in_between;

    double d_s = r_max.Get_s() - r_min.Get_s();
    double d_d = r_max.Get_distance_LCFS() - r_min.Get_distance_LCFS();

    if(d_s  < 0.0 || d_d < 0.0){throw std::invalid_argument("Wrongly ordered Flux Surfaces for Mesh_Closed_Flux_Surface.... Aborting...");}
    
    unsigned n_s_disc = d_s > 0.0 ? 10 : 0;
    unsigned n_d_disc = d_d > 0.0 ? 5  : 0;

    // This goes up to LCFS, so the d discretisation should not include that 
    for(unsigned s_i = 0; s_i < n_s_disc; ++s_i ){
        r_in_between.push_back(Radial_Flux_Coordinate(r_min.Get_s() + (r_max.Get_s()  - r_min.Get_s()) * double(s_i) / double(n_s_disc - 1) , 0.0));
    }
    unsigned d_start =  r_in_between.size() > 0  ? 1 : 0;
    for(unsigned d_i = d_start; d_i < n_d_disc; ++d_i){
        r_in_between.push_back(Radial_Flux_Coordinate(1.0, r_min.Get_distance_LCFS() + (r_max.Get_distance_LCFS() - r_min.Set_distance_LCFS() ) * double(d_i) / double(n_d_disc - 1) ));
    }
    
    auto v_axis = flux_surface.Return_V_Axis(N_v, toroidal_extent);

    auto triangle_vector = std::vector<Triangle_Vertices>();

    if(! includes_axis){        
        triangle_vector.push_back(flux_surface.Return_UV_Manifold(r_in_between[0],N_u,N_v, toroidal_extent).Mesh_Surface_Orientation(false));
    }
    triangle_vector.push_back(flux_surface.Return_UV_Manifold(r_in_between.back(),N_u,N_v, toroidal_extent).Mesh_Surface_Orientation(true));    
    
    bool include_edges = ! toroidal_extent.Full_Angle();
            
    if(include_edges){
        
        auto mesh_plane = [&v_axis, r_in_between, N_u, N_v, toroidal_extent, &flux_surface, includes_axis](bool orientation_switch, unsigned v_i_pos){
            Triangle_Vertices plane;


            unsigned start_r = includes_axis ? 1 : 0;
            

            for(unsigned r_i = start_r ; r_i < r_in_between.size(); ++r_i){
                for(unsigned u_i = 0 ; u_i < N_u; ++u_i){
                    auto u_i_pos_f = Coordinates_From_Discrete_Angles(r_in_between[r_i], u_i, v_i_pos, N_u, N_v, toroidal_extent);
                    auto u_i_pos_r = flux_surface.Return_Position(u_i_pos_f);
                    plane.nodes.push_back(std::make_unique<Flux_Surface_Node>(u_i_pos_f, u_i_pos_r));
                    if(r_i < r_in_between.size()- 1){
                        unsigned u_i_index = (r_i - start_r) * N_u + u_i;
                        unsigned u_i_1_index = (r_i - start_r) * N_u + (u_i + 1)%N_u;
                        unsigned u_i_r1_index = (r_i - start_r + 1) * N_u  + u_i;
                        unsigned u_i_r1_1_index = (r_i - start_r + 1) * N_u  + ( u_i + 1 ) % N_u;
                        if(! orientation_switch){
                            plane.vertices.push_back({u_i_index ,  u_i_r1_index, u_i_1_index});
                            plane.vertices.push_back({u_i_1_index , u_i_r1_index, u_i_r1_1_index});
                        }
                        else{
                            plane.vertices.push_back({u_i_index , u_i_1_index, u_i_r1_index});
                            plane.vertices.push_back({u_i_1_index , u_i_r1_1_index, u_i_r1_index});
                            
                        }
                    }
                }
            }


            if(includes_axis){
                unsigned offset_size = plane.nodes.size();
                
                plane.nodes.push_back(std::make_unique<Node>(v_axis.Real_Coordinate_From_Index(v_i_pos)));
                for(unsigned u_i = 0; u_i < N_u; ++u_i){
                    auto u_i_pos_f = Coordinates_From_Discrete_Angles(r_in_between[start_r], u_i, v_i_pos, N_u, N_v, toroidal_extent);
                
                    auto u_i_pos_r = flux_surface.Return_Position(u_i_pos_f);

                    plane.nodes.push_back(std::make_unique<Flux_Surface_Node>(u_i_pos_f,u_i_pos_r));
                    if(! orientation_switch){
                        plane.vertices.push_back({offset_size , offset_size + 1 + u_i , offset_size + 1 + (u_i + 1) % N_u});
                    }
                    else{
                        plane.vertices.push_back({offset_size , offset_size + 1 + (u_i + 1) % N_u, offset_size + 1 + u_i});
                    }
                    
                }
         
            }
           return plane;
        };
        

        triangle_vector.push_back(mesh_plane(false, 0));
        triangle_vector.push_back(mesh_plane(true, N_v - 1));
    }
    auto result = Triangle_Vertices();
    unsigned offset = 0;
    for(auto& tv  : triangle_vector){
        for(auto& pos : tv.nodes){
            result.nodes.push_back(pos->Make_Unique());
        }
        for(auto& vert : tv.vertices){
            result.vertices.push_back({vert[0] + offset, vert[1] + offset, vert[2] + offset});
        }
        offset += tv.nodes.size();
    }

    return result;

}

Vector Flux_Surfaces::Return_Cylindrical_Position(const Flux_Surface_Coordinates& flux_surface_coordinates) const{
    auto result  = this->Return_Position(flux_surface_coordinates);
    
    auto R_tot   =  sqrt(result[0]*result[0] + result[1]*result[1]);
    auto Z_tot   =  result[2];
    auto phi_tot =  atan2(result[1],result[0]);

    return Vector(R_tot, Z_tot, phi_tot);
}

double Flux_Surfaces::Get_Rmnc_Interp(double s, unsigned i ) const{
    
    if(m_Rmnc.rows() == 1){ return m_Rmnc(0,i);}
    auto lower_index  = unsigned((double(m_Rmnc.rows()) - 1.0) * s );
    
    // if the s = 1.0, it should just be the LCFS (no interpolation needed anyway
    // and cannot do a higher index than the maximum)
    auto higher_index = s == 1.0 ? lower_index  : lower_index + 1;
    auto s_low  = 1.0 / (double(m_Rmnc.rows()) - 1.0) * lower_index;
    auto s_high = 1.0 / (double(m_Rmnc.rows()) - 1.0) * higher_index;
    auto ds     = s == 1.0 ? 1.0 : s_high - s_low;
    auto s_high_fraction  = (s - s_low ) / ds;
    auto s_low_fraction = 1.0 - s_high_fraction;
    return m_Rmnc(lower_index, i) * s_low_fraction + m_Rmnc(higher_index, i) * s_high_fraction;
}

double Flux_Surfaces::Get_Zmns_Interp(double s, unsigned i ) const{
    
    if(m_Zmns.rows() == 1){ return m_Zmns(0,i);}
    auto lower_index  = unsigned((double(m_Rmnc.rows()) - 1.0) * s );
    
    // if the s = 1.0, it should just be the LCFS (no interpolation needed anyway
    // and cannot do a higher index than the maximum)
    auto higher_index = s == 1.0 ? lower_index  : lower_index + 1;
    auto s_low  = 1.0/(double(m_Rmnc.rows()) - 1.0) * lower_index;
    auto s_high = 1.0/(double(m_Rmnc.rows()) - 1.0) * higher_index;
    auto ds     = s == 1.0 ? 1.0 : s_high - s_low;
    auto s_high_fraction  = (s - s_low ) / ds;
    auto s_low_fraction = 1.0 - s_high_fraction;
    return m_Zmns(lower_index, i) * s_low_fraction + m_Zmns(higher_index, i) * s_high_fraction;
}

void print_byte(uint8_t byte)
{
    
    if (32 < byte and byte < 128)
    {
        std::cout << (char)byte<<" ";
    }
    else
    {
        std::cout << (int)byte<<" ";
    }
}

nlohmann::json Flux_Surfaces::Return_Dictionary() const{
    nlohmann::json result;
    result["Type"] = "Flux_Surfaces";
    result["Initialisation_Parameters"]["Settings"] = m_settings.Return_Dictionary();
    result["Initialisation_Parameters"]["Rmnc"] = Eigen_to_BJData(m_Rmnc);
    result["Initialisation_Parameters"]["Zmns"] = Eigen_to_BJData(m_Zmns);    
    return result;
};

VectorArray Total_Array_From_Vector(const std::vector<VectorArray>& v_in){
    
    unsigned total_size = 0;
    for(unsigned i = 0; i < v_in.size(); ++i){
        total_size+= v_in[i].rows();
    }

    auto result = VectorArray(total_size, 3);

    unsigned offset = 0;
    for(unsigned i = 0; i < v_in.size(); ++i){
        result.block(offset ,0, v_in[i].rows(), v_in[i].cols()) = v_in[i];
        offset += v_in[i].rows();
    }

    return result;
}

std::pair<VectorArray, std::vector<UnsignedVectorArray>> Mesh_Watertight_Flux_Surfaces(const Flux_Surfaces& flux_surfaces, Radial_Flux_Coordinate r_start, std::vector<Differential_Radial_Flux_Coordinate> diff_r_vector, unsigned n_theta, unsigned n_phi, const Toroidal_Extent& toroidal_extent ){
    sb_assert_message(r_start.Get_s() > 0.0, "Meshing watertight surfaces does not support starting at the axis!");
    std::pair<VectorArray, std::vector<UnsignedVectorArray>> result;
    
    std::vector<VectorArray> total_points;

    auto mesh_surface = [&flux_surfaces, n_theta, n_phi, toroidal_extent](Radial_Flux_Coordinate r_surface, bool surfaces_normal){        
        auto triangle_vertices = flux_surfaces.Return_UV_Manifold(r_surface, n_theta, n_phi, toroidal_extent).Mesh_Surface_Orientation(surfaces_normal);

        return Triangle_Vertices_to_Numeric(triangle_vertices);
    };  
    
    

    auto mesh_inter_surface = [n_theta, n_phi](unsigned offset_0, unsigned offset_1){
        auto total_index = [n_theta, n_phi](unsigned theta_i, unsigned phi_i){
            return (theta_i%n_theta) * n_phi + phi_i;
        };

        auto result = UnsignedVectorArray(  2 * n_theta * 2 , 3).setZero(); // first 2 is for two triangle per block, second for front and backside
        for(unsigned theta_i = 0; theta_i < n_theta; ++theta_i){
            
            result(2 * theta_i + 0, 0  ) = offset_0 + total_index(theta_i,     0);
            result(2 * theta_i + 0, 1  ) = offset_1 + total_index(theta_i,     0);
            result(2 * theta_i + 0, 2  ) = offset_0 + total_index(theta_i + 1, 0);
            
            result(2 * theta_i + 1, 0  ) = offset_1 + total_index(theta_i,     0);
            result(2 * theta_i + 1, 1  ) = offset_1 + total_index(theta_i + 1, 0);
            result(2 * theta_i + 1, 2  ) = offset_0 + total_index(theta_i + 1, 0);

            result(2 * theta_i + 0 + 2 * n_theta, 0  ) = offset_1 + total_index(theta_i,     n_phi - 1);
            result(2 * theta_i + 0 + 2 * n_theta, 1  ) = offset_0 + total_index(theta_i,     n_phi - 1);
            result(2 * theta_i + 0 + 2 * n_theta, 2  ) = offset_0 + total_index(theta_i + 1, n_phi - 1);

            result(2 * theta_i + 1 + 2 * n_theta, 0  ) = offset_1 + total_index(theta_i + 1, n_phi - 1);
            result(2 * theta_i + 1 + 2 * n_theta, 1  ) = offset_1 + total_index(theta_i,     n_phi - 1);
            result(2 * theta_i + 1 + 2 * n_theta, 2  ) = offset_0 + total_index(theta_i + 1, n_phi - 1);

        }

        return result;
    };

    unsigned total_offset = 0;
    // First wall has the normals in the radially inwards direction (the total solid should be enclosed by surfaces with outwards normal -> first surface has radially inwards normal)
    auto first_surface = mesh_surface(r_start, false);
    total_points.push_back(first_surface.first);
    result.second.push_back(first_surface.second + total_offset);
    total_offset += first_surface.first.rows();

    // Mesh all other surfaces with radially outward normals
    Radial_Flux_Coordinate r_current = r_start;
    for(unsigned i = 0; i < diff_r_vector.size(); ++i){
        r_current = r_current + diff_r_vector[i];        
        auto surface_i = mesh_surface(r_current , true);

        total_points.push_back(surface_i.first);
        // Mesh interplane surface:

        unsigned offset_previous_surface = total_offset - total_points[i].rows();
        unsigned offset_this_surface     = total_offset;


        result.second.push_back(mesh_inter_surface(offset_previous_surface, offset_this_surface));


        result.second.push_back(surface_i.second + total_offset);

        total_offset += surface_i.first.rows();
    }

    // Mesh interplane surfaces:

    result.first = Total_Array_From_Vector(total_points)    ;

    return result;
}; 