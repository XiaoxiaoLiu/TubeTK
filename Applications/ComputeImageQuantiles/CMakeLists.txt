##############################################################################
#
# Library:   TubeTK
#
# Copyright 2010 Kitware Inc. 28 Corporate Drive,
# Clifton Park, NY, 12065, USA.
#
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
##############################################################################

set( MODULE_NAME ComputeImageQuantiles )
project( ${MODULE_NAME} )

if( NOT TubeTK_SOURCE_DIR )
  find_package( TubeTK REQUIRED )
  include( ${TubeTK_USE_FILE} )
endif( NOT TubeTK_SOURCE_DIR )

find_package( SlicerExecutionModel REQUIRED )
include( ${SlicerExecutionModel_USE_FILE} )

find_package( ITK REQUIRED )
include( ${USE_ITK_FILE} )

# Find Boost
set( Boost_ADDITIONAL_VERSIONS "1.51 1.52 1.53" )
find_package( Boost 1.49 COMPONENTS system filesystem REQUIRED )

# Fiddle with template-depth (for Boost's accumulators)
set( USER_CMAKE_CXX_FLAGS "-ftemplate-depth-100" )
set( CMAKE_CXX_FLAGS
   "${CMAKE_CXX_FLAGS} ${USER_CMAKE_CXX_FLAGS}" )
set( CMAKE_CXX_FLAGS_RELEASE
  "${CMAKE_CXX_FLAGS_RELEASE} ${USER_CMAKE_CXX_FLAGS}" )
set( CMAKE_CXX_FLAGS_DEBUG
  "${CMAKE_CXX_FLAGS_DEBUG} ${USER_CMAKE_CXX_FLAGS}" )
set( CMAKE_CXX_FLAGS_RELWITHDEBINFO
  "${CMAKE_CXX_FLAGS_RELWITHDEBINFO} ${USER_CMAKE_CXX_FLAGS}" )

SEMMacroBuildCLI(
  NAME ${MODULE_NAME}
  LOGO_HEADER ${TubeTK_SOURCE_DIR}/Base/CLI/TubeTKLogo.h
  TARGET_LIBRARIES ${ITK_LIBRARIES}
  INCLUDE_DIRECTORIES
    ${Boost_INCLUDE_DIRS}
    ${TubeTK_SOURCE_DIR}/Base/CLI
    ${TubeTK_SOURCE_DIR}/Base/Common
    ${TubeTK_SOURCE_DIR}/Base/Filtering )

if( BUILD_TESTING )
  add_subdirectory( Testing )
endif( BUILD_TESTING )
