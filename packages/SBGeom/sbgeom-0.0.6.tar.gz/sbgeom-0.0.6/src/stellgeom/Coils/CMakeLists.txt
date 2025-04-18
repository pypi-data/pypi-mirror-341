cmake_minimum_required(VERSION 3.10)




list(APPEND SOURCE_FILES Coils.cpp)



add_library(Coils ${SOURCE_FILES})

target_link_libraries(Coils math)
target_link_libraries(Coils Input_Output)
target_link_libraries(Coils Flux_Surfaces_Geometry)

target_include_directories(Coils INTERFACE ${CMAKE_CURRENT_SOURCE_DIR})
