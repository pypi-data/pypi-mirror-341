#include "Flux_Surfaces_Extended.h"


/*
Flux_Surfaces_Fourier_Extended::Flux_Surfaces_Fourier_Extended(Array&& Rmnc, Array&& Zmns, Flux_Surface_Settings fs_settings, hid_t flux_surface_hid) : Flux_Surfaces(std::move(Rmnc), std::move(Zmns), fs_settings){
    try{
        m_Rmnc_extension = HDF5_Load_Array(flux_surface_hid, "Rmnc_extension");
        m_Zmns_extension = HDF5_Load_Array(flux_surface_hid, "Zmns_extension");;
        m_d_extension    = HDF5_Load_Array(flux_surface_hid, "d_extension");
        if(! this->Check_Compatible()){
            throw std::runtime_error("Extension does not have the same size (same toroidal and poloidal harmonic numbers) as the base flux surface class..");
        }
    }
    catch(const std::exception& e){
        std::cout<< e.what()<<" in Flux_Surfaces_Fourier_Extended(Array&&, Array&&, Flux_Surface_Settings, hid_t). Aborting..."<<std::endl;
        abort();
    }
    
    
};
*/
Flux_Surfaces_Fourier_Extended::Flux_Surfaces_Fourier_Extended(const Array& Rmnc,const Array& Zmns, Flux_Surface_Settings fs_settings,\
                                                              const DynamicVector& d_extension, const Array& Rmnc_extension, const Array& Zmns_extension, Flux_Surface_Settings fs_settings_ex) : Flux_Surfaces(Rmnc, Zmns, fs_settings),\
                                                                                                                                                                                  m_extension_fs(Rmnc_extension, Zmns_extension, fs_settings_ex),
                                                                                                                                                                                  m_d_extension(d_extension){
        if(! this->Check_Compatible()){
            throw std::runtime_error("Extension does not have the same number of surfaces as the provided distance vector");
        }
                                                                                                                                                                                  
};
Flux_Surfaces_Fourier_Extended::Flux_Surfaces_Fourier_Extended(const Flux_Surfaces& flux_surfaces,\
                                                              const DynamicVector& d_extension, const Array& Rmnc_extension, const Array& Zmns_extension, Flux_Surface_Settings fs_settings_ex) : Flux_Surfaces(flux_surfaces),\
                                                                                                                                                                                  m_extension_fs(Rmnc_extension, Zmns_extension, fs_settings_ex),
                                                                                                                                                                                  m_d_extension(d_extension){
        if(! this->Check_Compatible()){
            throw std::runtime_error("Extension does not have the same number of surfaces as the provided distance vector");
        }
                                                                                                                                                                                  
};

/*/
Flux_Surfaces_Fourier_Extended::Flux_Surfaces_Fourier_Extended(std::string filename_VMEC_NC4, const json& json_extension) : Flux_Surfaces(filename_VMEC_NC4){
    
    try{
        auto extension_file_name = json_extension.at("Initialisation_Parameters").at("Filename_Extension").get<std::string>();
        auto file_id = H5Fopen(extension_file_name.c_str(), H5F_ACC_RDONLY, H5P_DEFAULT);
            if(file_id == H5I_INVALID_HID){throw std::invalid_argument(" File " + extension_file_name + " not found ");}
            m_Rmnc_extension = HDF5_Load_Array(file_id, "Rmnc_extension");
            m_Zmns_extension = HDF5_Load_Array(file_id, "Zmns_extension");
            m_d_extension    = HDF5_Load_Array(file_id, "d_extension")   ;
        auto status       = H5Fclose(file_id);
        if(! this->Check_Compatible()){
            throw std::runtime_error("Extension does not have the same size (same toroidal and poloidal harmonic numbers) as the base flux surface class..");
        }
    }
    catch(const std::exception& e){
        std::cout<< e.what()<< " in Flux_Surfaces_Fourier_Extended(std::string filename_VMEC_NC4, const json& json_extension)"<<std::endl;
        abort();
    }
};
Flux_Surfaces_Fourier_Extended::Flux_Surfaces_Fourier_Extended(std::string filename_VMEC_NC4, std::string filename_extension) : Flux_Surfaces(filename_VMEC_NC4){
    try{
        auto file_id = H5Fopen(filename_extension.c_str(), H5F_ACC_RDONLY, H5P_DEFAULT);
            if(file_id == H5I_INVALID_HID){throw std::invalid_argument(" File " + filename_extension + " not found ");}
            m_Rmnc_extension = HDF5_Load_Array(file_id, "Rmnc_extension");
            m_Zmns_extension = HDF5_Load_Array(file_id, "Zmns_extension");
            m_d_extension    = HDF5_Load_Array(file_id, "d_extension")   ;
        auto status       = H5Fclose(file_id);
    }
    catch(const std::exception& e){
        std::cout<< e.what()<< " in Flux_Surfaces_Fourier_Extended(std::string filename_VMEC_NC4, std::string filename_extension)"<<std::endl;
        abort();
    }
    
};
*/
unsigned Flux_Surfaces_Fourier_Extended::Find_Index_d(double d) const{
    unsigned result = 0;
    bool     found  = false;
    for(unsigned i = 0; i < m_d_extension.rows(); ++i){
        if(d <= m_d_extension[i]){
            result = i;
            found  = true;
            break;
        }
    }
    if( ! found){throw std::invalid_argument(" Trying to calculate a position beyond the last surface in Flux_Surfaces_Fourier_Extend.");}
    return result;
}

