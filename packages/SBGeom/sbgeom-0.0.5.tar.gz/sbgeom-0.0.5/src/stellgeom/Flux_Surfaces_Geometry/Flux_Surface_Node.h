#pragma once
#include "Node.h"
#include "Flux_Surface_Coords.h"


class Flux_Surfaces;
/**
 * @brief Class to describe a Node that is on a Flux surface.
 * 
 */
class Flux_Surface_Node : public Node{
    public:
        /**
         * @brief Construct a new Flux_Surface_Node object from a Flux_Surface_Coordinates and the Flux_Surfaces
         * 
         * @param node_coordinates 
         * @param flux_surfaces 
         */
        Flux_Surface_Node(Flux_Surface_Coordinates node_coordinates, const Flux_Surfaces& flux_surfaces);

        /**
         * @brief Construct a new Flux_Surface_Node object from a Flux_Surface_Coordinates and real_space_coordinates
         * 
         * Can be useful if the domain is not derived from a Flux_Surfaces directly (but e.g. indirectly using UV_Manifolds from other codes)
         * 
         * @param node_coordinates 
         * @param real_space_coordinates 
         */
        Flux_Surface_Node(Flux_Surface_Coordinates node_coordinates,Vector real_space_coordinates) : Node(real_space_coordinates), m_flux_surface_coordinates(node_coordinates){}

        /**
         * @brief Construct a new Flux_Surface_Node object from another Flux_Surface_Node
         * 
         * @param other 
         */
        Flux_Surface_Node(const Flux_Surface_Node& other): Node(other.m_location), m_flux_surface_coordinates(other.m_flux_surface_coordinates){};

        /**
         * @brief Cloning to a unique_ptr.
         * 
         * @return std::unique_ptr<Node> 
         */
        std::unique_ptr<Node> Make_Unique() const override{return std::make_unique<Flux_Surface_Node>(*this); }

        /**
         * @brief Return the Flux_Surface_Coordinates of this Flux_Surface_Node.
         * 
         * @return Flux_Surface_Coordinates 
         */
        Flux_Surface_Coordinates Get_Flux_Surface_Coordinates() const{return m_flux_surface_coordinates;}

        /**
         * @brief Override of Node::Write
         * 
         */
        void Write() const override;
    protected:
        
        Flux_Surface_Coordinates m_flux_surface_coordinates;
};