! (C) Copyright 2001- ECMWF.
! (C) Copyright 2001- Meteo-France.
! 
! This software is licensed under the terms of the Apache Licence Version 2.0
! which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
! In applying this licence, ECMWF does not waive the privileges and immunities
! granted to it by virtue of its status as an intergovernmental organisation
! nor does it submit to any jurisdiction.
! 


INTERFACE
SUBROUTINE HORIZ_FIELD(KX,KY,PHFIELD)

USE EC_PARKIND  ,ONLY : JPIM     ,JPRD

IMPLICIT NONE

INTEGER(KIND=JPIM),   INTENT(IN)    :: KX
INTEGER(KIND=JPIM),   INTENT(IN)    :: KY
REAL(KIND=JPRD),      INTENT(OUT)   :: PHFIELD(KX,KY)
REAL(KIND=JPRD),      PARAMETER     :: PPI=3.141592
END SUBROUTINE HORIZ_FIELD
END INTERFACE
