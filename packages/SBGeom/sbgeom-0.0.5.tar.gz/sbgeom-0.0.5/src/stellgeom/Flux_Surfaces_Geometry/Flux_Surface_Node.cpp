#include "Flux_Surface_Node.h"
#include "Flux_Surfaces.h"

Flux_Surface_Node::Flux_Surface_Node(Flux_Surface_Coordinates node_coordinates, const Flux_Surfaces& flux_surfaces) : Node(flux_surfaces.Return_Position(node_coordinates)), m_flux_surface_coordinates(node_coordinates) {

};

void Flux_Surface_Node::Write() const{
   std::cout<<"Node at "<<this<<": fs_coords [";
    printf("% .5f,",m_flux_surface_coordinates.Get_s());
    printf("% .5f,",m_flux_surface_coordinates.Get_distance_LCFS());
    printf("% .5f,",m_flux_surface_coordinates.u);
    printf("% .5f ",m_flux_surface_coordinates.v);

    std::cout<<"] \t xyz: [";
    printf("% .5f,",m_location[0]);
    printf("% .5f,",m_location[1]);
    printf("% .5f",m_location[2]);
    std::cout<<"]";

    std::cout<<"\t RZp: [";
    printf("% .5f,",sqrt(m_location[0] * m_location[0]+ m_location[1] * m_location[1]));
    printf("% .5f,",m_location[2]);
    printf("% .5f",atan2(m_location[1], m_location[0]));
    std::cout<<"]";
    std::cout<<std::endl;
    
}