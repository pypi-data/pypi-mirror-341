#pragma once
#include "Contiguous_Arrays.h"
#include "Flux_Surface_Coords.h"

#include <array>
#include "Mesh_Tools.h"

class Flux_Surfaces;

/**
 * @brief Wrapper around a flux surface axis. Construct using Flux_Surfaces::Return_V_Axis
 * 
 * The constructor using data is still public because it should be possible to initialise to
 * it using data from e.g. equi-surf. There is no checking of the validity of the data though,
 * so use only when needed and otherwise use Flux_Surfaces::Return_V_Axis
 * 
 * 
 */
class V_Axis{
    public: 
        /**
         * @brief Construct a new v axis object from raw data.
         * 
         * Uses rvalue reference to move the data (since it can become rather large and copying is unnecessary)
         * There is no checking on the validity and compatibility of the data and Toroidal_Extent
         * 
         * @param data 
         * @param toroidal_extent 
         */
        V_Axis(Array&& data, const Toroidal_Extent& toroidal_extent);

        /**
         * @brief Obtain the Flux_Surface_Coordinate from a v_i index.
         * 
         * Checking is performed if th v_i is present in the data.
         * @param v_i 
         * @return Flux_Surface_Coordinates 
         */
        Flux_Surface_Coordinates Flux_Coordinate_From_Index(unsigned v_i) const;

        /**
         * @brief Return the real coordiante from a v_i index.
         * 
         * @param v_i 
         * @return Vector 
         */
        Vector                   Real_Coordinate_From_Index(unsigned v_i) const;

        /**
         * @brief Get the maximum index of the data.
         * 
         * @return unsigned 
         */
        unsigned Get_Nv() const{return m_Nv;}
    private:
    Toroidal_Extent m_toroidal_extent;
    Array m_data;
    unsigned m_Nv;
};

/**
 * @brief Class to describe a surface characterised by poloidal and toroidal angle.
 * 
 * It is defined both in the plasma and outside the plasma through a Radial_Flux_Coordinate.
 */
class UV_Manifold{
    public:
        /**
         * @brief Construct a new uv manifold object from raw data
         * 
         * It has no checking on the validity and compatibility of the constructor arguments, since it should be 
         * possible to use an e.g. equi-surf generated surface.
         * 
         * Uses rvalue reference to avoid copying.
         * 
         * @param data 
         * @param radial_coordinate 
         * @param toroidal_extent 
         */
        UV_Manifold(Contiguous3D<double>&& data, const Radial_Flux_Coordinate& radial_coordinate, const Toroidal_Extent& toroidal_extent);

        /**
         * @brief Checks whether two UV_Manifold objects have the same data shape.
         * 
         * @param other 
         * @return true 
         * @return false 
         */
        bool Same_Shape(const UV_Manifold& other) const{return (m_Nv == other.m_Nv && m_Nu == other.m_Nu);}

        /**
         * @brief Writes out some data. 
         * 
         */
        void Write()const{
            std::cout<<" UV_Manifold with:";
            std::cout<<"\n\ts                  = "+std::to_string(m_radial_flux_coordinate.Get_s());
            std::cout<<"\n\tDistance from LCFS = "+std::to_string(m_radial_flux_coordinate.Get_distance_LCFS());
            std::cout<<"\n\tN_u                = "+std::to_string(m_Nu);
            std::cout<<"\n\tN_v                = "+std::to_string(m_Nv)<<std::endl;
        }

        /**
         * @brief Obtain the Flux_Surface_Coordinates from poloidal and toroidal indices
         * 
         * @param u_i poloidal index 
         * @param v_i toroidal index
         * @return Flux_Surface_Coordinates 
         */
        Flux_Surface_Coordinates Flux_Coordinate_From_Index(unsigned u_i, unsigned v_i) const;

        /**
         * @brief Obtain the real space coordinate from poloidal and toroidal indices
         * 
         * Checks that the indices are within bounds of the data.
         * 
         * @param u_i poloidal index
         * @param v_i toroidal indx
         * @return Vector 
         */
        Vector                   Real_Coordinate_From_Index(unsigned u_i, unsigned v_i) const;

