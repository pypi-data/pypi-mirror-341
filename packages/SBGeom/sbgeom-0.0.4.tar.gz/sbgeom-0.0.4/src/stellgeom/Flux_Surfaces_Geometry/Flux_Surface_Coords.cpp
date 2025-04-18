#include "Flux_Surface_Coords.h"

Toroidal_Extent Half_Module(Flux_Surface_Settings settings,double min_angle){
    return Toroidal_Extent(min_angle, min_angle + 2.0 * Constants::pi / ( 2.0 * settings.symmetry) );
}

Flux_Surface_Coordinates Coordinates_From_Discrete_Angles(Radial_Flux_Coordinate r, unsigned u_i, unsigned v_i, unsigned N_u, unsigned N_v, const Toroidal_Extent& toroidal_extent){
    
    auto N_v_corrected = toroidal_extent.Full_Angle() ? N_v : N_v - 1;

    double u = double(u_i) / double(N_u) * 2.0 * Constants::pi; 
    
    double v = double(v_i) / double(N_v_corrected ) * (toroidal_extent.max() - toroidal_extent.min())  + toroidal_extent.min(); 

    return Flux_Surface_Coordinates(r,u,v);
}

Flux_Surface_Coordinates Coordinates_From_Discrete_Angles_Axis(unsigned v_i, unsigned N_v, const Toroidal_Extent& toroidal_extent){
    return Coordinates_From_Discrete_Angles(Radial_Flux_Coordinate(0.0,0.0), 0, v_i, 1, N_v, toroidal_extent);
}
