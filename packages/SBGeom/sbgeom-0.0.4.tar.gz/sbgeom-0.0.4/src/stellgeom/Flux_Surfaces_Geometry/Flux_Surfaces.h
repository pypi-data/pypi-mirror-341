#pragma once
#include <string>
#include <vector>
#include "Vector.h"
#include <fstream>
#include "Matrix.h"
#include "Constants.h"
#include <cmath>    
#include "json.h"
#include "Flux_Surface_Coords.h"
#include "UV_Manifolds.h"



/*!
 * \brief Class for handling VMEC-type flux surfaces
 * 
 * Given an array of \f$ R^{mn}_c\f$, \f$ Z^{mn}_s\f$ and \f$ B^{mn}_c\f$ arrays (through a simple .dat file) this class
 * provides functions to calculate Cartesian coordinates of \f$(s,u,v)\f$ flux-surface coordinates. 
 * 
 * Furthermore, it also provides a template for handling distance beyond the LCFS using a derived class (i.e. Flux_Surfaces_Extended)
 * using the extended flux surface coordinates \f$ (r,u,v) \f$ where \f$ r = {s, d} \f$ and \f$ d\f$ is the distance beyond the LCFS
 * Uses Flux_Surface_Coordinates.
 * 
 * The base class will immediately throw if an extension is desired; on purpose this is ambiguous in the base class so just unimplemented.
 * 
 * Use the derived classes Flux_Surfaces_Fourier_Extended and Flux_Surfaces_Normal_Extended
*/
class Flux_Surfaces {
    using json = nlohmann::json;
    public: 
     

        
         
        /**
         * @brief Construct a new Flux_Surfaces object
         * 
         * @param Rmnc 
         * @param Zmns 
         * @param fs_settings 
         */
        Flux_Surfaces(const Array& Rmnc,const Array& Zmns, Flux_Surface_Settings fs_settings) : m_Rmnc(1,1), m_Zmns(1,1){this->Set_Data_Members(fs_settings, Rmnc, Zmns);}



        /**
         * @brief Factory method to construct a Flux_Surfaces object from a JSON object. 
         * 
         * The structure of the JSON object is 
         * \verbatim embed:rst:leading-asterisk 
         * .. code-block:: javascript
         * 
         *      {
         *         "Flux_Surfaces" : {
         *              "Type" : string
         *              "Filenames" : json_object
         *          }
         *      }
         * \endverbatim
         * 
         * The type can be 
         * \verbatim embed:rst:leading-asterisk 
         * .. code-block:: javascript
         * 
         *      {"HDF5",  "netCDF4"}
         * 
         * \endverbatim
         * 
         * where the name refers to the type of data. If the type is HDF5, the @verbatim embed:rst:inline :code:`Filenames` @endverbatim
         * JSON object should have a structure 
         * \verbatim embed:rst:leading-asterisk 
         * .. code-block:: javascript
         * 
         *      {
         *          "Filename_H5" : string
         *      }
         * 
         * \endverbatim 
         * with the file being created by a Simulation::Save_HDF5 call. 
         * 
         * 
         * where the corresponding the files should be created by @verbatim embed:rst:inline :ref:`VMEC Data processing <vmec_data_process>` @endverbatim. 
         * 
         * If the type is netCDF4 the @verbatim embed:rst:inline :code:`Filenames` @endverbatim JSON object should have the structure 
         * \verbatim embed:rst:leading-asterisk 
         * .. code-block:: javascript
         * 
         *      {
         *          "Filename_netCDF4" : string
         *      }
         * 
         * \endverbatim  
         * with the file being created by a VMEC run. Note that VMEC outputs a netcdf3 file which is not compatible and should be converted to a netcdf4 file.
         * The easiest way to do this is using the @verbatim embed:rst:inline :code:`nccopy` @endverbatim utility: 
         * \verbatim embed:rst:leading-asterisk 
         * .. code-block:: bash
         * 
         *      nccopy -k 4 old_file.nc old_file.nc4
         * 
         * \endverbatim  
         * 
         * @param json 
         * @return std::unique_ptr<Flux_Surfaces> 
         */
//        static std::unique_ptr<Flux_Surfaces> Construct_Flux_Surface(const json& json);    


        /**
         * @brief Return the Cartesian coordinate corresponding to flux-surface coordinates \f$(s,u,v)\f$ 
         * 
         * @param s Radial Flux-surface coordinate (from 0.0 to 1.0)
         * @param u Poloidal flux-surface coordinate (from 0.0 to \f$ 2\pi \f$)
         * @param v Toroidal flux-surface coordinate (from 0.0 to \f$ 2\pi \f$)
         * @return Vector Cartesian (X,Y,Z) coordinate
         */
        virtual Vector Return_Position(const Flux_Surface_Coordinates& flux_surface_coordinates) const;

        Vector Return_Position_Index(size_t index, double u, double v) const;

        /**
         * @brief Returns \f$(R,Z,\phi)\f$ from flux surface coordinates \f$(r,u,v)\f$
         * 
         * @param flux_surface_coordinates 
         * @return Vector 
         */
        Vector Return_Cylindrical_Position(const Flux_Surface_Coordinates& flux_surface_coordinates) const;

        /**
         * @brief Function to return the axis position of a particular angle \f$v\f$
         * 
         * @param v 
         * @return Vector 
         */
        Vector Return_Axis_Position(double v)const;