        /**
         * @brief Gets the maximum poloidal coordinate index
         * 
         * @return unsigned 
         */
        unsigned Get_Nu()const{return m_Nu;}

        /**
         * @brief Gets the maximum toroidal coordinate index
         * 
         * @return unsigned 
         */
        unsigned Get_Nv()const{return m_Nv;}

        /**
         * @brief Gets the toroidal extent on which the data is defined.
         * 
         * @return Toroidal_Extent 
         */
        Toroidal_Extent Get_Toroidal_Extent() const {return m_toroidal_extent;}


        /**
         * @brief Meshes the surface of this UV_collection
         * 
         * @return Triangle_Vertices
         */
        Triangle_Vertices Mesh_Surface() const{
            return this->Mesh_Surface_Orientation(true);
        };

        /**
         * @brief Meshes the surface of this UV_collection
         * 
         * @return Triangle_Vertices
         */
        Triangle_Vertices Mesh_Surface_Orientation(bool normals_facing_outwards) const;
    private:
        unsigned m_Nu;
        unsigned m_Nv;        
        Radial_Flux_Coordinate m_radial_flux_coordinate;
        Contiguous3D<double> m_data;
        Toroidal_Extent m_toroidal_extent;
};

/**
 * @brief Class containing functions on a set of UV_Manifold objects
 * 
 * Most importantly, it can mesh the space between the UV_Manifold layers.
 * 
 */
class UV_Manifold_Collection{
    public:
        /**
         * @brief Construct a new uv manifold collection object from a vector of UV_Manifold objects
         * 
         * Uses rvalue reference to avoid copying and checks for compatibility
         * 
         * @param uv_manifolds_rvalues 
         */
        UV_Manifold_Collection(std::vector<UV_Manifold>&& uv_manifolds_rvalues) : m_uv_manifolds(std::move(uv_manifolds_rvalues)){
            if(m_uv_manifolds.size() < 1 ){ throw std::invalid_argument(" Trying to initialise a UV_Manifold_Collection without any manifolds.");}
            
            for(const auto& i : m_uv_manifolds){
                if(! i.Same_Shape(m_uv_manifolds[0])){
                    throw std::invalid_argument("Cannot mesh together UV_Manifolds with different shapes.");
                }
            m_Nv = m_uv_manifolds[0].Get_Nv();
            m_Nu = m_uv_manifolds[0].Get_Nu();
            m_toroidal_extent = m_uv_manifolds[0].Get_Toroidal_Extent();
            }          
        };

        /**
         * @brief Writes out information about the UV_Manifold objects
         * 
         */
        void Write() const{
            for(const auto& i : m_uv_manifolds){
                i.Write();
            }
        }


