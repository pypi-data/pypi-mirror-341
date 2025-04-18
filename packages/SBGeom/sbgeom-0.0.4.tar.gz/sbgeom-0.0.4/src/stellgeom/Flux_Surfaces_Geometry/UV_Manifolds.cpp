#include "UV_Manifolds.h"
#include "Flux_Surface_Node.h"
#include "Flux_Surfaces.h"
V_Axis::V_Axis(Array&& data, const Toroidal_Extent& toroidal_extent) : m_toroidal_extent(toroidal_extent), m_data(std::move(data)){
    m_Nv = m_data.rows();
};
Flux_Surface_Coordinates V_Axis::Flux_Coordinate_From_Index(unsigned v_i) const{
    if(v_i >= m_Nv){throw std::invalid_argument("Too large v_i="+std::to_string(v_i)+" compared to"+\
                                 " N_v=" + std::to_string(m_Nv)+" in V_Axis::Flux_Coordinate_From_Index");}  
    return Coordinates_From_Discrete_Angles_Axis(v_i,m_Nv, m_toroidal_extent);
};
Vector                   V_Axis::Real_Coordinate_From_Index(unsigned v_i) const{
    if(v_i >= m_Nv){throw std::invalid_argument("Too large v_i="+std::to_string(v_i)+" compared to"+\
                                 " N_v=" + std::to_string(m_Nv)+" in V_Axis::Real_Coordinate_From_Index");}  
    Vector result; 
    result[0] = m_data(v_i, 0);
    result[1] = m_data(v_i, 1);
    result[2] = m_data(v_i, 2);
    return result;
};

UV_Manifold::UV_Manifold(Contiguous3D<double>&& data, const Radial_Flux_Coordinate& radial_coordinate, const Toroidal_Extent& toroidal_extent) : m_radial_flux_coordinate(radial_coordinate), m_data(std::move(data)), m_toroidal_extent(toroidal_extent){
    m_Nu = m_data.Number_of_First_Index();
    m_Nv = m_data.Number_of_Second_Index();
};
Flux_Surface_Coordinates UV_Manifold::Flux_Coordinate_From_Index(unsigned u_i, unsigned v_i)const{
    if(u_i >= m_Nu || v_i >= m_Nv){throw std::invalid_argument("Too large u_i="+std::to_string(u_i)+"v_i="+std::to_string(v_i)+" compared to"+\
                                 "N_u=" + std::to_string(m_Nu) + "N_v=" + std::to_string(m_Nv)+" in UV_Manifold::Flux_Coordinate_From_Index");}    
    return Coordinates_From_Discrete_Angles(m_radial_flux_coordinate,u_i,v_i, m_Nu, m_Nv, m_toroidal_extent);
};


Vector UV_Manifold:: Real_Coordinate_From_Index(unsigned u_i, unsigned v_i)const{
    if(u_i >= m_Nu || v_i >= m_Nv){throw std::invalid_argument("Too large u_i="+std::to_string(u_i)+"v_i="+std::to_string(v_i)+" compared to"+\
                                 "N_u=" + std::to_string(m_Nu) + "N_v=" + std::to_string(m_Nv)+" in UV_Manifold::Real_Coordinate_From_Index");}
    Vector result;
    result[0] = m_data(u_i, v_i, 0);
    result[1] = m_data(u_i, v_i, 1);
    result[2] = m_data(u_i, v_i, 2);
    return result;
};


