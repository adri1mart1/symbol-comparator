cmake_minimum_required(VERSION 3.23)

project(example CXX)

set(CMAKE_CXX_COMPILER "g++")

add_executable(pgmA ${CMAKE_CURRENT_SOURCE_DIR}/mainA.cpp)

add_executable(pgmB ${CMAKE_CURRENT_SOURCE_DIR}/mainB.cpp)