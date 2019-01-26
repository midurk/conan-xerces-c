cmake_minimum_required(VERSION 2.8.12)
project(test_package)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(${PROJECT_NAME} 
  MemParse/MemParse.cpp
  MemParse/MemParse.hpp
  MemParse/MemParseHandlers.cpp
  MemParse/MemParseHandlers.hpp)
  
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})
