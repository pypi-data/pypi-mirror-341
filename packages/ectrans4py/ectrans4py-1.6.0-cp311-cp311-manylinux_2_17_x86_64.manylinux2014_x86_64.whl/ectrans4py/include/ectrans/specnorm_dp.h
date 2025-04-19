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
SUBROUTINE SPECNORM_dp(PNORM,PSPEC,KVSET,KMASTER,KRESOL,PMET)

!**** *SPECNORM_dp* - Compute global spectral norms

!     Purpose.
!     --------
!        Interface routine for computing spectral norms

!**   Interface.
!     ----------
!     CALL SPECNORM_dp(...)

!     Explicit arguments : All arguments optional
!     -------------------- 
!     PSPEC(:,:)  - Spectral array
!     KVSET(:)    - "B-Set" for each field
!     KMASTER     - processor to recieve norms
!     KRESOL      - resolution tag  which is required ,default is the
!                   first defined resulution (input)
!     PMET(:)     - metric
!     PNORM(:)    - Norms (output for processor KMASTER)
!
!     Method.
!     -------

!     Externals.  SET_RESOL - set resolution
!     ----------  SPNORM_CTL - control routine

!     Author.
!     -------
!        Mats Hamrud *ECMWF*

!     Modifications.
!     --------------
!        Original : 00-03-03

!     ------------------------------------------------------------------

USE EC_PARKIND  ,ONLY : JPIM     ,JPRD


IMPLICIT NONE

! Declaration of arguments


REAL(KIND=JPRD)             , INTENT(OUT) :: PNORM(:)
REAL(KIND=JPRD)    ,OPTIONAL, INTENT(IN)  :: PSPEC(:,:)
INTEGER(KIND=JPIM) ,OPTIONAL, INTENT(IN)  :: KVSET(:)
INTEGER(KIND=JPIM) ,OPTIONAL, INTENT(IN)  :: KMASTER
REAL(KIND=JPRD)    ,OPTIONAL, INTENT(IN)  :: PMET(:)
INTEGER(KIND=JPIM) ,OPTIONAL, INTENT(IN)  :: KRESOL

!     ------------------------------------------------------------------

END SUBROUTINE SPECNORM_dp

END INTERFACE