Tetrahedron_Vertices UV_Manifold_Collection::Mesh_Tetrahedrons(unsigned offset) const{
    Tetrahedron_Vertices result;
    if(m_uv_manifolds.size()< 2){
        throw std::invalid_argument(" Cannot construct a Tetrahedronic mesh from a UV_Manifold collection with only 1 manifold.");
    }
    // std::cout<<"\nConstructing a ";
    // if(m_toroidal_extent.Full_Angle()){std::cout<<"toroidally connected";}else{std::cout<<"toroidally disconnected";}std::cout<<" UV_Manifold collection using:\n";
    // m_toroidal_extent.Write();
    

    unsigned number_of_element_layers = m_uv_manifolds.size() - 1 ;
    unsigned number_of_flux_layers    = m_uv_manifolds.size();
    auto N_u = m_Nu;
    auto N_v = m_Nv;

    for(unsigned layer = 0; layer < number_of_flux_layers; ++layer){
         for(unsigned u_i = 0 ; u_i < N_u; u_i++){
            for(unsigned v_i = 0 ; v_i < N_v; v_i++){
                Flux_Surface_Coordinates surface_i_flux = m_uv_manifolds[layer].Flux_Coordinate_From_Index(u_i, v_i);
                Vector                   surface_i_real = m_uv_manifolds[layer].Real_Coordinate_From_Index(u_i, v_i);
                result.nodes.push_back(std::make_unique<Flux_Surface_Node>(surface_i_flux, surface_i_real));
           }
        }
    }    

    auto index_in_nodes = [N_v, N_u, offset](unsigned u_i, unsigned v_i, unsigned layer){
        

        return u_i * N_v + v_i + N_v * N_u * layer + offset;
    };

    //If we have a toroidally connected mesh, we have N_v tetrahedrons in the toroidal direction. Else N_v -1
    unsigned N_v_connected = (m_toroidal_extent.Full_Angle()) ? N_v :  N_v - 1; 

    for(unsigned layer =0; layer < number_of_element_layers; ++layer){

        unsigned node_layer_start = layer * 6 * N_u * N_v ; // first index of a *node* in the current layer)

        for(unsigned v_i = 0; v_i < N_v_connected; ++v_i){
        
            for(unsigned u_i = 0; u_i < N_u; ++u_i){
                unsigned first_u_i   =   u_i;
                unsigned second_u_i  = ( u_i + 1 )%N_u;

                unsigned first_v_i   =   v_i;
                unsigned second_v_i  = ( v_i + 1 )%N_v;

                unsigned vertex_c = index_in_nodes(first_u_i, first_v_i, layer );
                unsigned vertex_d = index_in_nodes(first_u_i, second_v_i, layer);

                unsigned vertex_e = index_in_nodes(second_u_i, first_v_i,layer);       
                unsigned vertex_f = index_in_nodes(second_u_i, second_v_i,layer);

                unsigned vertex_g = index_in_nodes(first_u_i, first_v_i, layer  + 1);
                unsigned vertex_h = index_in_nodes(first_u_i, second_v_i, layer + 1);

                unsigned vertex_i = index_in_nodes(second_u_i, first_v_i, layer + 1);       
                unsigned vertex_j = index_in_nodes(second_u_i, second_v_i,layer + 1);

                result.vertices.push_back(std::array<unsigned,4>({vertex_c, vertex_e, vertex_f, vertex_i}));
                result.vertices.push_back(std::array<unsigned,4>({vertex_c, vertex_f, vertex_i, vertex_j}));
                result.vertices.push_back(std::array<unsigned,4>({vertex_c, vertex_g, vertex_j, vertex_i}));
                result.vertices.push_back(std::array<unsigned,4>({vertex_c, vertex_d, vertex_f, vertex_j}));
                result.vertices.push_back(std::array<unsigned,4>({vertex_c, vertex_d, vertex_g, vertex_j}));
                result.vertices.push_back(std::array<unsigned,4>({vertex_h, vertex_d, vertex_g, vertex_j}));
            }
        }
         
    }
    return result;

};

Triangle_Vertices UV_Manifold::Mesh_Surface_Orientation(bool normals_facing_outwards)const{
    Triangle_Vertices result;

    auto Nu = this->Get_Nu();
    auto Nv = this->Get_Nv();
    Toroidal_Extent tor_extent = this->Get_Toroidal_Extent();

    auto v_blocks = tor_extent.Full_Angle() ? Nv : Nv - 1;
    auto u_blocks = Nu;
    auto total_vertex_points = Nu * Nv;
    auto vertex_values = total_vertex_points * 3;
	
    auto total_blocks =  u_blocks * v_blocks;

    for(unsigned u_i = 0; u_i < Nu; ++u_i){
        for(unsigned v_i = 0 ; v_i < Nv; ++v_i){
            result.nodes.push_back(std::make_unique<Flux_Surface_Node>(this->Flux_Coordinate_From_Index(u_i,v_i), this->Real_Coordinate_From_Index(u_i,v_i)));            
        }
    }
    auto uv_index = [Nv](unsigned u_i, unsigned v_i){
        return u_i * Nv + v_i;
    };
    
    for(unsigned u_i_block = 0; u_i_block < u_blocks; ++u_i_block){
        for(unsigned v_i_block = 0; v_i_block < v_blocks; ++v_i_block){

            unsigned bottom_left_u_i  = u_i_block;
			unsigned bottom_left_v_i  = v_i_block;

			unsigned bottom_right_u_i = u_i_block; 
			unsigned bottom_right_v_i = (v_i_block + 1) % Nv;

			unsigned top_left_u_i     = (u_i_block + 1) % Nu;
			unsigned top_left_v_i     = v_i_block;

			unsigned top_right_u_i    = (u_i_block + 1) % Nu;
			unsigned top_right_v_i    = (v_i_block + 1) % Nv;
            // Normal  is P_{21} x P_{31}
            if(normals_facing_outwards){
            result.vertices.push_back(std::array<unsigned,3>({uv_index(bottom_left_u_i, bottom_left_v_i),  \
                                                              uv_index(bottom_right_u_i, bottom_right_v_i),\
                                                              uv_index(top_left_u_i, top_left_v_i)}));
            result.vertices.push_back(std::array<unsigned,3>({uv_index(bottom_right_u_i, bottom_right_v_i),\
                                                              uv_index(top_right_u_i, top_right_v_i),      \
                                                              uv_index(top_left_u_i, top_left_v_i)}));
            }
            else{
            result.vertices.push_back(std::array<unsigned,3>({uv_index(bottom_right_u_i, bottom_right_v_i),\
                                                              uv_index(bottom_left_u_i, bottom_left_v_i),  \
                                                              uv_index(top_left_u_i, top_left_v_i)}));
            result.vertices.push_back(std::array<unsigned,3>({uv_index(top_right_u_i, top_right_v_i),      \
                                                              uv_index(bottom_right_u_i, bottom_right_v_i),\
                                                              uv_index(top_left_u_i, top_left_v_i)}));
            }

        }        
    }
    return result;
}

