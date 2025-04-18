#include "Mesh_Tools.h"

Array Nodes_to_array(const std::vector<std::unique_ptr<Node>>& v_in){
    auto result = Array(v_in.size(), 3);
    for(unsigned i = 0; i < v_in.size(); ++i){
        for(unsigned j = 0; j < 3; ++j){
            result(i,j) = v_in[i]->m_location[j];
        }
    }
    return result;
}

Mesh Mesh_From_Triangle_Vertices_Vector(const std::vector<Triangle_Vertices>& tvec_in){
    auto result = Triangle_Vertices();
    unsigned offset = 0;
    for(auto& tv  : tvec_in){
        for(auto& pos : tv.nodes){
            result.nodes.push_back(pos->Make_Unique());
        }
        for(auto& vert : tv.vertices){
            result.vertices.push_back({vert[0] + offset, vert[1] + offset, vert[2] + offset});
        }
        offset += tv.nodes.size();
    }
    return Mesh(result);
}

std::pair<VectorArray, UnsignedVectorArray> Triangle_Vertices_to_Numeric(const Triangle_Vertices& t_in){
    std::pair<VectorArray, UnsignedVectorArray> result;

    result.first = VectorArray(t_in.nodes.size(), 3);
    for(unsigned i = 0; i < t_in.nodes.size(); ++i){
        for(unsigned j = 0; j < 3; ++j){
            result.first(i,j) = t_in.nodes[i]->m_location[j];
        }
    }

    result.second = UnsignedVectorArray(t_in.vertices.size(), 3);
    for(unsigned i = 0; i < t_in.vertices.size(); ++i){
        for(unsigned j = 0; j < 3; ++j){
            result.second(i,j) = t_in.vertices[i][j];
        }
    }
    

    return result;

};