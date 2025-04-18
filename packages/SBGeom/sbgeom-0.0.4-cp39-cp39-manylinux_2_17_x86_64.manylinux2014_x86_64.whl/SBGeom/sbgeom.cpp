#include <nanobind/nanobind.h>
#include <nanobind/eigen/dense.h>
#include "Conversion_Tools.h"
#include <string>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/shared_ptr.h>
#include <nanobind/stl/unique_ptr.h>
#include <nanobind/make_iterator.h>
#include <nanobind/stl/string.h>

#include "nanobind_to_json.h"
#include "Flux_Surfaces.h"
#include "Flux_Surfaces_Extended.h"
#include "Coils.h"
#include "Mesh_Tools.h"
#include "Flux_Surfaces_Initialisation.h"
namespace nb = nanobind;
using namespace nb::literals;


NB_MODULE(sbgeom_cpp, m) {
    nb::class_<Mesh>(m, "Mesh")
        .def("positions", &Mesh::positions_v)
        .def("vertices", &Mesh::vertices_v)
        .def("__repr__", [](const Mesh& self){
            return self.Write_str();
        });

    nb::class_<Flux_Surface_Settings>(m, "Flux_Surface_Settings")
        .def(nb::init<unsigned, unsigned, unsigned,unsigned>(),  "Number_of_Surfaces"_a, "n_tor"_a, "m_pol"_a, "Symmetry"_a)
        .def_ro("number_of_surfaces", &Flux_Surface_Settings::number_of_surfaces)
        .def_ro("n_tor", &Flux_Surface_Settings::n_tor)
        .def_ro("m_pol", &Flux_Surface_Settings::m_pol)        
        .def_ro("symmetry", &Flux_Surface_Settings::symmetry)
        .def("__repr__", &Flux_Surface_Settings::Write_str);

    nb::class_<Flux_Surfaces>(m, "Flux_Surfaces")
        .def(nb::new_([](const Array& rmnc, const Array& zmns, Flux_Surface_Settings settings){return std::make_unique<Flux_Surfaces>(rmnc,zmns,settings);}), "R_mnc"_a, "Z_mns"_a, "Flux_Surface_Settings"_a)
        .def(nb::new_([](const nb::dict& dict){return Initialisation::Construct<Flux_Surfaces>(pyjson::to_json(dict));}), "Dictionary"_a)
        .def("__repr__", &Flux_Surfaces::Write_str)        
        .def("Rmnc", &Flux_Surfaces::Get_Rmnc)
        .def("Zmns", &Flux_Surfaces::Get_Zmns)
        .def("m_pol_vec", &Flux_Surfaces::Get_m_mpol_vector) 
        .def("n_tor_vec", &Flux_Surfaces::Get_n_ntor_vector) 
        .def("flux_surface_settings", &Flux_Surfaces::Get_Flux_Surface_Settings)
        .def("Return_Dictionary", [](const Flux_Surfaces& fs){return pyjson::from_json(fs.Return_Dictionary());})        
        .def("Return_Axis_Position", &Flux_Surfaces::Return_Axis_Position, "phi"_a)
        .def("Return_Position", [](const Flux_Surfaces& self,  DynamicVector& s, DynamicVector& d, DynamicVector& u, DynamicVector& v){
            Array values(s.rows(),3); 
            #pragma omp parallel for
            for(unsigned i=0; i < s.rows(); ++i){
                values.row(i)  = self.Return_Position({{s[i], d[i]}, u[i],v[i]});
            }
            return values;
        }, "s"_a, "LCFS_distance_label"_a, "theta"_a, "phi"_a)
        .def("Return_Position", [](const Flux_Surfaces& self,  double s, double d, DynamicVector& u, double v){
            VectorArray values(u.rows(),3); 
            for(unsigned i=0; i < u.rows(); ++i){
                values.row(i)  = self.Return_Position({{s, d}, u[i],v});
            }
            return values;
        }, "s"_a, "LCFS_distance_label"_a, "theta"_a, "phi"_a)
        .def("Return_Position", [](const Flux_Surfaces& self,  DynamicVector& s, DynamicVector& d, double u, double v){
            sb_assert_message(s.rows() == d.rows(), "Number of values for s and LCFS_distance_label not equal");
            VectorArray values(s.rows(),3); 
            for(unsigned i=0; i < s.rows(); ++i){
                values.row(i)  = self.Return_Position({{s[i], d[i]}, u,v});
            }
            return values;
        }, "s"_a, "LCFS_distance_label"_a, "theta"_a, "phi"_a)
        .def("Return_Position", [](const Flux_Surfaces& self,  double s, double d,  double u, DynamicVector& v){
            VectorArray values(v.rows(),3); 
            for(unsigned i=0; i < v.rows(); ++i){
                values.row(i)  = self.Return_Position({{s, d}, u,v[i]});
            }
            return values;
        }, "s"_a, "LCFS_distance_label"_a, "theta"_a, "phi"_a)
        .def("Return_Position", [](const Flux_Surfaces& self,  double s, double d, DynamicVector& u, double v){
            VectorArray values(u.rows(),3); 
            for(unsigned i=0; i < u.rows(); ++i){
                values.row(i)  = self.Return_Position({{s, d}, u[i],v});
            }
            return values;
        }, "s"_a, "LCFS_distance_label"_a, "theta"_a, "phi"_a)
        .def("Return_Position", [](const Flux_Surfaces& self, double s, double d, double u, double v){
            return self.Return_Position({{s, d}, u,v});
        } , "s"_a, "LCFS_distance_label"_a, "theta"_a, "phi"_a)
        .def("Return_Cylindrical_Position", [](const Flux_Surfaces& self, double s, double d, double u, double v){
            return self.Return_Cylindrical_Position({{s, d}, u,v});
        }, "s"_a, "LCFS_distance_label"_a, "theta"_a, "phi"_a)
        .def("Return_Cylindrical_Position", [](const Flux_Surfaces& self, double s, double d, DynamicVector u, double v){
            VectorArray result = VectorArray(u.rows(),3);
            for(unsigned i = 0; i < u.rows(); ++i){
                result.row(i) = self.Return_Cylindrical_Position({{s, d}, u[i],v});
            }
            return result;
        }, "s"_a, "LCFS_distance_label"_a, "theta"_a, "phi"_a)
        .def("Return_Normal", [](const Flux_Surfaces& self, double s, double d, double u, double v){
            return self.Return_Surface_Normal({{s, d}, u,v});
        }, "s"_a, "LCFS_distance_label"_a, "theta"_a, "phi"_a)
        .def("Return_Normal", [](const Flux_Surfaces& self, DynamicVector s, DynamicVector d, DynamicVector u, DynamicVector v){
            sb_assert_message(s.rows() == d.rows() && s.rows() == u.rows() && s.rows() == v.rows() , "Number of values not equal in all arrays!");
            VectorArray values(s.rows(),3); 
            #pragma omp parallel for
            for(unsigned i=0; i < s.rows(); ++i){
                values.row(i)  = self.Return_Surface_Normal({{s[i], d[i]}, u[i],v[i]});
            }
            return values;            
        }, "s"_a, "LCFS_distance_label"_a, "theta"_a, "phi"_a)


        .def("Mesh_Surface", [](const Flux_Surfaces& self, double s, double d, unsigned Nv, unsigned Nu, double tor_min, double tor_max, bool normals_facing_outwards){
            return Mesh(self.Return_UV_Manifold({s,d},Nu,Nv,{tor_min, tor_max}).Mesh_Surface_Orientation(normals_facing_outwards));
        }, "s"_a, "LCFS_distance_label"_a, "N_lines_phi"_a,  "N_lines_theta"_a, "phi_min"_a, "phi_max"_a, "Normals_Facing_Outwards"_a = true)
        .def("Mesh_Tetrahedrons", [](const Flux_Surfaces& self, DynamicVector s_arr, DynamicVector d_arr, unsigned Nv, unsigned Nu, double tor_min, double tor_max){
            return Mesh(Mesh_Tetrahedron_Flux_Surfaces(self, s_arr, d_arr, Nv, Nu, {tor_min, tor_max}));
        }, "s"_a, "LCFS_distance_label"_a,"N_lines_phi"_a,  "N_lines_theta"_a, "phi_min"_a, "phi_max"_a )
        .def("Mesh_Surfaces_Closed", [](const Flux_Surfaces& self, double s_1, double s_2, double d_1, double d_2, unsigned Nv, unsigned Nu, double tor_min, double tor_max){
            return Mesh(Mesh_Closed_Flux_Surface(self, {Radial_Flux_Coordinate(s_1, d_1), Radial_Flux_Coordinate(s_2, d_2)}, Nu, Nv, {tor_min, tor_max}));
        }, "s_1"_a, "s_2"_a, "LCFS_distance_label_1"_a, "LCFS_distance_label_2"_a, "N_lines_phi"_a,  "N_lines_theta"_a, "phi_min"_a, "phi_max"_a )
        .def("Mesh_Watertight_Flux_Surfaces", [](const Flux_Surfaces& self, double s_start, double d_start, DynamicVector ds, DynamicVector dd, unsigned n_phi, unsigned n_theta, double tor_min, double tor_max){
            auto toroidal_extent = Toroidal_Extent(tor_min, tor_max);
            auto r_start         = Radial_Flux_Coordinate(s_start, d_start);
            sb_assert_message(ds.rows() == dd.rows(), "Radial layer sizes do not match! (s= "+std::to_string(ds.rows())+", d="+std::to_string(dd.rows())+")");
            std::vector<Differential_Radial_Flux_Coordinate> dr;
            for(size_t i = 0; i < ds.rows(); ++i){
                dr.push_back(Differential_Radial_Flux_Coordinate(ds[i], dd[i]));
            }
            return Mesh_Watertight_Flux_Surfaces(self, r_start, dr, n_theta, n_phi, toroidal_extent);
        }, "s_start"_a, "LCFS_distance_label_start"_a, "d_s"_a, "d_LCFS_distance_2"_a, "N_lines_phi"_a,  "N_lines_theta"_a, "phi_min"_a, "phi_max"_a )
        .def("Mesh_Tiled_Surface", [](const Flux_Surfaces& self, double s, double d, unsigned N_tiles_v, unsigned N_tiles_u, double tile_spacing, double tor_min, double tor_max){
            return Mesh_Tiled_Surface(self,s,d, N_tiles_v, N_tiles_u, tile_spacing, tor_min, tor_max);
        },"s"_a, "LCFS_distance_label"_a,"N_lines_phi"_a,  "N_lines_theta"_a, "Tile_Fraction"_a, "phi_min"_a, "phi_max"_a )
        .def("Mesh_Detailed_Tiled_Surface", [](const Flux_Surfaces& self, double s, double d, unsigned N_tiles_v, unsigned N_tiles_u, double tile_spacing, double normal_inwards, double tor_min, double tor_max){
            return Mesh_Detailed_Tiled_Surface(self,s,d, N_tiles_v, N_tiles_u, tile_spacing, normal_inwards, tor_min, tor_max);
        },"s"_a, "LCFS_distance_label"_a,"N_lines_phi"_a,  "N_lines_theta"_a, "Tile_Fraction"_a, "Normal_Inwards"_a, "phi_min"_a, "phi_max"_a );
    nb::class_<Flux_Surfaces_Normal_Extended, Flux_Surfaces>(m, "Flux_Surfaces_Normal_Extended")
        .def(nb::init<const Array&, const Array&, Flux_Surface_Settings>(), "R_mnc"_a, "Z_mns"_a, "Flux_Surface_Settings"_a)
        .def(nb::init<const Flux_Surfaces&>(), "Flux_Surfaces"_a);

    nb::class_<Flux_Surfaces_Normal_Extended_Constant_Phi, Flux_Surfaces>(m, "Flux_Surfaces_Normal_Extended_Constant_Phi")
        .def(nb::init<const Array&, const Array&, Flux_Surface_Settings>(), "R_mnc"_a, "Z_mns"_a, "Flux_Surface_Settings"_a)
        .def(nb::init<const Flux_Surfaces&>(), "Flux_Surfaces"_a);

    nb::class_<Flux_Surfaces_Fourier_Extended, Flux_Surfaces>(m, "Flux_Surfaces_Fourier_Extended")
        .def(nb::init<const Array&, const Array&, Flux_Surface_Settings, const DynamicVector&, const Array&, const Array&, Flux_Surface_Settings >(), "R_mnc"_a, "Z_mns"_a, "Flux_Surface_Settings_Base"_a, "LCFS_distance_labels_extension"_a, "Rmnc_extension"_a, "Zmns_extension"_a,  "Flux_Surface_Settings_extension"_a)
        .def(nb::init<const Flux_Surfaces& , const DynamicVector&, const Array&, const Array&, Flux_Surface_Settings >(), "Flux_Surfaces"_a, "LCFS_distance_labels_extension"_a, "Rmnc_extension"_a, "Zmns_extension"_a,  "Flux_Surface_Settings_extension"_a)
        .def("Rmnc_Extension", &Flux_Surfaces_Fourier_Extended::Get_Rmnc_Extension)
        .def("Zmns_Extension", &Flux_Surfaces_Fourier_Extended::Get_Zmns_Extension)
        .def("Extension_Labels", &Flux_Surfaces_Fourier_Extended::Get_Extension_Labels)
        .def("Flux_Surface_Settings_Extension", &Flux_Surfaces_Fourier_Extended::Get_Flux_Surface_Settings_Extension);

    nb::class_<Coil>(m,"Coil")
	    .def("Scale_Points",&Coil::Scale_Points, "Factor"_a)
        .def("Get_Centre", &Coil::Get_Centre)        
        .def("Set_Centre", &Coil::Set_Centre, "Centre"_a)
        .def("__repr__", &Coil::Write_str)
        .def("Mesh_Triangles_Centroid", [](const Coil& self, double width_phi, double width_R, unsigned number_of_vertices){
            return Mesh(self.Mesh_Triangles_Centroid(width_phi, width_R,number_of_vertices));
            }, "width_phi"_a, "width_R"_a, "number_of_vertices"_a)
        .def("Mesh_Triangles_RMF", [](const Coil& self, double width_phi, double width_R, unsigned number_of_vertices){
            return Mesh(self.Mesh_Triangles_RMF(width_phi, width_R,number_of_vertices));
            }, "width_phi"_a, "width_R"_a, "number_of_vertices"_a)
        .def("Mesh_Triangles_Frenet", [](const Coil& self, double width_phi, double width_R, unsigned number_of_vertices){
            return Mesh(self.Mesh_Triangles_Frenet(width_phi, width_R,number_of_vertices));
            }, "width_phi"_a, "width_R"_a, "number_of_vertices"_a)
        .def("Mesh_Triangles_Rotated_From_Centroid", [](const Coil& self, double width_phi, double width_R, unsigned number_of_vertices, DynamicVector rot){
            return Mesh(self.Mesh_Triangles_Rotated_From_Centroid(width_phi, width_R,number_of_vertices, rot));
            }, "width_phi"_a, "width_R"_a, "number_of_vertices"_a, "rotation"_a)                                        
        
        .def("Position", [](const Coil& self, double arclength){return self.Position(arclength);})
        .def("Position",[](const Coil& self, DynamicVector arclength){
            auto result = VectorArray(arclength.rows(), 3);
            for(unsigned i =0; i < arclength.rows(); ++i){
                result.row(i) = self.Position(arclength[i]);
            }
            return result;
        })
        .def("Tangent", [](const Coil& self, double arclength){return self.Tangent(arclength);})
        .def("Tangent",[](const Coil& self, DynamicVector arclength){
            auto result = VectorArray(arclength.rows(), 3);
            for(unsigned i =0; i < arclength.rows(); ++i){
                result.row(i) = self.Tangent(arclength[i]);
            }
            return result;
        })

        .def("Finite_Size_Lines_Centroid", [](const Coil& self, double width_phi, double width_R, unsigned number_of_points){
            return self.Finite_Size_Lines_Centroid(number_of_points, width_phi, width_R);
            }, "width_phi"_a, "width_R"_a, "number_of_points"_a)
        .def("Finite_Size_Lines_RMF", [](const Coil& self, double width_phi, double width_R, unsigned number_of_points){
            return self.Finite_Size_Lines_RMF(number_of_points,width_phi, width_R);
            }, "width_phi"_a, "width_R"_a, "number_of_points"_a)
        .def("Finite_Size_Lines_Frenet", [](const Coil& self, double width_phi, double width_R, unsigned number_of_points){
            return self.Finite_Size_Lines_Frenet(number_of_points, width_phi, width_R);
            }, "width_phi"_a, "width_R"_a, "number_of_points"_a)
        .def("Finite_Size_Lines_Rotated_From_Centroid", [](const Coil& self, double width_phi, double width_R, unsigned number_of_points, DynamicVector rot){
            return self.Finite_Size_Lines_Rotated_From_Centroid(number_of_points, width_phi, width_R, rot);
            }, "width_phi"_a, "width_R"_a, "number_of_points"_a, "rotation"_a)                                        
        .def("Return_Sampling_Curve",[](const Coil& self){return self.Return_Sampling_Curve();});

    nb::class_<Discrete_Coil, Coil>(m,"Discrete_Coil")
        .def(nb::init<VectorArray>(), "Positions"_a)
        .def("Get_Vertices", &Discrete_Coil::Return_Sampling_Curve)
        .def("Set_Vertices", &Discrete_Coil::Set_Vertices, "Vertices"_a);
    nb::class_<Fourier_Coil, Coil>(m,"Fourier_Coil")
        .def(nb::init<VectorArray,VectorArray,Vector>(), "xyz_cos"_a, "xyz_sin"_a, "centre"_a)
        .def("Get_Fourier_Cos", &Fourier_Coil::Get_Fourier_Cos)
        .def("Set_Fourier_Cos", &Fourier_Coil::Set_Fourier_Cos, "Fourier_Cos"_a)
        .def("Get_Fourier_Sin", &Fourier_Coil::Get_Fourier_Sin)
        .def("Set_Fourier_Sin", &Fourier_Coil::Set_Fourier_Sin, "Fourier_Sin"_a);


    nb::class_<Coil_Set>(m, "Coil_Set")
        .def(nb::init<std::vector<std::shared_ptr<Coil>>&>())        
        .def("Truncate_to_Angles", [](Coil_Set& self, double tor_min, double tor_max){self.Truncate_To_Angles({tor_min, tor_max});})
	    .def("Scale_Points",&Coil_Set::Scale_Points,"Factor"_a) 
        .def("Number_of_Coils", [](const Coil_Set& self){return self.m_coils.size();})
        .def("__getitem__", [](const Coil_Set& self, unsigned index){
            if(index >= self.m_coils.size()){
                throw std::invalid_argument("Index " + std::to_string(index) + " greater than number of coils (" + std::to_string(self.m_coils.size())+")");
            }
            return self.m_coils[index];
        })
        .def("__iter__", [](const Coil_Set& self){return nb::make_iterator(nb::type<Coil_Set>(), "iterator",self.begin(), self.end());}, nb::keep_alive<0,1>())
        .def("Mesh_Triangles_Centroid", [](const Coil_Set& self, double width_phi, double width_R, unsigned number_of_vertices){
            std::vector<Triangle_Vertices> result;
            for(auto& coil : self.m_coils){
                result.push_back(coil->Mesh_Triangles_Centroid(width_phi, width_R,number_of_vertices));
            }
            return Mesh_From_Triangle_Vertices_Vector(result);
        },"width_phi"_a, "width_R"_a, "number_of_vertices"_a)
        .def("Mesh_Triangles_RMF", [](const Coil_Set& self, double width_phi, double width_R, unsigned number_of_vertices){
            std::vector<Triangle_Vertices> result;
            for(auto& coil : self.m_coils){
                result.push_back(coil->Mesh_Triangles_RMF(width_phi, width_R,number_of_vertices));
            }
            return Mesh_From_Triangle_Vertices_Vector(result);
        },"width_phi"_a, "width_R"_a, "number_of_vertices"_a)
        .def("Mesh_Triangles_Frenet", [](const Coil_Set& self, double width_phi, double width_R, unsigned number_of_vertices){
            std::vector<Triangle_Vertices> result;
            for(auto& coil : self.m_coils){
                result.push_back(coil->Mesh_Triangles_Frenet(width_phi, width_R,number_of_vertices));
            }
            return Mesh_From_Triangle_Vertices_Vector(result);
        },"width_phi"_a, "width_R"_a, "number_of_vertices"_a)
        .def("Mesh_Triangles_Rotated_From_Centroid", [](const Coil_Set& self, double width_phi, double width_R, unsigned number_of_vertices, DynamicVector rot){
            std::vector<Triangle_Vertices> result;
            for(auto& coil : self.m_coils){
                result.push_back(coil->Mesh_Triangles_Rotated_From_Centroid(width_phi, width_R,number_of_vertices, rot));
            }
            return Mesh_From_Triangle_Vertices_Vector(result);
        },"width_phi"_a, "width_R"_a, "number_of_vertices"_a, "rotation"_a);
}