//We make the *choice* that N_v does *not* indicate the number of tetrahedrons  but the number of *nodes* in toroidal direction
Tetrahedron_Vertices VMEC_Meshing_axis(const Flux_Surfaces& flux_surfaces, unsigned N_u, unsigned N_v, const Toroidal_Extent& toroidal_extent, Radial_Flux_Coordinate r_first){
    Tetrahedron_Vertices result;
    
    bool toroidally_connected = toroidal_extent.Full_Angle();
    
    // std::cout<<std::endl<<"Constructing a ";
    // if(toroidally_connected){std::cout<<"toroidally connected";}else{std::cout<<"toroidally disconnected";}std::cout<<" axis to flux surface s= "<<r_first.Get_s()<<" distance="<<r_first.Get_distance_LCFS()<< " grid, "<<std::endl;
    // std::cout<<" with N_u = "<<N_u << " and N_v = "<<N_v<<std::endl;
    
    auto index_in_nodes = [N_v](unsigned u_i, unsigned v_i){
        return N_v + u_i * N_v + v_i;
    };
    
    //First add the axis, then the flux surface
    for(unsigned v_i = 0; v_i < N_v; ++v_i ){
        Flux_Surface_Coordinates axis_i = Coordinates_From_Discrete_Angles_Axis(v_i, N_v, toroidal_extent);
        result.nodes.push_back(std::make_unique<Flux_Surface_Node>(axis_i, flux_surfaces));
    }
    for(unsigned u_i = 0 ; u_i < N_u; u_i++){
        for(unsigned v_i = 0 ; v_i < N_v; v_i++){
            Flux_Surface_Coordinates flux_coord_i = Coordinates_From_Discrete_Angles(r_first, u_i, v_i, N_u, N_v, toroidal_extent);
            result.nodes.push_back(std::make_unique<Flux_Surface_Node>(flux_coord_i, flux_surfaces));
        }
    }

    //If we have a toroidally connected mesh, we have N_v tetrahedrons. Else N_v -1
    unsigned N_v_connected = (toroidally_connected) ? N_v :  N_v - 1; 
    for(unsigned v_i = 0; v_i < N_v_connected; v_i++){
        for(unsigned u_i = 0; u_i < N_u; u_i++){
            unsigned first_u_i   = u_i;
            unsigned second_u_i  = ( u_i + 1 )%N_u;
            unsigned first_v_i   = v_i;
            unsigned second_v_i  = ( v_i + 1 )%N_v;
            
            unsigned vertex_a = first_v_i;
            unsigned vertex_b = second_v_i;                                     // Axis point at v_i
            
            unsigned vertex_c = index_in_nodes(first_u_i, first_v_i);
            unsigned vertex_d = index_in_nodes(first_u_i, second_v_i);
            
            unsigned vertex_e = index_in_nodes(second_u_i, first_v_i);       // Axis point at v_i + 1
            unsigned vertex_f = index_in_nodes(second_u_i, second_v_i);

            
            result.vertices.push_back(std::array<unsigned,4>({vertex_a, vertex_b, vertex_c, vertex_e}));

            result.vertices.push_back(std::array<unsigned,4>({vertex_b,vertex_c, vertex_e, vertex_f }));

            result.vertices.push_back(std::array<unsigned,4>({vertex_b, vertex_c, vertex_d, vertex_f}));

        }

    }
  return result;

}

