# (C) Copyright 2020- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

# Import for trans package
#
# This file is included during
#
#    find_package( ectrans [COMPONENTS (double|single|transi)] [QUIET] [REQUIRED] )
#
# Supported COMPONENTS: double single transi
#
# If available following targets will be exported:
# - trans_dp  Double precision trans library
# - trans_sp  Single precision trans library
# - transi_dp Double precision transi library (C interface to trans_dp)
#

##################################################################
## Export project variables

set( ectrans_VERSION_STR             1.6.0 )
set( ectrans_HAVE_MPI                0 )
set( ectrans_HAVE_OMP                True )
set( ectrans_HAVE_FFTW                )
set( ectrans_HAVE_TRANSI             True )
set( ectrans_HAVE_SINGLE_PRECISION   0 )
set( ectrans_HAVE_DOUBLE_PRECISION   True )
set( ectrans_REQUIRES_PRIVATE_DEPENDENCIES 0 )

if( NOT ${CMAKE_FIND_PACKAGE_NAME}_FIND_QUIETLY )
  message( STATUS "Found ectrans version ${ectrans_VERSION_STR}" )
endif()

##################################################################
## Export project dependencies

include( CMakeFindDependencyMacro )
if( ectrans_REQUIRES_PRIVATE_DEPENDENCIES OR CMAKE_Fortran_COMPILER_LOADED )
    if( NOT CMAKE_Fortran_COMPILER_LOADED )
        enable_language( Fortran )
    endif()
    if( trans_HAVE_OMP AND NOT TARGET OpenMP::OpenMP_Fortran )
        find_dependency( OpenMP COMPONENTS Fortran )
    endif()
    find_dependency( fiat HINTS ${CMAKE_CURRENT_LIST_DIR}/../fiat /home/mary/containers/build_ectrans4py/work/install/lib64/cmake/fiat )
endif()


##################################################################
## Handle components

set( ${CMAKE_FIND_PACKAGE_NAME}_single_FOUND ${ectrans_HAVE_SINGLE_PRECISION} )
set( ${CMAKE_FIND_PACKAGE_NAME}_double_FOUND ${ectrans_HAVE_DOUBLE_PRECISION} )
set( ${CMAKE_FIND_PACKAGE_NAME}_transi_FOUND ${ectrans_HAVE_TRANSI} )

foreach( _component ${${CMAKE_FIND_PACKAGE_NAME}_FIND_COMPONENTS} )
  if( NOT ${CMAKE_FIND_PACKAGE_NAME}_${_component}_FOUND AND ${CMAKE_FIND_PACKAGE_NAME}_FIND_REQUIRED )
    message( SEND_ERROR "ectrans was not build with support for COMPONENT ${_component}" )
  endif()
endforeach()
