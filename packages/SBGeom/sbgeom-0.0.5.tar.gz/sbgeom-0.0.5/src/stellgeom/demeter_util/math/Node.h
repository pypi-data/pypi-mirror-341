#pragma once
#include "Vector.h"
#include <memory>
#include <iostream>
#include "Matrix.h"
#include "cmath"
#include <unordered_map>

void print_tabs(unsigned number_of_tabs);

bool approx_float_sb(double d_1, double d_2);


/**
 * @brief Class for a node of a tetrahedron
 * 
 * It provides a way to check whether two nodes are the same or reflected in the case of Stellarator Symmetry
 *
 */
class Node{
    public:

    /**
     * @brief Construct a new Node object from a Vector
     * 
     * @param location 
     */
    Node(Vector location) : m_location(location){};

    /**
     * @brief Construct a new Node object from X,Y,Z data.
     * 
     * @param x 
     * @param y 
     * @param z 
     */
    Node(double x, double y, double z) : m_location(x,y,z){};

    /**
     * @brief Write information about this Node
     * 
     */
    virtual void Write() const;
    
    /**
     * @brief Function for checking if two nodes are the same
     * 
     * The nodes are compared through their address; this assumes the nodes 
     * both come from some where else (i.e., a Tetrahedron_Domain).
     * 
     * @param node_2 The other Node
     * @return true if the nodes are the same physical node
     * @return false if the nodes are not the same physical node
     */
    bool operator==(const Node& node_2) const{ return this == &node_2; }

    /**
     * @brief Function for checking if two nodes correspond to the same physical location
     * 
     * Since they are generated in exactly the same FP operations, FP errors will be the same and therefore this works 
     * by directly comparing the floating point values (no epsilon involved)
     * 
     * @param node_2 
     * @return true 
     * @return false 
     */
    bool Same_Physical_Node(const Node& node_2 ) const { return this->m_location[0] == node_2.m_location[0] && this->m_location[1] == node_2.m_location[1]&& this->m_location[2] == node_2.m_location[2];}    
    

    /**
     * @brief Function for checking if two nodes correspond to a node reflected in the Z=0 plane
     * 
     * Not exactly the same FP calculations so have to use an epsilon type comparison here.
     * 
     * @param node_2 
     * @return true 
     * @return false 
     */
    bool Same_Physical_Node_Ref_Z(const Node& node_2) const{return approx_float_sb(this->m_location[0],node_2.m_location[0]) && approx_float_sb(this->m_location[1], node_2.m_location[1] ) && approx_float_sb( this->m_location[2],- node_2.m_location[2] ) ;}

    /**
     * @brief Cloning function to a unique_ptr.
     * 
     * @return std::unique_ptr<Node> 
     */
    virtual std::unique_ptr<Node> Make_Unique() const{return std::make_unique<Node>(m_location);}

    virtual ~Node(){}

    /**
     * @brief The location of this node in Cartesian coordinates.
     * 
     */
    Vector m_location;

    private:    
};