Tetrahedron_Vertices Mesh_Tetrahedron_Flux_Surfaces(const Flux_Surfaces& fs, DynamicVector s, DynamicVector d, unsigned Nv, unsigned Nu, Toroidal_Extent toroidal_extent){
      Tetrahedron_Vertices result;      
      bool includes_axis = s[0] == 0.0;
      std::vector<Radial_Flux_Coordinate> flux_to_flux_layers;;
      unsigned flux_to_flux_node_offset     = 0;
      unsigned flux_to_flux_vertices_offset = 0;
      if(d.rows() != s.rows()){
        throw std::invalid_argument("Trying to mesh with different sized s and d vectors...");
      }
      for(unsigned i =0 ; i < d.rows(); ++i){
         flux_to_flux_layers.push_back({s[i], d[i]});
      }

      if(includes_axis){
         
         result = VMEC_Meshing_axis(fs, Nu, Nv, toroidal_extent, {s[1], d[1]});
         flux_to_flux_layers.erase(flux_to_flux_layers.begin());
         flux_to_flux_node_offset = Nv * Nu; // The first flux_to_flux layer is already here so no need to add those nodes again. This offset takes care of that.
         flux_to_flux_vertices_offset = Nv;     // The axis points are not used in the UV_Manifold_Collection::Mesh_Tetrahedrons, so all vertex indices need to be moved by this number.
      }
      
      std::vector<UV_Manifold> flux_layers;

      for(auto& r : flux_to_flux_layers){
          flux_layers.push_back(fs.Return_UV_Manifold(r,Nu, Nv,toroidal_extent));
      }
      auto uv_manifold_layers = UV_Manifold_Collection(std::move(flux_layers));

      auto flux_to_flux_mesh  = uv_manifold_layers.Mesh_Tetrahedrons(flux_to_flux_vertices_offset);

      for(unsigned node_i= flux_to_flux_node_offset; node_i < flux_to_flux_mesh.nodes.size(); ++node_i){
          result.nodes.push_back(flux_to_flux_mesh.nodes[node_i]->Make_Unique());
      }

      for(auto& vertex_i : flux_to_flux_mesh.vertices){
        result.vertices.push_back(vertex_i);
      }
      
      return result;
   }
   Mesh Mesh_Tiled_Surface(const Flux_Surfaces& self, double s, double d, unsigned N_tiles_v, unsigned N_tiles_u, double tile_spacing, double tor_min, double tor_max){
    auto tor_extent = Toroidal_Extent(tor_min, tor_max);
    auto edge_points = self.Return_UV_Manifold({s,d},N_tiles_u, N_tiles_v, {tor_min, tor_max});
    unsigned no_u_tiles = N_tiles_u;
    unsigned no_v_tiles = tor_extent.Full_Angle() ? N_tiles_v : N_tiles_v - 1;

    auto result_mesh = Triangle_Vertices();
    
    for(unsigned v_i = 0; v_i < no_v_tiles; ++v_i){
        for(unsigned u_i = 0; u_i < no_u_tiles; ++u_i){
            
            auto line_u0_v0 = edge_points.Real_Coordinate_From_Index(u_i,v_i);
            auto line_u1_v0 = edge_points.Real_Coordinate_From_Index( (u_i + 1) % no_u_tiles, v_i);
            auto line_u0_v1 = edge_points.Real_Coordinate_From_Index( u_i , (v_i + 1 ) % N_tiles_v);
            auto line_u1_v1 = edge_points.Real_Coordinate_From_Index( (u_i + 1) % no_u_tiles, (v_i + 1 ) % N_tiles_v);
            auto centre_point = (line_u0_v0 + line_u0_v1 + line_u1_v0 + line_u1_v1) / 4.0;            

            auto l00 = centre_point + tile_spacing * (line_u0_v0 - centre_point);
            auto l01 = centre_point + tile_spacing * (line_u0_v1 - centre_point);
            auto l10 = centre_point + tile_spacing * (line_u1_v0 - centre_point);
            auto l11 = centre_point + tile_spacing * (line_u1_v1 - centre_point);

            result_mesh.nodes.push_back(std::make_unique<Node>(l00));
            result_mesh.nodes.push_back(std::make_unique<Node>(l01));
            result_mesh.nodes.push_back(std::make_unique<Node>(l10));
            result_mesh.nodes.push_back(std::make_unique<Node>(l11));
            
            unsigned start_index = 4 * (v_i * no_u_tiles  + u_i);
            
            result_mesh.vertices.push_back({start_index, start_index + 1, start_index + 2});            
            result_mesh.vertices.push_back({start_index + 2, start_index + 1, start_index + 3});
        }
    }
    return Mesh(result_mesh);
}

