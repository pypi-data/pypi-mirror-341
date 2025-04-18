cmake_minimum_required(VERSION 3.15)
project(SBGeom)

# Debug options (for asserts)
if (CMAKE_BUILD_TYPE STREQUAL "")
    message(STATUS "  Diag: Build type was unspecified, set to RelWithDebugInfo")
    set(CMAKE_BUILD_TYPE RelWithDebugInfo)
else ()
    message(STATUS "  Diag: Build type specified as '${CMAKE_BUILD_TYPE}'")
endif ()

if (CMAKE_BUILD_TYPE STREQUAL Debug)
    set_directory_properties(PROPERTIES COMPILE_DEFINITIONS "_DEBUG")
else ()
    set_directory_properties(PROPERTIES COMPILE_DEFINITIONS "NDEBUG")
endif ()
cmake_policy(SET CMP0074 NEW)
message(${CMAKE_BUILD_TYPE})


add_compile_options(-march=native -O3 -std=c++20 -g -fPIC)





find_package(OpenMP)
if(OpenMP_CXX_FOUND)
    link_libraries(OpenMP::OpenMP_CXX)
endif()


set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})



#=========================================================================================================
#||                                            nanobind                                                 ||
#=========================================================================================================
if (CMAKE_VERSION VERSION_LESS 3.18)
  set(DEV_MODULE Development)
else()
  set(DEV_MODULE Development.Module)
endif()
set(Python_FIND_STRATEGY LOCATION)
find_package(Python 3.8 COMPONENTS Interpreter ${DEV_MODULE} REQUIRED)
execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE NB_DIR)
  message("Nanobind Location: ${NB_DIR}")
list(APPEND CMAKE_PREFIX_PATH "${NB_DIR}")
find_package(nanobind CONFIG)

# nanobind_FOUND

#=========================================================================================================
#||                                             Options                                                 ||
#=========================================================================================================

add_definitions(-DCHECK_ASSERT_SB)
add_definitions(-DCHECK_ASSERT_SB_DEBUG)
add_definitions(-DLINEAR_SB)
#add_definitions(-DCONSTANT_SB)
#add_definitions(-DQUADRATIC_SB)
#add_definitions(-DCUBIC_SB)


#=========================================================================================================
#||                                             TARGETS                                                 ||
#=========================================================================================================
    set(EIGEN3_INCLUDE_DIR "$ENV{EIGEN3_INCLUDE_DIR}")
    if(EIGEN3_INCLUDE_DIR)
    else()
        message("EIGEN3_INCLUDE_DIR not set, setting it to default CI: /project/eigen/")
        set(ENV{EIGEN3_INCLUDE_DIR} "/project/eigen/")
    endif()
    set(EIGEN3_INCLUDE_DIR "$ENV{EIGEN3_INCLUDE_DIR}")
    if(EIGEN3_INCLUDE_DIR)
        message(EIGEN3_INCLUDE_DIR)
        add_subdirectory(src/stellgeom/demeter_util/math)
        add_subdirectory(src/stellgeom/demeter_util/Input_Output)
        add_subdirectory(src/stellgeom/Flux_Surfaces_Geometry)
        add_subdirectory(src/stellgeom/Coils)

        list(APPEND SBGEOM_LIBS Flux_Surfaces_Geometry Coils)

        
        if(nanobind_FOUND)            
                                                

            list(APPEND SBGEOM_SRC 
                src/SBGeom/sbgeom.cpp)
            nanobind_add_module(sbgeom_cpp NOMINSIZE ${SBGEOM_SRC})
            target_link_libraries(sbgeom_cpp PRIVATE ${SBGEOM_LIBS})
            target_include_directories(sbgeom_cpp PUBLIC "${PROJECT_BINARY_DIR}" src/nanobind_utilities )

            set_target_properties(sbgeom_cpp PROPERTIES POSITION_INDEPENDENT_CODE ON)
            
            
            nanobind_add_stub(sbgeom_cpp_stub
                MODULE sbgeom_cpp
                OUTPUT ${CMAKE_BINARY_DIR}/sbgeom_cpp.pyi
                PYTHON_PATH $<TARGET_FILE_DIR:sbgeom_cpp>
                DEPENDS sbgeom_cpp
            )
                        
            install(TARGETS sbgeom_cpp DESTINATION SBGeom OPTIONAL)                                    
            
            install(FILES            
             ${CMAKE_BINARY_DIR}/sbgeom_cpp.pyi
             DESTINATION SBGeom OPTIONAL)
             
            
        else()
            message("nanobind not found, cannot build Python bindings...")
        endif()

    else()
        message("Please point the environment variable EIGEN3_INCLUDE_DIR to the include directory of your Eigen3 installation.")
        message("Can only build docs")
    endif()


add_subdirectory(src/docs)


