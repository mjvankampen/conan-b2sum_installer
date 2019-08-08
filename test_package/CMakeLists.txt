cmake_minimum_required(VERSION 2.8.11)

project(test_package CXX)

include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

find_program(B2SUM_CMD b2sum)

if ( NOT B2SUM_CMD )
    message(FATAL_ERROR "b2sum not found!")
else()
	message(STATUS "Found b2sum")
	execute_process(COMMAND ${B2SUM_CMD} --help)
endif()

