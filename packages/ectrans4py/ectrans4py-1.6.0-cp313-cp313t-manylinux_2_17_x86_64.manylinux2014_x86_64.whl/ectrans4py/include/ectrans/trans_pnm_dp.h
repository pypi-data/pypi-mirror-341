! (C) Copyright 2000- ECMWF.
! (C) Copyright 2013- Meteo-France.
! 
! This software is licensed under the terms of the Apache Licence Version 2.0
! which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
! In applying this licence, ECMWF does not waive the privileges and immunities
! granted to it by virtue of its status as an intergovernmental organisation
! nor does it submit to any jurisdiction.
!

INTERFACE
SUBROUTINE TRANS_PNM_dp(KRESOL,KM,PRPNM,LDTRANSPOSE,LDCHEAP)

!**** *TRANS_PNM_dp* - Compute Legendre polynomials for a given wavenember

!     Purpose.
!     --------
!     Interface routine for computing Legendre polynomials for a given wavenember

!**   Interface.
!     ----------
!     CALL TRANS_PNM_dp(...)

!     Explicit arguments : All arguments are optional.
!     --------------------
!     KRESOL   - resolution tag for which info is required ,default is the
!                first defined resulution (input)
!     KM       - wave number
!     PRPNM    - Legendre polynomials
!     LDTRANSPOSE - Legendre polynomials array is transposed
!     LDCHEAP   - cheapest but less accurate computation

!     Method.
!     -------

!     Externals.  SET_RESOL - set resolution
!     ----------

!     Author.
!     -------
!        R. El Khatib *METEO-FRANCE*

!     Modifications.
!     --------------
!        Original : 22-Jan-2016

!     ------------------------------------------------------------------

USE EC_PARKIND  ,ONLY : JPIM     ,JPRD

IMPLICIT NONE

INTEGER(KIND=JPIM) ,OPTIONAL, INTENT(IN)  :: KRESOL
INTEGER(KIND=JPIM) ,INTENT(IN)  :: KM
REAL(KIND=JPRD)    ,INTENT(OUT) :: PRPNM(:,:)
LOGICAL, OPTIONAL, INTENT(IN) :: LDTRANSPOSE
LOGICAL, OPTIONAL, INTENT(IN) :: LDCHEAP

END SUBROUTINE TRANS_PNM_dp
END INTERFACE