        Tetrahedron_Vertices Mesh_Tetrahedrons() const{return this->Mesh_Tetrahedrons(0);};
        /**
         * @brief Meshes the space between the UV_Manifold layers
         * 
         * Optionally provide an offset for the node indices. This can be useful for connecting different meshes sharing
         * nodes (e.g. using VMEC_Meshing_Axis).
         * Procedure for each layer: for each discrete point \f$(u_i, v_i)\f$ on the first flux surface create a hexahedron with as points (they are named as in VMEC_Meshing_axis): 
         *      |   \f$(u_i, v_i)\f$       | Type of point        | Name of vertex | 
         *      |--------------------------|----------------------|----------------|
         *      | \f$(u_i,     v_i    )\f$ |  First flux surface  |  Vertex c      |
         *      | \f$(u_i,     v_i + 1)\f$ |  First flux surface  |  Vertex d      |
         *      | \f$(u_i + 1, v_i    )\f$ |  First flux surface  |  Vertex e      |
         *      | \f$(u_i + 1, v_i + 1)\f$ |  First flux surface  |  Vertex f      |
         *      | \f$(u_i,     v_i    )\f$ |  Second flux surface |  Vertex g      |
         *      | \f$(u_i,     v_i + 1)\f$ |  Second flux surface |  Vertex h      |
         *      | \f$(u_i + 1, v_i    )\f$ |  Second flux surface |  Vertex i      |
         *      | \f$(u_i + 1, v_i + 1)\f$ |  Second flux surface |  Vertex j      |
         * 
         * They wrap around if the domain is toroidally connected (such that for the last point this \f$ u_i + 1 \f$  or \f$v_i + 1\f$ are just \f$u_i = 0\f$ and \f$v_i = 0\f$ again for both layers)
         * Therefore, we have \f$N_v\f$ tetrahedrons in the toroidal direction if it is toroidally connected and otherwise \f$N_V - 1 \f$.
         * Given \f$n \f$ layers, we have \f$n-1\f$ tetrahedrons in the layered direction. 
         * 
         * In such a hexahedron, we need six tetrahedrons to fill the volume. These are the tetrahedrons spanned by the vertices
         *     - (c, e, f, j)
         *     - (c, f, i, j)
         *     - (c, g, i, j)
         *     - (c, d, f, j)
         *     - (c, d, g, j)
         *     - (h, d, g, j)
         * 
         * These are chosen such that they connect properly to the axis-to-first-flux-surface mesh.
         * 
         * The ordering of the resulting arrays is ordered as follows:
         * 
         *  - Nodes:
         *      - For each layer:
         *          - \f$u_i = 0\f$ and all \f$ N_V\f$ \f$v_i\f$ nodes
         *          -  \f$u_i = 1\f$ and all \f$v_i\f$ nodes
         * 
         *  - Vertices:
         *      - For each layer:
         *          - \f$v_i\f$ = 0 and all \f$ N_u \f$ \f$u_i\f$ tetrahedrons
         *          - \f$v_i\f$ = 1 and all \f$ N_u \f$ \f$u_i\f$ tetrahedrons 
         *          - etc..
         * 
         * Given an index \f$i\f$ in this vertices array, we need to calculate the \f$(l_i, v_i, u_i, t_i)\f$ indices. We have \f$ 6 N_{vt} N_u \f$ elements per layer and \f$ 6 N_u \f$ elements per \f$v_i\f$ slice (
         * where \f$ N_{vt} \f$ is the amount of tetrahedron slices in the toroidal direction)
         * 
         *  - \f$ l_i = i / ( 6 N_{vt} N_u ) \f$ and index \f$j\f$ in the layer \f$l_i\f$ is \f$ i % ( 6 N_{vt} N_u ) \f$
         *  - \f$ v_i = ( j )/ ( 6 N_u)\f$ and index \f$ k\f$ in the \f$v_i\f$ slice is  \f$ j % 6 N_u \f$
         *  - \f$ u_i = k / 6\f$ 
         *  - \f$ t_i = k % 6\f$
         * 
         * Given \f$(l_i, v_i, u_i, t_i)\f$ we have \f$ i =  l_i \times 6 N_{vt} N_u + v_i \times 6 N_u + u_i \times 6 + t_i \f$
         * 
         * These formulas are offset if this is stitched together with an axis domain.      
         * 
         * @param offset 
         * @return Tetrahedron_Vertices 
         */
        Tetrahedron_Vertices Mesh_Tetrahedrons(unsigned offset) const;
    private:
        unsigned m_Nu;
        unsigned m_Nv;
        Toroidal_Extent m_toroidal_extent;
        std::vector<UV_Manifold> m_uv_manifolds;
};


