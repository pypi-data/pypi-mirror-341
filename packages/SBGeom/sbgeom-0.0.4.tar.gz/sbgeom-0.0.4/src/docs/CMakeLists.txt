find_package(Doxygen)
if(DOXYGEN_FOUND)
    file(GLOB_RECURSE STELL_BLANKET_PUBLIC_HEADERS ${PROJECT_SOURCE_DIR}/*.h)
    list(FILTER STELL_BLANKET_PUBLIC_HEADERS EXCLUDE REGEX ".*/external/.*h") # Don't want to document the external headers (this is also specified in the Doxyfile.in file!)

    # set input and output files
    set(DOXYGEN_INPUT_DIR  ${PROJECT_SOURCE_DIR})
    set(DOXYGEN_OUTPUT_DIR ${CMAKE_CURRENT_BINARY_DIR}/doxygen)
    set(DOXYFILE_IN  ${CMAKE_CURRENT_SOURCE_DIR}/Doxyfile.in)
    set(DOXYFILE_OUT ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile)
    message(${CMAKE_CURRENT_BINARY_DIR})
    # request to configure the file
    configure_file(${DOXYFILE_IN} ${DOXYFILE_OUT} @ONLY)


    set(DOXYGEN_INDEX_FILE ${DOXYGEN_OUTPUT_DIR}/xml/index.xml)

    # note the option ALL which allows to build the docs together with the application

    file(MAKE_DIRECTORY ${DOXYGEN_OUTPUT_DIR})
    add_custom_command(OUTPUT ${DOXYGEN_INDEX_FILE}
                       DEPENDS ${STELL_BLANKET_PUBLIC_HEADERS}
                       COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYFILE_OUT}
                       MAIN_DEPENDENCY ${DOXYFILE_OUT} ${DOXYFILE_IN}
                       COMMENT "Gerating Doxygen Docs")
    #Dependency is for checking which files changed (i.e. do not rerun doxygen if no headers are changed)
    add_custom_target(Doxygen ALL DEPENDS ${DOXYGEN_INDEX_FILE})

    find_package(Sphinx)
        if(Sphinx_FOUND)
        set(SPHINX_SOURCE ${CMAKE_CURRENT_SOURCE_DIR})
        set(SPHINX_BUILD ${CMAKE_CURRENT_BINARY_DIR}/sphinx)
        set(SPHINX_INDEX_FILE ${SPHINX_BUILD}/index.html)


        file(GLOB_RECURSE SPHINX_DOCS ${CMAKE_CURRENT_SOURCE_DIR}/*.rst)

        add_custom_command(OUTPUT ${SPHINX_INDEX_FILE}
                           COMMAND ${SPHINX_EXECUTABLE} -b html -Dbreathe_projects.DEMETER=${DOXYGEN_OUTPUT_DIR}/xml ${SPHINX_SOURCE} ${SPHINX_BUILD}
                           WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
                           DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/index.rst ${DOXYGEN_INDEX_FILE} ${SPHINX_DOCS}
                           MAIN_DEPENDENCY ${SPHINX_SOURCE}/conf.py)
        add_custom_target(Sphinx ALL DEPENDS ${SPHINX_INDEX_FILE})

    else()
        message(" Sphinx not found, can only build Doxygen docs")
    endif()
else()
    message(" Doxygen not found, cannot build docs")
endif()      




                  
                  