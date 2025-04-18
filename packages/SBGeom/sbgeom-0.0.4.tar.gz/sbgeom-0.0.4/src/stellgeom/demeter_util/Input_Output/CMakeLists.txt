cmake_minimum_required(VERSION 3.10)
list(APPEND SOURCE_FILES Utility.cpp)
list(APPEND SOURCE_FILES json_utility.cpp)
list(APPEND SOURCE_FILES json.h)
add_library(Input_Output ${SOURCE_FILES})

target_link_libraries(Input_Output math)
target_include_directories(Input_Output INTERFACE ${CMAKE_CURRENT_SOURCE_DIR})
 