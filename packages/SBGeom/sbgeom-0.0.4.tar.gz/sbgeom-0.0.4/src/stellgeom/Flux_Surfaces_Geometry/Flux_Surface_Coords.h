#pragma once
#include "Constants.h"
#include <array>
#include <cmath>   
#include <iostream>
#include <sstream>
#include "custom_assert.h"
#include "json.h"
/**
 * 
 * @brief Class for wrapping a toroidal extent
 * 
 * It is mainly used to have user-safe angles (i.e., checking happens once on construction, not every function needs to check it)
 * 
 */
class Toroidal_Extent{
    public:
        Toroidal_Extent(const Toroidal_Extent& toroidal_extent) : m_vmin(toroidal_extent.m_vmin), m_vmax(toroidal_extent.m_vmax), m_full_angle(toroidal_extent.m_full_angle){}
        /**
         * @brief Construct a new Toroidal_Extent object from a minimum and maximum angle
         * 
         * It is checked that these are sensible in Debug mode.
         * 
         * @param v_min 
         * @param v_max 
         */
        Toroidal_Extent(double v_min, double v_max) : m_vmin(v_min), m_vmax(v_max){
            //if( ! (v_min < v_max && v_min >= 0 && v_max <= 2*Constants::pi)){
            //    throw std::invalid_argument("Trying to construct invalid toroidal extent with v_min="+std::to_string(v_min)+", v_max="+std::to_string(v_max)\
            //                                +".\n Please only use angles between 0 and 2 pi for a Toroidal_Extent. In Toroidal_Extent::Toroidal_Extent(double v_min, double v_max) in Flux_Surfaces.h");}
            
            if(fabs(2*Constants::pi - (m_vmax - m_vmin)) < 1e-5 ){ m_full_angle = true; }
        }
        Toroidal_Extent() : Toroidal_Extent(0.0, 2*Constants::pi) {};

        Toroidal_Extent(std::array<double,2> minmaxarr) : Toroidal_Extent(minmaxarr[0], minmaxarr[1]){}

        /**
         * @brief Function that yields whether this Toroidal_Extent will span the whole angle. 
         * 
         * @return true 
         * @return false 
         */
        bool Full_Angle() const{return m_full_angle; }

        /**
         * @brief Write out some information about the Toroidal_Extent.
         * 
         */
        void Write()const{
            std::cout<<" Toroidal_Extent at "<<this<<" from "<<m_vmin<<" to "<<m_vmax<<" which is toroidally ";if(this->Full_Angle()){std::cout<<"connected ";}else{std::cout<<"disconnected";}std::cout<<std::endl;
        }
        /**
         * @brief Minimum angle
         * 
         * @return double 
         */
        double min()const{ return m_vmin;}
        /**
         * @brief Maximum angle.
         * 
         * @return double 
         */
        double max()const{ return m_vmax;}
    
    private:

    double m_vmin = 0.0;
    double m_vmax = 2 *Constants::pi;
    bool   m_full_angle = false;

};



/**
 * @brief Class to facilitate reading of simple .dat files for VMEC matrices 
 * 
 * It is only used by Flux_Surface for easy storing of these quantities.
 * 
 * 
 */
struct Flux_Surface_Settings{
    unsigned number_of_surfaces; /**<  Number of flux surfaces contained in the .dat files */
    unsigned n_tor             ; /**<  Number of toroidal harmonics present*/
    unsigned m_pol             ; /**<  Number of poloidal harmonics present*/
    unsigned symmetry          ; /**<  Symmetry of the reactor.*/

    Flux_Surface_Settings(unsigned ns, unsigned ntor, unsigned mpol, unsigned symm){
        number_of_surfaces = ns;
        n_tor = ntor;
        m_pol = mpol; 
        symmetry = symm;
    }

    Flux_Surface_Settings(const nlohmann::json& settings_json){
        number_of_surfaces = settings_json.at("Number_of_Surfaces").get<unsigned>();
        symmetry           = settings_json.at("Symmetry").get<unsigned>();
        n_tor              = settings_json.at("n_tor").get<unsigned>();
        m_pol              = settings_json.at("m_pol").get<unsigned>();
    }
    Flux_Surface_Settings(){
        number_of_surfaces = 0;
        symmetry           = 1;
        n_tor              = 0;
        m_pol              = 0;
    }

    std::string Write_str() const{
        std::stringstream os;
        os<<"Flux_Surface_Settings(\n";
        os<< this->Write_Settings();
        os<<"      )";
        return os.str();                                      
    }
    std::string Write_Settings() const{
        std::stringstream os;        
        os<<"    Surfaces: "<< number_of_surfaces<<'\n';
        os<<"    n_tor:    "<< n_tor<<'\n';
        os<<"    m_pol:    "<< m_pol<<'\n';
        os<<"    Symmetry: "<< symmetry;
        return os.str();
    }
    nlohmann::json Return_Dictionary() const{
        nlohmann::json result;
        result["Number_of_Surfaces"] = number_of_surfaces;
        result["n_tor"] = n_tor;
        result["m_pol"] = m_pol;
        result["Symmetry"] = symmetry;
        return result;
    }
};

