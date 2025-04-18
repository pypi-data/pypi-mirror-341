cmake_minimum_required(VERSION 3.10)



list(APPEND SOURCE_FILES Vector.cpp)

list(APPEND SOURCE_FILES Spherical_Harmonic_Functions.cpp)
list(APPEND SOURCE_FILES Matrix.cpp)
list(APPEND SOURCE_FILES Contiguous_Arrays.cpp)
list(APPEND SOURCE_FILES Constants.cpp)
list(APPEND SOURCE_FILES Node.cpp)
list(APPEND SOURCE_FILES Mesh_Tools.cpp)
list(APPEND SOURCE_FILES OMP_Tools.cpp)
list(APPEND SOURCE_FILES Conversion_Tools.cpp)
list(APPEND SOURCE_FILES custom_assert.h)
list(APPEND SOURCE_FILES Iterators.h)
list(APPEND SOURCE_FILES Norms.cpp)
add_library(math ${SOURCE_FILES})

find_package(OpenMP)
if(OpenMP_CXX_FOUND)
    target_link_libraries(math OpenMP::OpenMP_CXX)
endif()

INCLUDE_DIRECTORIES ( "${EIGEN3_INCLUDE_DIR}" )
message(${EIGEN3_INCLUDE_DIR})
target_include_directories(math PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${EIGEN3_INCLUDE_DIR})