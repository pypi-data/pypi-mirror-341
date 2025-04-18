cmake_minimum_required(VERSION 3.10)



add_definitions(
	-DTW_STATIC
	-DTW_NO_LIB_PRAGMA
	-DTW_NO_DIRECT3D
	-DGLEW_STATIC
	-D_CRT_SECURE_NO_WARNINGS
)
list(APPEND SOURCE_FILES Flux_Surface_Coords.cpp)
list(APPEND SOURCE_FILES UV_Manifolds.cpp)
list(APPEND SOURCE_FILES Flux_Surfaces.cpp)
list(APPEND SOURCE_FILES Flux_Surfaces_Extended.cpp)
list(APPEND SOURCE_FILES Flux_Surfaces_Initialisation.cpp)
list(APPEND SOURCE_FILES Flux_Surface_Node.cpp)

add_library(Flux_Surfaces_Geometry ${SOURCE_FILES})


target_link_libraries(Flux_Surfaces_Geometry math)
target_link_libraries(Flux_Surfaces_Geometry Input_Output)

target_include_directories(Flux_Surfaces_Geometry INTERFACE ${CMAKE_CURRENT_SOURCE_DIR})
