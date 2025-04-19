#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ectrans_common" for configuration "Release"
set_property(TARGET ectrans_common APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ectrans_common PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libectrans_common.so"
  IMPORTED_SONAME_RELEASE "libectrans_common.so"
  )

list(APPEND _cmake_import_check_targets ectrans_common )
list(APPEND _cmake_import_check_files_for_ectrans_common "${_IMPORT_PREFIX}/lib64/libectrans_common.so" )

# Import target "ectrans_dp" for configuration "Release"
set_property(TARGET ectrans_dp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ectrans_dp PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libectrans_dp.so"
  IMPORTED_SONAME_RELEASE "libectrans_dp.so"
  )

list(APPEND _cmake_import_check_targets ectrans_dp )
list(APPEND _cmake_import_check_files_for_ectrans_dp "${_IMPORT_PREFIX}/lib64/libectrans_dp.so" )

# Import target "ectrans-benchmark-cpu-dp" for configuration "Release"
set_property(TARGET ectrans-benchmark-cpu-dp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ectrans-benchmark-cpu-dp PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/ectrans-benchmark-cpu-dp"
  )

list(APPEND _cmake_import_check_targets ectrans-benchmark-cpu-dp )
list(APPEND _cmake_import_check_files_for_ectrans-benchmark-cpu-dp "${_IMPORT_PREFIX}/bin/ectrans-benchmark-cpu-dp" )

# Import target "ectrans-lam-benchmark-cpu-dp" for configuration "Release"
set_property(TARGET ectrans-lam-benchmark-cpu-dp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ectrans-lam-benchmark-cpu-dp PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/ectrans-lam-benchmark-cpu-dp"
  )

list(APPEND _cmake_import_check_targets ectrans-lam-benchmark-cpu-dp )
list(APPEND _cmake_import_check_files_for_ectrans-lam-benchmark-cpu-dp "${_IMPORT_PREFIX}/bin/ectrans-lam-benchmark-cpu-dp" )

# Import target "transi_dp" for configuration "Release"
set_property(TARGET transi_dp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(transi_dp PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libtransi_dp.so"
  IMPORTED_SONAME_RELEASE "libtransi_dp.so"
  )

list(APPEND _cmake_import_check_targets transi_dp )
list(APPEND _cmake_import_check_files_for_transi_dp "${_IMPORT_PREFIX}/lib64/libtransi_dp.so" )

# Import target "ectrans_etrans_dp" for configuration "Release"
set_property(TARGET ectrans_etrans_dp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ectrans_etrans_dp PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libectrans_etrans_dp.so"
  IMPORTED_SONAME_RELEASE "libectrans_etrans_dp.so"
  )

list(APPEND _cmake_import_check_targets ectrans_etrans_dp )
list(APPEND _cmake_import_check_files_for_ectrans_etrans_dp "${_IMPORT_PREFIX}/lib64/libectrans_etrans_dp.so" )

# Import target "ectrans4py_dp" for configuration "Release"
set_property(TARGET ectrans4py_dp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ectrans4py_dp PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libectrans4py_dp.so"
  IMPORTED_SONAME_RELEASE "libectrans4py_dp.so"
  )

list(APPEND _cmake_import_check_targets ectrans4py_dp )
list(APPEND _cmake_import_check_files_for_ectrans4py_dp "${_IMPORT_PREFIX}/lib64/libectrans4py_dp.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
