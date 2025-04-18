#pragma once
#include "Node.h"
#include "Vector.h"
#include <vector>
#include <array>
#include <fstream>
#include <iostream>
#include "Mesh_Tools.h"
#include <map>


/**
 * @brief Function for generating a Tetrahedron_Vertices object from files
 * 
 * @param filename_nodes 
 * @param filename_vertices 
 * @return Tetrahedron_Vertices 
 */
Tetrahedron_Vertices Tetrahedrons_From_File(std::string filename_nodes, std::string filename_vertices);


std::vector<Vector> Location_Linspace(const Vector& start,const Vector& end, unsigned samples);


std::string Triangle_To_STL(Vector v1, Vector v2, Vector v3);

void Append_To_STL(const Triangle_Vertices& triangle_vertices ,std::ofstream& ofstream, bool orientation_switch = false);

template<class Obj>
std::pair<std::vector<std::shared_ptr<Obj>>, std::vector<size_t>> Return_Unique_Shared_Ptr(const std::vector<std::shared_ptr<Obj>>& total_vector){
    std::vector<size_t> result_numbers;
    std::vector<std::shared_ptr<Obj>> unique_shared_ptr;

    std::map<const Obj*, size_t> contains_map;

    for(size_t i = 0; i <total_vector.size(); ++i){
        const auto& ptr = total_vector[i];

        if(contains_map.contains(ptr.get())){

            auto mat = contains_map[ptr.get()];
            result_numbers.push_back(mat);
        }
        else{

            size_t mat =  contains_map.size();
            result_numbers.push_back(mat);
            contains_map.insert({ptr.get(), mat});            
            unique_shared_ptr.push_back(std::shared_ptr<Obj>(ptr));
        }
    }

    return {unique_shared_ptr, result_numbers};
}