bool    Flux_Surfaces_Fourier_Extended::Check_Compatible() const{
    return m_d_extension.rows() == m_extension_fs.Get_Flux_Surface_Settings().number_of_surfaces;
};
Vector Flux_Surfaces_Fourier_Extended::Return_Extension_Position(unsigned index, double u, double v) const{
    return m_extension_fs.Return_Position_Index(index, u, v);
}
Vector Flux_Surfaces_Fourier_Extended::Return_Position(const Flux_Surface_Coordinates& flux_surface_coordinates) const{
    Vector result(0.0,0.0,0.0);
    
    if(flux_surface_coordinates.Get_distance_LCFS() == 0.0){
        result = Flux_Surfaces::Return_Position(flux_surface_coordinates);
    }
    else{
        auto d = flux_surface_coordinates.Get_distance_LCFS();
        auto s = flux_surface_coordinates.Get_s(); // Will always be 1.0; Radial_Flux_Surface_Coordinate throws if d > 0.0 && s < 1.0
        
        auto d_max_index = this->Find_Index_d(d);
        auto result_start = Vector(0.0,0.0,0.0);
        auto result_end   = Vector(0.0,0.0,0.0);

        double d_start      = 0.0;
        
        if(d_max_index == 0){
            result_start = Flux_Surfaces::Return_Position({{1.0,0.0}, flux_surface_coordinates.u,flux_surface_coordinates.v});
            d_start      = 0.0;
        }
        else{
            result_start = this->Return_Extension_Position(d_max_index - 1, flux_surface_coordinates.u, flux_surface_coordinates.v);
            d_start      = m_d_extension(d_max_index - 1);
        }
        result_end       = this->Return_Extension_Position(d_max_index, flux_surface_coordinates.u, flux_surface_coordinates.v);
        
        double d_end            = m_d_extension(d_max_index);
        auto d_max_fraction = (d - d_start) / (d_end - d_start);
        auto d_min_fraction =  1.0 - d_max_fraction;
        result = result_start * d_min_fraction + result_end * d_max_fraction;
    }    
    return result;
};

Unit_Vector Flux_Surfaces_Fourier_Extended::Return_Surface_Normal(const Flux_Surface_Coordinates& flux_surface_coordinates) const{
    auto result = Vector(1.0,0.0,0.0);
    if(flux_surface_coordinates.Get_distance_LCFS() == 0.0){
        result = Flux_Surfaces::Return_Surface_Normal(flux_surface_coordinates);
    }
    else{
        auto d = flux_surface_coordinates.Get_distance_LCFS();

        auto d_max_index = this->Find_Index_d(d);

        double d_start = 0.0;

        Vector result_start = Vector(1.0,0.0,0.0);
        Vector result_end   = Vector(1.0,0.0,0.0);

        if(d_max_index == 0){
            d_start = 0.0;
            result_start = Flux_Surfaces::Return_Surface_Normal({{1.0, 0.0}, flux_surface_coordinates.u, flux_surface_coordinates.v});
        }
        else{
            
            result_start = m_extension_fs.Return_Surface_Normal({{double(d_max_index - 1) / double(m_d_extension.size()), 0.0}, flux_surface_coordinates.u, flux_surface_coordinates.v});
            
            d_start = m_d_extension(d_max_index);
            
        }
        result_end = m_extension_fs.Return_Surface_Normal({{double(d_max_index) / double(m_d_extension.size()), 0.0}, flux_surface_coordinates.u, flux_surface_coordinates.v});
        
        double d_end = m_d_extension(d_max_index);
        auto d_max_fraction = (d - d_start) / (d_end - d_start);
        auto d_min_fraction =  1.0 - d_max_fraction;
        // the extension thinks it has s = 0.0 to s=1.0 linearly spaced. So we have to have 
        // the percent_max * the d_max_index surface and the 1 - percent_max * the d_min_index ()
        result = result_start * d_min_fraction + result_end * d_max_fraction;
    }
    return Unit_Vector(result);
};

