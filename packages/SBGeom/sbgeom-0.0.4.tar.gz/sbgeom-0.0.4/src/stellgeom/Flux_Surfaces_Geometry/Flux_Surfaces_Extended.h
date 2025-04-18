#include "Flux_Surfaces.h"
#include "json_utility.h"
/**
 * @brief Derived class of Flux_Surfaces for a Fourier extension
 * 
 * This extension has the same Fourier coefficients as the base class but defined beyond \f$ s=1\f$. 
 * 
 * It uses internally a \f$d\f$ (distance from LCFS) vector. Distances between the defined \f$d\f$ manifolds are linearly interpolated.
 * 
 */
class Flux_Surfaces_Fourier_Extended : public Flux_Surfaces {
    using  json = nlohmann::json ;
    public:

    /**
     * @brief Construct a new Flux_Surfaces_Fourier_Extended object
     * 
     * Directly uses the provided data
     * 
     * @param Rmnc 
     * @param Zmns 
     * @param fs_settings 
     * @param d_extension 
     * @param Rmnc_extension 
     * @param Zmns_extension 
     */
    Flux_Surfaces_Fourier_Extended(const Array& Rmnc, const Array& Zmns, Flux_Surface_Settings fs_settings, const DynamicVector& d_extension, const Array& Rmnc_extension, const Array& Zmns_extension, Flux_Surface_Settings fs_extension_settings);
    Flux_Surfaces_Fourier_Extended(const Flux_Surfaces& flux_surfaces, const DynamicVector& d_extension, const Array& Rmnc_extension, const Array& Zmns_extension, Flux_Surface_Settings fs_extension_settings);

    /**
     * @brief Override of Flux_Surfaces::Return_Position
     * 
     * @param flux_surface_coordinates 
     * @return Vector 
     */
    Vector Return_Position(const Flux_Surface_Coordinates& flux_surface_coordinates) const override;

    Unit_Vector Return_Surface_Normal(const Flux_Surface_Coordinates& flux_surface_coordinates) const override;

    const Array& Get_Rmnc_Extension()const{return m_extension_fs.Get_Rmnc();}
    const Array& Get_Zmns_Extension()const{return m_extension_fs.Get_Zmns();}
    Flux_Surface_Settings Get_Flux_Surface_Settings_Extension() const{return m_extension_fs.Get_Flux_Surface_Settings();}
    DynamicVector Get_Extension_Labels() const {return m_d_extension;}

    nlohmann::json Return_Dictionary() const{
        nlohmann::json result = Flux_Surfaces::Return_Dictionary();
        result.at("Type") = "Flux_Surfaces_Fourier_Extended";
        result.at("Initialisation_Parameters")["d_extension"] = Eigen_to_BJData(m_d_extension);
        result.at("Initialisation_Parameters")["Extension"] = m_extension_fs.Return_Dictionary();
        return result;

        
    };
    virtual std::string Write_str() const{
        return "Flux_Surfaces_Fourier_Extended(\n  Base:     \n" + m_settings.Write_Settings() +"\n" +\
               "  Extension:\n"+ m_extension_fs.Get_Flux_Surface_Settings().Write_Settings()+")";
    }
       
    private:
        bool     Check_Compatible() const;
        unsigned Find_Index_d(double d) const;
        Vector   Return_Extension_Position(unsigned index, double u, double v) const;        
        DynamicVector m_d_extension;
        Flux_Surfaces m_extension_fs;
};

/**
 * @brief Derived class of Flux_Surfaces for a normal vector extension
 * 
 * See Lion, Jorrit, Felix Warmer, and Huaijin Wang. "A deterministic method for the fast evaluation and optimisation of the 3D neutron wall load for generic stellarator configurations." Nuclear Fusion 62.7 (2022): 076040.
 * 
 */
class Flux_Surfaces_Normal_Extended : public Flux_Surfaces { 
    public:
        
        /**
         * @brief Construct a new Flux_Surfaces_Normal_Extended object 
         * 
         * Does not need extra data: the extension is obtained by using normal vectors of the LCFS.
         * 
         * @param Rmnc 
         * @param Zmns 
         * @param fs_settings 
         */
        Flux_Surfaces_Normal_Extended(const Array& Rmnc, const Array& Zmns, Flux_Surface_Settings fs_settings) : Flux_Surfaces(Rmnc, Zmns, fs_settings) {};
        /**
         * @brief Construct a new Flux_Surfaces_Normal_Extended object
         * 
         * Copies an existing Flux_Surfaces for the base class initialisation
         * 
         * @param flux_surfaces 
         */
        Flux_Surfaces_Normal_Extended(const Flux_Surfaces& flux_surfaces) : Flux_Surfaces(flux_surfaces){}
                

        /**
         * @brief Override of Flux_Surfaces::Return_Position
         * 
         * @param flux_surface_coordinates 
         * @return Vector 
         */
        Vector Return_Position(const Flux_Surface_Coordinates& flux_surface_coordinates) const override;

        virtual std::string Write_str() const{
            return "Flux_Surfaces_Normal_Extended(\n" + m_settings.Write_Settings() +")";
        }
        nlohmann::json Return_Dictionary() const{
            nlohmann::json result = Flux_Surfaces::Return_Dictionary();
            result.at("Type") = "Flux_Surfaces_Normal_Extended";
            return result;
        };
    private:

};

/**
 * @brief Derived class of Flux_Surfaces for a normal vector extension
 * 
 * See Lion, Jorrit, Felix Warmer, and Huaijin Wang. "A deterministic method for the fast evaluation and optimisation of the 3D neutron wall load for generic stellarator configurations." Nuclear Fusion 62.7 (2022): 076040.
 * 
 */
class Flux_Surfaces_Normal_Extended_Constant_Phi: public Flux_Surfaces_Normal_Extended { 
    public:
        
        /**
         * @brief Construct a new Flux_Surfaces_Normal_Extended object 
         * 
         * Does not need extra data: extension is obtained using normal vectors from the LCFS.
         * 
         * @param Rmnc 
         * @param Zmns 
         * @param fs_settings 
         */
        Flux_Surfaces_Normal_Extended_Constant_Phi(const Array& Rmnc, const Array& Zmns, Flux_Surface_Settings fs_settings) : Flux_Surfaces_Normal_Extended(Rmnc, Zmns, fs_settings) {};

        /**
         * @brief Construct a new Flux_Surfaces_Normal_Extended_Constant_Phi object
         * 
         * Copies an existing Flux_Surfaces class for the base class initialisation.
         * 
         * @param flux_surfaces 
         */
        Flux_Surfaces_Normal_Extended_Constant_Phi(const Flux_Surfaces& flux_surfaces) : Flux_Surfaces_Normal_Extended(flux_surfaces){}
                

        /**
         * @brief Override of Flux_Surfaces::Return_Position
         * 
         * @param flux_surface_coordinates 
         * @return Vector 
         */
        Vector Return_Position(const Flux_Surface_Coordinates& flux_surface_coordinates) const override;
        virtual std::string Write_str() const{
            return "Flux_Surfaces_Normal_Extended_Constant_Phi(\n" + m_settings.Write_Settings() +")";
        }

        nlohmann::json Return_Dictionary() const{
            nlohmann::json result = Flux_Surfaces::Return_Dictionary();
            result.at("Type") = "Flux_Surfaces_Normal_Extended_Constant_Phi";
            return result;
        };
    private:

};