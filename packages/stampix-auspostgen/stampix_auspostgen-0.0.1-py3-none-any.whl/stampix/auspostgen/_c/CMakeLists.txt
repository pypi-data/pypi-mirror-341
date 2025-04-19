cmake_minimum_required(VERSION 3.10)
project(auspost)

# Find Python
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Add gettext library path
set(GETTEXT_ROOT "/opt/homebrew/opt/gettext")
set(CMAKE_LIBRARY_PATH ${CMAKE_LIBRARY_PATH} ${GETTEXT_ROOT}/lib)

# Set C standard
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Add the source files
set(SOURCES
    auspost.c
)

# Create the shared library
add_library(auspost SHARED ${SOURCES})

# Set output name to match Python's expectations
set_target_properties(auspost PROPERTIES
    PREFIX ""
    OUTPUT_NAME "auspost"
)

# Link against Python and gettext
target_link_libraries(auspost PRIVATE Python3::Python)
target_link_directories(auspost PRIVATE ${GETTEXT_ROOT}/lib)

# Set include directories
target_include_directories(auspost PRIVATE
    ${Python3_INCLUDE_DIRS}
)

# Set compile definitions
target_compile_definitions(auspost PRIVATE
    PY_SSIZE_T_CLEAN
)

# Install the library
install(TARGETS auspost
    LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}
)
