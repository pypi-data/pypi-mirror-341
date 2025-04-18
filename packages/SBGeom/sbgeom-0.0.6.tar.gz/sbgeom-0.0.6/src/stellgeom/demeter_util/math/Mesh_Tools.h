#pragma once
#include "Node.h"
#include <vector>
#include <array>

/**
 * @brief Struct for importing a tetrahedron domain from somewhere
 * 
 */
struct Tetrahedron_Vertices
{   public:
    /**
     * @brief Node vector containing all physical nodes
     * 
     */
    std::vector<std::unique_ptr<Node>> nodes;

    /**
     * @brief vector of arrays with four unsigned numbers connecting the Nodes
     * 
     */
    std::vector<std::array<unsigned,4>> vertices;
    private:
};

/**
 * @brief Struct for a triangular mesh
 * 
 * Only really used for meshing .stl files.
 * 
 */
struct Triangle_Vertices
{   public:
    /**
     * @brief Node vector containing all physical nodes
     * 
     */
    std::vector<std::unique_ptr<Node>> nodes;

    /**
     * @brief vector of arrays with four unsigned numbers connecting the Nodes
     * 
     */
    std::vector<std::array<unsigned,3>> vertices;
    private:
};

template<unsigned N>
UnsignedArray vec_to_uarray(const std::vector<std::array<unsigned, N>>& vec_in){
    auto result = UnsignedArray(vec_in.size(), N);
    for(unsigned i = 0; i < vec_in.size(); ++i){
        for(unsigned j=0; j < N; ++j){                    
            result(i,j) = vec_in[i][j];
        }        
    }    
    return result;
}

Array Nodes_to_array(const std::vector<std::unique_ptr<Node>>& v_in);

std::pair<VectorArray, UnsignedVectorArray> Triangle_Vertices_to_Numeric(const Triangle_Vertices& t_in);



struct Mesh{
    Mesh(const Triangle_Vertices& t_v_in) : positions(Nodes_to_array(t_v_in.nodes)), vertices(vec_to_uarray<3>(t_v_in.vertices)) {}
    Mesh(const Tetrahedron_Vertices& t_v_in) : positions(Nodes_to_array(t_v_in.nodes)), vertices(vec_to_uarray<4>(t_v_in.vertices)) {}
    Array positions_v() const{return positions;}
    void set_positions(const Array& array){positions = array;}
    UnsignedArray vertices_v() const{return vertices;}
    void set_vertices(const UnsignedArray& array){vertices = array;}

    std::string Write_str() const{
        std::stringstream os;
        os << "Mesh( " << positions.rows()<<" points, "<<vertices.rows();
        if(vertices.cols() == 1){
            os << " point elements";
        }
        else if(vertices.cols() == 2){
            os << " line elements";
        }
        else if(vertices.cols() == 3){
            os << " triangle elements";
        }
        else if(vertices.cols() == 4){
            os << " tetrahedron elements";
        }
        else{
            os <<" elements with "<< vertices.cols() << " nodes each";
        }
        os <<")";
        return os.str();
    }

    Array positions;
    UnsignedArray vertices;
};


Mesh Mesh_From_Triangle_Vertices_Vector(const std::vector<Triangle_Vertices>& tvec_in);