/**
 * 
 * @brief Create a tetrahedron mesh of the magnetic axis and a first flux surface
 * 
 * @param flux_surfaces Flux_Surfaces object containing all information about both the magnetic axis and the first flux surface
 * @param N_u Number of poloidal angles in the surface
 * @param N_v Number of toroidal angles in the surface
 * @param toroidal_extent Toroidal_Extent object containing information about the starting and ending angles. 
 * @param s_first First flux surface it will be meshed to 
 * @return Tetrahedron_Vertices Structure containing the node locations of the mesh and an the vertices array (indicating which nodes are connected by which tetrahedron)
 * 
 * Procedure: for each discrete point \f$(u_i, v_i)\f$ on the first flux surface create a wedge with as points:
 *      |   \f$(u_i, v_i)\f$       | Type of point        | Name of vertex | 
 *      |--------------------------|----------------------|----------------|
 *      | \f$(v_i)             \f$ |  Axis                |  Vertex a      |
 *      | \f$(v_i + 1)         \f$ |  Axis                |  Vertex b      |
 *      | \f$(u_i,     v_i    )\f$ |  First flux surface  |  Vertex c      |
 *      | \f$(u_i,     v_i + 1)\f$ |  First flux surface  |  Vertex d      |
 *      | \f$(u_i + 1, v_i    )\f$ |  First flux surface  |  Vertex e      |
 *      | \f$(u_i + 1, v_i + 1)\f$ |  First flux surface  |  Vertex f      |
 * 
 * They wrap around if the domain is toroidally connected (such that for the last point this \f$ u_i + 1 \f$  or \f$v_i + 1\f$ are just \f$u_i = 0\f$ and \f$v_i = 0\f$ again)
 * Therefore, we have \f$N_v\f$ tetrahedrons in the toroidal direction if it is toroidally connected and otherwise \f$N_V - 1 \f$.
 * 
 * In such a wedge, we need three tetrahedrons to fill the volume. These are the tetrahedrons spanned by the vertices
 *     - (a, b, c, e)
 *     - (b, c, e, f)
 *     - (b, c, d, f)
 * 
 * It is important that they are consistent (such that boundaries always touch completely instead of crossing over), and this is the case with this ordering.
 *
 * The ordering of the resulting arrays is then as follows:
 * - Nodes:
 *      - \f$N_v\f$ axis points
 *      - \f$u_i = 0\f$ and all \f$ N_V\f$ \f$v_i\f$ nodes
 *      - Populate \f$u_i = 1\f$ and all \f$v_i\f$ nodes
 *      - etc...
 *
 * - Vertices:
 *      - \f$v_i = 0\f$ and all \f$N_u\f$ \f$u_i\f$ for the 3 tetrahedrons in the \f$(u_i, v_i)\f$ wedge
 *      - \f$v_i = 1\f$ and all \f$N_u\f$ \f$u_i\f$ for the 3 tetrahedrons in the \f$(u_i, v_i)\f$ wedge
 *      - etc..
 *
 * Given an index \f$ i \f$ in this vertices array (i.e. the tetrahedron number), it can be calculated that  
 * in every \f$ v_i \f$ slice, there exist \f$ 3 N_u\f$ tetrahedrons. Therefore, 
 *      - \f$v_i = i / (3 \ N_u)\f$                                   
 *          - 3 tetrahedrons per \f$(u_i, v_i)\f$ pair, \f$N_u\f$ amount of wedges per \f$v_i\f$ which implies \f$ 3 \ N_u \f$ tetrahedrons per \f$v_i\f$)
 *      - \f$u_i = (  i\  \% \ (3 \   N_u) )  / 3 \f$                        
 *          - Calculate the  index in the \f$ v_i\f$ toroidal angle element. Three tetrahedrons per \f$(u_i, v_i)\f$ wedge, thus divide by 3.
 *      - tetrahedron number in wedge =  \f$t_i =  (i\  \% \ (3 \  N_u) ) \ \% \ 3 \f$
 * 
 * The other way around, given an \f$(u_i, v_i, t_i)\f$ the index can be calculated as \f$i = 3\ N_u\ v_i + 3 \ u_i + \text{tetrahedron_number}\f$
 * 
 */
Tetrahedron_Vertices VMEC_Meshing_axis(const Flux_Surfaces& flux_surfaces, unsigned N_u, unsigned N_v, const Toroidal_Extent& toroidal_extent, Radial_Flux_Coordinate s_first);

Tetrahedron_Vertices Mesh_Tetrahedron_Flux_Surfaces(const Flux_Surfaces& fs, DynamicVector s, DynamicVector d, unsigned Nv, unsigned Nu, Toroidal_Extent toroidal_extent);
Mesh Mesh_Tiled_Surface(const Flux_Surfaces& self, double s, double d, unsigned N_tiles_v, unsigned N_tiles_u, double tile_spacing, double tor_min, double tor_max);
Mesh Mesh_Detailed_Tiled_Surface(const Flux_Surfaces& self, double s, double d, unsigned N_lines_v, unsigned N_lines_u, double tile_spacing, double normal_in, double tor_min, double tor_max);