        /**
         * @brief Returns a surface normal on a Flux_Surface_Coordinates
         * 
         * @param flux_surface_coordinates 
         * @return Unit_Vector 
         */
        virtual Unit_Vector Return_Surface_Normal(const Flux_Surface_Coordinates& flux_surface_coordinates) const;
        
        
        /**
         * @brief Function to return a 2D array containing all positions of a discretised flux surface
         * 
         * @param s Radial Flux-surface coordinate (from 0.0 to 1.0)
         * @param N_u Number of poloidal angles in the surface
         * @param N_v Number of toroidal angles in the surface
         * @return std::vector<std::vector<Vector>> 2D array containing all positions of a discretised flux surface.
         * First index determines the poloidal angle \f$ u \f$ and the second \f$ v\f$
         */
        UV_Manifold Return_UV_Manifold(Radial_Flux_Coordinate r, unsigned N_u, unsigned N_v) const ;

        /**
         * @brief Function to return a 2D array containing all positions of a (part of a) discretised flux surface
         * 
         * @param s Radial Flux-surface coordinate (from 0.0 to 1.0)
         * @param N_u Number of poloidal angles in the surface
         * @param N_v Number of toroidal angles in the surface
         * @param v_min minimum toroidal angle
         * @param v_max maximum toroidal angle
         * @return std::vector<std::vector<Vector>> 2D array containing all positions of a discretised flux surface.
         * First index determines the poloidal angle \f$ u \f$ and the second \f$ v\f$
         */
        UV_Manifold Return_UV_Manifold(Radial_Flux_Coordinate r, unsigned N_u, unsigned N_v, const Toroidal_Extent& toroidal_extent) const;

        /**
         * @brief Returns the V_axis of this Flux_Surfaces
         * 
         * @param N_v 
         * @return V_Axis 
         */
        V_Axis      Return_V_Axis(unsigned N_v) const;

        /**
         * @brief Returns the V_axis of this Flux_Surfaces for a given Toroidal_Extent
         * 
         * @param N_v 
         * @param toroidal_extent 
         * @return V_Axis 
         */
        V_Axis      Return_V_Axis(unsigned N_v, const Toroidal_Extent& toroidal_extent) const;                
        
        /**
         * @brief Returns the symmetry of the VMEC flux surfaces
         * 
         * @return unsigned 
         */
        unsigned Symmetry()const{return m_settings.symmetry;}

        unsigned Index_in_Matrix(double s) const { return unsigned( (double(m_Rmnc.rows()) - 1.0) * s);}

        Flux_Surface_Settings Get_Flux_Surface_Settings()const{
            return m_settings;
        }

        const Array& Get_Rmnc()const{return m_Rmnc;}
        const Array& Get_Zmns()const{return m_Zmns;}

        auto Get_m_mpol_vector() const {return m_mpol_vector;}
        auto Get_n_ntor_vector() const {return m_ntor_vector;}

        virtual ~Flux_Surfaces();

        virtual std::string Write_str() const{
            return "Flux_Surfaces(\n" + m_settings.Write_Settings() +")";
        }


        virtual nlohmann::json Return_Dictionary() const;
    protected:

        void Set_Data_Members(const Flux_Surface_Settings& flux_surface_settings, const Array& Rmnc, const Array& Zmns);

        double Get_Rmnc_Interp(double s, unsigned i) const;
        double Get_Zmns_Interp(double s, unsigned i) const;
        Array m_Rmnc;
        Array m_Zmns;
        DynamicVector m_ntor_vector;
        DynamicVector m_mpol_vector;
        Flux_Surface_Settings m_settings;

        double m_du_x_dv_sign = 1.0;
        void Set_du_x_dv_sign();


};
/**
 * @brief Class that describes a discretised flux surface with a specific radial coordinate \f$ s\f$
 * 
 * 
 */
class Discrete_Flux_Surface{
    public: 
        /**
         * @brief Construct a new Discrete_Flux_Surface object
         * 
         * @param flux_surfaces A Flux_Surfaces object containing a method to discretise a certain flux surface
         * @param r Radial_Flux_Coordinate which the discrete surface describes
         * @param N_u Number of poloidal angles in the surface
         * @param N_v Number of toroidal angles in the surface
         */
        Discrete_Flux_Surface(const Flux_Surfaces& flux_surfaces, Radial_Flux_Coordinate r,  unsigned N_u, unsigned N_v, const Toroidal_Extent& toroidal_extent) : m_N_u(N_u), m_N_v(N_v), m_locations(flux_surfaces.Return_UV_Manifold(r,N_u,N_v,toroidal_extent)){ }
    protected:
        UV_Manifold m_locations;
        unsigned m_N_u; 
        unsigned m_N_v;
};

std::pair<VectorArray, std::vector<UnsignedVectorArray>>  Mesh_Watertight_Flux_Surfaces(const Flux_Surfaces& flux_surfaces, Radial_Flux_Coordinate r_start, std::vector<Differential_Radial_Flux_Coordinate> diff_r_vector, unsigned n_theta, unsigned n_phi, const Toroidal_Extent& toroidal_extent );

Triangle_Vertices Mesh_Closed_Flux_Surface(const Flux_Surfaces& flux_surface, std::array<Radial_Flux_Coordinate, 2> r_vector, unsigned N_u, unsigned N_v, const Toroidal_Extent& toroidal_extent);


        // /**
        //  * @brief Construct a new Flux_Surfaces object from an HDF5 group.
        //  * 
        //  * Created by a previous run of this code.
        //  * @param flux_surface_hid 
        //  */
        // static std::unique_ptr<Flux_Surfaces> Load_HDF5(hid_t flux_surface_hid);

//             /**
//          * @brief Function to load a VMEC NC4 file.
//          * 
//          * @param filename_VMEC_NC4 
//          * @param extension_json 
//          * @return std::unique_ptr<Flux_Surfaces> 
//          */
// static std::unique_ptr<Flux_Surfaces> Load_VMEC_NetCDF4(std::string filename_VMEC_NC4, const json& extension_json);


