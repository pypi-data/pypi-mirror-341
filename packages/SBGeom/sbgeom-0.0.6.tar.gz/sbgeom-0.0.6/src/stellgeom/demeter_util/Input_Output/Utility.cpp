#include "Utility.h"
#include <sstream>
Tetrahedron_Vertices Tetrahedrons_From_File(std::string filename_nodes, std::string filename_vertices){
    Tetrahedron_Vertices result;

    std::ifstream Nodes_File(filename_nodes);
    std::ifstream Vertices_File(filename_vertices);
    
    double node_x, node_y, node_z;
    double vertex_0, vertex_1, vertex_2, vertex_3;
    while(Nodes_File >> node_x >> node_y>> node_z){
        //std::cout<<node_x<<", "<<node_y<<", "<<node_z<<std::endl;
        result.nodes.push_back(std::make_unique<Node>(node_x,node_y,node_z));
        
    }
    while(Vertices_File >> vertex_0 >> vertex_1 >> vertex_2 >> vertex_3){
        //std::cout<<vertex_0<<", "<<vertex_1<<", "<< vertex_2<<", "<<vertex_3<<std::endl;
        result.vertices.push_back(std::array<unsigned,4>({unsigned(vertex_0), unsigned(vertex_1), unsigned(vertex_2), unsigned(vertex_3)})); // implicit conversion from the double of the array to unsigned (could change, not needed)
    }

    

    return result;
}


std::vector<Vector> Location_Linspace(const Vector& start,const Vector& end, unsigned samples){
    std::vector<Vector> result;
    for(unsigned i=0; i < samples; i++){
        result.push_back(Vector(start+(end-start)*double(i)/double(samples-1)));
    }
    return result;
}

std::string Triangle_To_STL(Vector v1, Vector v2, Vector v3){
    std::stringstream s;
    s << std::scientific;
    s <<"facet normal "<<0.0<<" "<<0.0<<" "<<0.0<<"\n";
    s <<"\t outer loop\n";
    //s <<"\t\t vertex " << v1[0] * 100.0 <<" "<<v1[1] * 100.0<<" "<<v1[2] * 100.0<<"\n";
    //s <<"\t\t vertex " << v2[0] * 100.0 <<" "<<v2[1] * 100.0<<" "<<v2[2] * 100.0<<"\n";
    //s <<"\t\t vertex " << v3[0] * 100.0 <<" "<<v3[1] * 100.0<<" "<<v3[2] * 100.0<<"\n";
    s <<"\t\t vertex " << v1[0] <<" "<<v1[1]<<" "<<v1[2] <<"\n";
    s <<"\t\t vertex " << v2[0] <<" "<<v2[1]<<" "<<v2[2] <<"\n";
    s <<"\t\t vertex " << v3[0] <<" "<<v3[1]<<" "<<v3[2] <<"\n";
    s <<"\t endloop\n";
    s <<"endfacet\n";
    return s.str();
};

void Append_To_STL(const Triangle_Vertices& triangle_vertices ,std::ofstream& ofstream, bool orientation_switch){
    for(const auto& i : triangle_vertices.vertices){
        if(! orientation_switch){
            ofstream << Triangle_To_STL(triangle_vertices.nodes[i[0]]->m_location, triangle_vertices.nodes[i[1]]->m_location,triangle_vertices.nodes[i[2]]->m_location);
        }
        else{
            ofstream << Triangle_To_STL(triangle_vertices.nodes[i[0]]->m_location,triangle_vertices.nodes[i[2]]->m_location, triangle_vertices.nodes[i[1]]->m_location);
        }
    
    }
};