/*
void  Flux_Surfaces_Fourier_Extended::Save_HDF5(hid_t location_id) const{
    Flux_Surfaces::Save_HDF5(location_id);
    auto fs_id  = H5Gopen(location_id, "Flux_Surfaces", H5P_DEFAULT); 
        HDF5_Add_Unsigned_Attribute("Extension", fs_id, Flux_Surfaces_Fourier_Extended_type_H5); 
        HDF5_Store_Array(m_Rmnc_extension, fs_id, "Rmnc_extension");
        HDF5_Store_Array(m_Zmns_extension, fs_id, "Zmns_extension");
        HDF5_Store_Array(m_d_extension,    fs_id, "d_extension");
    auto status = H5Gclose(fs_id);
};
*/

Vector Flux_Surfaces_Normal_Extended::Return_Position(const Flux_Surface_Coordinates& flux_surface_coordinates) const{
    auto base_coordinate = Flux_Surface_Coordinates({flux_surface_coordinates.Get_s(), 0.0}, flux_surface_coordinates.u, flux_surface_coordinates.v);
    auto xyz = Flux_Surfaces::Return_Position(base_coordinate);
    Vector result;
    if(fabs(flux_surface_coordinates.Get_distance_LCFS()) > 0.0){        
        result = xyz + this->Return_Surface_Normal(base_coordinate) * flux_surface_coordinates.Get_distance_LCFS();
    }
    else{
        result = xyz;
    }
    return result;
 };

 Vector Flux_Surfaces_Normal_Extended_Constant_Phi::Return_Position(const Flux_Surface_Coordinates& flux_surface_coordinates) const{
    static constexpr double conv_tol = 1e-8; // completely arbitrary, but R < 100 so this tolerance will yield at most micrometer errors and is not too small for floating point errors. 
    static constexpr unsigned max_iter = 10; // This should always converge, we can throw if it does not.

    Radial_Flux_Coordinate base_radial = flux_surface_coordinates.r;
    double                 u           = flux_surface_coordinates.u;
    double                 v_desired   = flux_surface_coordinates.v;
    
    double x_minus_two = flux_surface_coordinates.v + 1e-3;
    double x_minus_one = flux_surface_coordinates.v;

    auto distance_angles = [](double a1, double a2){
        return atan2(sin(a1 - a2), cos(a1- a2));
    };

    auto fn = [this, distance_angles, base_radial, u, v_desired](double v){
        auto pos = Flux_Surfaces_Normal_Extended::Return_Position({base_radial,u,v});
        return distance_angles(atan2(pos[1], pos[0]), v_desired);
    };


    
    for(unsigned i = 0; i < max_iter + 1; ++i){    
        
        if(i == max_iter){
            std::cout<<("Tolerance not achieved in Flux_Surfaces_Normal_Extended_Constant_Phi::Return_Position. Err = (" + std::to_string(fn(x_minus_one))+"), tol="+std::to_string(conv_tol))<<std::endl;
            throw std::runtime_error("Tolerance not achieved in Flux_Surfaces_Normal_Extended_Constant_Phi::Return_Position. Err = (" + std::to_string(fn(x_minus_one))+"), tol="+std::to_string(conv_tol));
        }
        double f_n_minus_one = fn(x_minus_one);
        if(abs(f_n_minus_one) < conv_tol){
            break;
        }
        double f_n_minus_two = fn(x_minus_two);
        
        double x_minus_two_temp = x_minus_one;

        x_minus_one = x_minus_one - f_n_minus_one * distance_angles(x_minus_one, x_minus_two) / (f_n_minus_one - f_n_minus_two);
        x_minus_two = x_minus_two_temp;
                
    }
    
    return Flux_Surfaces_Normal_Extended::Return_Position({base_radial, u, x_minus_one});
 };
 

 


//void Flux_Surfaces_Normal_Extended::Save_HDF5(hid_t location_id) const {Flux_Surfaces::Save_HDF5(location_id) ; auto fs_id = H5Gopen(location_id, "Flux_Surfaces", H5P_DEFAULT); HDF5_Add_Unsigned_Attribute("Extension", fs_id, Flux_Surfaces_Normal_Extended_type_H5); auto status = H5Gclose(fs_id);};