Mesh Mesh_Detailed_Tiled_Surface(const Flux_Surfaces& self, double s, double d, unsigned N_lines_v, unsigned N_lines_u, double tile_spacing, double normal_in, double tor_min, double tor_max){
    auto tor_extent = Toroidal_Extent(tor_min, tor_max);
    auto result_mesh = Triangle_Vertices();

    auto edge_points = self.Return_UV_Manifold({s,d}, N_lines_u, N_lines_v, tor_extent);

    unsigned no_u_tiles = N_lines_u;
    unsigned no_v_tiles = tor_extent.Full_Angle() ? N_lines_v : N_lines_v - 1;



    for(unsigned v_i = 0; v_i < no_v_tiles; ++v_i){
        for(unsigned u_i = 0; u_i < no_u_tiles; ++u_i){
            auto line_u0_v0 = edge_points.Real_Coordinate_From_Index(u_i,v_i);
            auto line_u1_v0 = edge_points.Real_Coordinate_From_Index( (u_i + 1) % no_u_tiles, v_i);
            auto line_u0_v1 = edge_points.Real_Coordinate_From_Index( u_i , (v_i + 1 ) % N_lines_v);
            auto line_u1_v1 = edge_points.Real_Coordinate_From_Index( (u_i + 1) % no_u_tiles, (v_i + 1 ) % N_lines_v);

            auto centre_point = (line_u0_v0 + line_u0_v1 + line_u1_v0 + line_u1_v1) / 4.0;            
            auto normal = Unit_Vector((line_u0_v0 - centre_point).cross(line_u1_v0 - centre_point));            

            auto l00 = centre_point + tile_spacing * (line_u0_v0 - centre_point) + normal * normal_in;
            auto l01 = centre_point + tile_spacing * (line_u0_v1 - centre_point) + normal * normal_in;
            auto l10 = centre_point + tile_spacing * (line_u1_v0 - centre_point) + normal * normal_in;
            auto l11 = centre_point + tile_spacing * (line_u1_v1 - centre_point) + normal * normal_in;

            unsigned start_index = 4 * (v_i * no_u_tiles  + u_i);

            result_mesh.nodes.push_back(std::make_unique<Node>(l00));
            result_mesh.nodes.push_back(std::make_unique<Node>(l01));
            result_mesh.nodes.push_back(std::make_unique<Node>(l10));
            result_mesh.nodes.push_back(std::make_unique<Node>(l11));

            result_mesh.vertices.push_back({start_index, start_index + 2, start_index + 1});            
            result_mesh.vertices.push_back({start_index + 2, start_index + 3, start_index + 1});

            unsigned start_central_points = 4 * (no_v_tiles * no_u_tiles);
            
            unsigned i_u0v0 = start_central_points + v_i * no_u_tiles + u_i;
            unsigned i_u1v0 = start_central_points + v_i * no_u_tiles + (u_i +1)%no_u_tiles;
            unsigned i_u0v1 = start_central_points + ((v_i + 1)% N_lines_v) * no_u_tiles + u_i;
            unsigned i_u1v1 = start_central_points + ((v_i + 1)% N_lines_v) * no_u_tiles + (u_i +1)%no_u_tiles;

            result_mesh.vertices.push_back({start_index,  i_u0v0, i_u1v0});
            result_mesh.vertices.push_back({start_index,start_index + 1, i_u0v1 }); // l01 

            result_mesh.vertices.push_back({start_index + 1, i_u1v1, i_u0v1}); // l01 
            result_mesh.vertices.push_back({start_index + 1, start_index + 3, i_u1v1}); // l01 

            result_mesh.vertices.push_back({start_index + 3, i_u1v0, i_u1v1}); // l01 
            result_mesh.vertices.push_back({start_index + 3, start_index + 2, i_u1v0}); // l01 

            result_mesh.vertices.push_back({start_index, i_u0v1, i_u0v0});
            result_mesh.vertices.push_back({start_index, i_u1v0, start_index + 2 }); // l01 


        }
    }
    
    for(unsigned i = 0; i < N_lines_v; ++i){
        for(unsigned j = 0; j < N_lines_u; ++j){
            result_mesh.nodes.push_back(std::make_unique<Node>(edge_points.Real_Coordinate_From_Index(j,i)));
        }
    }


    return Mesh(result_mesh);
}