Toroidal_Extent Half_Module(Flux_Surface_Settings settings,double min_angle);


struct Differential_Radial_Flux_Coordinate{
    Differential_Radial_Flux_Coordinate(double s, double distance_lcfs) : m_s(s), m_distance_lcfs(distance_lcfs){};
    double m_s;
    double m_distance_lcfs;

    Differential_Radial_Flux_Coordinate operator/(double factor){
        return Differential_Radial_Flux_Coordinate(m_s / factor, m_distance_lcfs / factor);
    }
    Differential_Radial_Flux_Coordinate operator*(double factor){
        return Differential_Radial_Flux_Coordinate(m_s * factor, m_distance_lcfs * factor);
    }

};

/**
 * @brief Struct to handle a radial flux coordinate, including equidistant to LCFS options.
 * 
 */
struct Radial_Flux_Coordinate{
    public: 

        /**
         * @brief Construct a new Radial_Flux_Coordinate object from a flux surface coordinate s and an equidistance to the LCFS.
         * 
         * It is checked that they make sense (i.e., no extra distance if \f$s < 1.0\f$)
         * 
         * @param s 
         * @param distance_lcfs 
         */
        Radial_Flux_Coordinate(double s, double distance_lcfs) : m_s(s), m_distance_lcfs(distance_lcfs) {if(s < 1.0 && m_distance_lcfs > 1e-5){
            throw std::invalid_argument("Trying to have a point inside the plasma ( s= "+std::to_string(s)+"<1.0" + " with a finite distance from the LCFS ("+std::to_string(distance_lcfs) +")");};
            sb_assert_message(s <= 1.0, "s > 1!");
            //Check whether distance is zero if < lcfs
            if(s < 1.0){m_distance_lcfs =0.0;}
            } 

        Radial_Flux_Coordinate operator+(const Differential_Radial_Flux_Coordinate& other){
            return Radial_Flux_Coordinate(m_s + other.m_s, m_distance_lcfs + other.m_distance_lcfs);
        }
        Differential_Radial_Flux_Coordinate operator-(const Radial_Flux_Coordinate& other){
            return Differential_Radial_Flux_Coordinate(m_s - other.m_s, m_distance_lcfs - other.m_distance_lcfs);
        }


        /**
         * @brief Function to get the flux surface coordinate \f$s\f$.
         * 
         * @return double 
         */
        double  Get_s()const{return m_s;}

        /**
         * @brief Function to set the flux surface coordinate \f$s\f$.
         * 
         * @return double 
         */
        double& Set_s(){return m_s;}

        /**
         * @brief Function to get the equidistant surface coordinate. 
         * 
         * @return double 
         */
        double  Get_distance_LCFS()const{return m_distance_lcfs;}

        /**
         * @brief Function to set the equidistant surface coordinate. 
         * 
         * @return double& 
         */
        double& Set_distance_LCFS(){return m_distance_lcfs;}
    private:
    double m_s;             // [flux surface coordinate s]
    double m_distance_lcfs; // [m]
};

/**
 * @brief Struct to safely use Flux surface coordinates with a Radial_Flux_Coordinate
 * 
 * 
 */
struct Flux_Surface_Coordinates{

    /**
     * @brief Construct a new Flux_Surface_Coordinates object.
     * 
     * @param r_in 
     * @param u_in 
     * @param v_in 
     */
    Flux_Surface_Coordinates(Radial_Flux_Coordinate r_in, double u_in, double v_in) : u(u_in), v(v_in), r(r_in){}
    
    /**
     * @brief Poloidal Coordinate
     * 
     */
    double u                 = 0;

    /**
     * @brief Toroidal coordinate
     * 
     */
    double v                 = 0;

    /**
     * @brief Radial Coordinate
     * 
     */
    Radial_Flux_Coordinate r = {0.0,0.0};

    /**
     * @brief Returns the flux surface label \f$s\f$
     * 
     * @return double 
     */
    double  Get_s()const{return r.Get_s();}

    /**
     * @brief Setter of flux surface label \f$s\f$
     * 
     * @return double&
     */
    double& Set_s()     {return r.Set_s();}

    /**
     * @brief Getter of distance from LCFS 
     * 
     * @return double 
     */
    double  Get_distance_LCFS()const{return r.Get_distance_LCFS();}

    /**
     * @brief Setter of distance from LCFS 
     * 
     * @return double&
     */
    double& Set_distance_LCFS()     {return r.Set_distance_LCFS();}
};


Flux_Surface_Coordinates Coordinates_From_Discrete_Angles(Radial_Flux_Coordinate r, unsigned u_i, unsigned v_i, unsigned N_u, unsigned N_v, const Toroidal_Extent& toroidal_extent);
Flux_Surface_Coordinates Coordinates_From_Discrete_Angles_Axis(unsigned v_i, unsigned N_v, const Toroidal_Extent& toroidal_extent);
