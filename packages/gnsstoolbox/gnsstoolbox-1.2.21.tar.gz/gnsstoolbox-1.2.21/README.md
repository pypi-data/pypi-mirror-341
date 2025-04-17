# GnssToolbox - Python package for GNSS learning

## Installation

This package requires Python 3

Required packages : 

* gpsdatetime - https://pypi.org/project/gpsdatetime/ (J. Beilin - ENSG)
* re
* math
* numpy
* copy
* time
* os
* json
* from operator import attrgetter

Installation is accomplished from the command line.

* From pypi

```
user@desktop$pip3 install pygnsstoolbox
```

* From package source directory

```
user@desktop$~/gnsstoolbox$ python3 setup.py install
```

For usage see gnsstoolbox cheatsheet and beamer slides shipped with the package. 

## Import modules

```python
""" Ephemerides management """
import gnsstoolbox.orbits as orbits

""" GNSS data (rinex "o" files) """ 
import gnsstoolbox.rinex_o as rx

""" Processing tools (rotations, coordinate conversions...) """
import gnsstoolbox.gnsstools as tools

""" Code processing """
import gnsstoolbox.gnss_process as proc

""" Constantes utiles """
import gnsstoolbox.gnss_const as const

""" Corrections (troposphere, antennas...) """
import gnsstoolbox.gnss_corr as corr
```

## gnss_const

| Constant | Description | Unit |
| :- |:- | :- |
|c| celerity | 299792458 m/s |
|f1| frequency L1 gps | 1.57542 GHz |
|f2| frequency L2 gps | 1.22760 GHz |
|f5| frequency L5 gps | 1.17645 GHz |

## orbits

### Structure

Orbit class contains all orbits informations :

|Attribute |Definition|
|:-|:-|
|leap_seconds||
|ion_alpha_gps||
|ion_beta_gps||
|ion_gal||
|delta_utc||
| NAV_dataG | list of GPS navigation message  |
| NAV_dataE | list of Galileo navigation message|
| NAV_dataR | list of Glonass navigation message|
| G | list of Sp3Pos objects with GPS precise orbits|
| E | list of Sp3Pos objects with Galileo precise orbits|
| R | list of Sp3Pos objects with Glonass precise orbits|


### GPS/Galileo nav  element (nav_element)

|Attribute| Definition | Unit|
|:-|:-|:-|
|tgps|date/time of ephemeris|gpsdatetime|
|mjd|date/time of ephemeris|decimal day from 17 November 1858|
|gps_wk|GPS week|week number from 6 jannuary 1980|
|TOE|Time of ephemeris|second of week|
|TOC|TIme of clock|==mjd|
|const|Constellation| G or E|
|PRN| Pseudo-random noise| I2|
|e|Orbit excentricity|without unit|
|sqrt_a|Square-root of semi-major axis|m**0.5|
|M0|Mean anomaly at at reference time|radians|
|delta_n|Mean motion difference from 2 body problem|radian.s**-1|
|i0| Inclination à TOE|radians|
|IDOT|Rate of change of inclination|radians.s**-1|
|crc|Amplitude of the cosine harmonic correction term to the orbit radius |radians|
|crs|Amplitude of the sine harmonic correction term to the orbit radius |radians|
|cuc|Amplitude of cosine harmonic correction term to the argument of latitude|radians|
|cus|Amplitude of sine harmonic correction term to the argument of latitude|radians|
|cic|Amplitude of the cosine harmonic correction term to the angle of inclination|radians|
|cis|Amplitude of the sine harmonic correction term to the angle of inclination|radians|
|omega|Argument of perigee|radians|
|OMEGA0|Longitude of ascending node of orbit plane at weekly epoch|radians|
|OMEGA_DOT|Rate of Right Ascension |radians.s**-1|
|L2_P|||
|sv_acc|||
|sv_health|Space vehicle health||
|TGD|Time group delay||
|alpha0|Clock bias|s|
|alpha1|Clock drift coefficient|s.s**-1|
|alpha2|Clock drift rate coefficient|s.s**-2|
|IODC|Issue of data, clock||
|IODE|Issue of data, ephemeris||

### Glonass nav  element (nav_element)

|Attribute| Definition | Unit|
|:-|:-|:-|
|tgps|date/time of ephemeris|gpsdatetime|
|mjd|date/time of ephemeris|modified julian date|
|gps_wk|GPS week|week number from 6 jannuary 1980|
|const|Constellation| R |
|PRN| Pseudo-random noise| #|
|SV_clock_offset||s|
|SV_relat_freq_offset||s.s**-1|
|Message_frame_time||s.s**-2|
|X||m|
|X_dot||m.s**-1|
|MS_X_acc||m.s**-2|
|Y||m|
|Y_dot||m.s**-1|
|MS_Y_acc||m.s**-2|
|Z||m|
|Z_dot||m.s**-1|
|MS_Z_acc||m.s**-2|
|freq_num||#|
|sv_health|||
|age_op_inf||days|

### Sp3 precise orbit (Sp3Pos class)

|Attribute| Definition | Unit|
|:-|:-|:-|
|mjd|date/time of ephemeris|modified julian date|
|X|X coordinate ECEF| m|
|Y|Y coordinate ECEF| m|
|Z|Z coordinate ECEF| m|
|dte| Satellite clock bias|µs|

### Data loading

* Broadcast ephemerides loading  (*.yyn ou *.yyg)

```python
Orb = orbits.orbit()
Orb.loadRinexN('brdm1500.13p')  
```


* Precise ephemerides loading (*.sp3)

```python
Orb = orbits.orbit()
Orb.loadSp3(['igs17424.sp3','igl17424.sp3','grm17424.sp3'])
```
or 

```python
Orb.loadSp3('igs17424.sp3') 
```

### Data access

* Get broadcast ephemerides for a satellite at an instant mjd 

```python
Eph = Orb.getEphemeris(constellation,PRN,mjd)
try:
	print("TOC : ",Eph.tgps.st_iso_epoch())
except:
	print("Unable to find satellite")	
```
	
* Get all precise ephemerides for a satellite
	

```python
(orb,nl) = Orb.getSp3('G',5) 

# Satellite GPS, PRN 5
# 'G' : GPS, 'E' : Galileo, 'R' : Glonass

X = orb[:,1] # X coordinates at all sp3 epochs
Y = orb[:,2]
Z = orb[:,3]
```

### Satellite coordinates/clock processing

* Process of ECEF coordinates and clock error (dte) for a satellite given by its constellation ('G','E','R'), its PRN, an instant mjd and et possibly a degree for Lagrange processing (precise orbits).

```python
X, Y, Z, dte = Orb.calcSatCoord(const,PRN,mjd,degree)
```

A debug class object is implemented during coordinate processing. It contains all intermediaries results.

In order to get its attributes : 

```python
print(Orb.debug.__dict__)
```

* Process satellite clock error for a satellite given by its constellation ('G','E','R'), its PRN and an instant mjd. 

```python
dte = Orb.calcDte(const, PRN, mjd)
```

* Process satellite relativistic error for a satellite given by its constellation ('G','E','R'), its PRN and an instant mjd. 

```python
dt_relat = Orb.calcDtrelatNav(const, PRN, mjd)
```

## Rinex_o

### Structure

#### class rinex_o

|Attribute|Definition|
|:-|:-|
|type|rinex type, always "o"|
|headers| list of **header** objects|

#### class header

|Attribute|Definition|
|:-|:-|
|VERSION||
|TYPE||
|PGM||
|RUN_BY||
|OBSERVER||
|AGENCY||
|MARKER_NAME|marker name|
|MARKER_NUMBER|marker number|
|REC_N|receiver number|
|REC_TYPE|receiver type|
|REC_VERS|receiver version|
|ANT_N|antenna number|
|ANT_TYPE|antenna type|
|X|X approximate coordinate (m)|
|Y|Y approximate coordinate (m)|
|Z|Z approximate coordinate (m)|
|dH|up offset|
|dE|east offset|
|dN|north offset|
|WAVELENGTH_FACTOR||
|TYPE_OF_OBS|dictionary|
|TIME_OF_FIRST_OBS|time of first observation (gpsdatetime)|
|TIME_OF_LAST_OBS|time of last observation (gpsdatetime)|
|EPOCH_FLAG||
|epochs|list of **epoch** objects|

#### class epoch 

|Attribute|Definition|
|:-|:-|
|tgps|epoch date/time (gpsdatetime)|
|satellites|list of **sat** objects|

#### class sat

|Attribute|Definition|
|:-|:-|
|type||
|const|constellation, in [G;R;E]|
|PRN|Pseudo Random Noise|
|obs|dictionnary of observables|

### Data loading

Loading observation Rinex file (*.yyo)

```python
Rnx = rx.rinex_o()
Rnx.loadRinexO('smne1500.13o') 
```

### Data access

* Get epoch object for a given MJD :
```python
t=gpst.gpsdatetime()
t.rinex_t('13  5 30  1  0 30.0000000')
Ep = Rnx.getEpochByMjd(t.mjd)
```
* Get header object for a given MJD :
```python
Hd = Rnx.getHeaderByMjd(t.mjd)
```
* Get attribute from any header
```python
X0 = Hd.X
```
* Print all header or epoch informations
```python
print(Hd)
print(Ep)
```
* Get any observable from an epoch :
```python
C1 = Ep.getObs("C1","G", 31)
```
or 
```python
S = Ep.getSat("G", 31)
C1 = S.getObs("C1")
```
or (only for C/A code) 

```python
C1 = Ep.getSat("G", 31).C1
```
* Get all common data for 2 datasets at a given MJD
```python
Ep_base,Ep_rover = rinex_base.getCommonEpochs(rinex_rover, 56442)
```
## gnsstools

* toolGeoCartGRS80 : geographic to cartesian coordinates conversion. All angles should be given in radians.

```python
X,Y,Z = tools.toolGeoCartGRS80(lon,lat,h)
```
* toolCartGeoGRS80 : cartesian to geographic coordinates conversion. All angles are given in radians.
```python
lon,lat,h = tools.toolCartGeoGRS80(X,Y,Z)
```
* toolCartLocGRS80 : cartesian to topocentric coordinates conversion.
```python
x, y, z = tools.toolCartLocGRS80(X0,Y0,Z0,X,Y,Z)
```
* toolAzEle : azimut and elevation (radians) for one or several satellites Xs,Ys,Zs (scalar or vector) seen from a point with X,Y,Z  coordinates.
```python
Az, Ele = tools.toolAzEle(X,Y,Z,Xs,Ys,Zs)
```
* toolAzEleH : azimut, elevation (radians) and ellipsoidal height for one or several satellites Xs,Ys,Zs (scalar or vector) seen from a point with X,Y,Z  coordinates.
```python
Az, Ele, h = tools.toolAzEleH(X,Y,Z,Xs,Ys,Zs)
```
* toolRotX, toolRotY, toolRotZ : alpha radians rotation around X, Y ou Z axis.
```python
X,Y,Z =  tools.toolRotX(X,Y,Z,alpha)
```
* matCart2Local : matrix from cartesian to local coordinates. Longitudes and latitudes given in radians. 
```python
R =  tools.matCart2Local(lon, lat)
```

## gnss_process


* TrilatGps : trilateration with 4 parameters (X,Y,Z,cdtr)
```python
X,Y,Z,cdtr,sigma0_2,V,Qxx = trilatGps(PosSat,Dobs,X0)
```
* TrilatGnss : trilateration with 4, 5 or 6 parameters (X,Y,Z,cdtr,[cGGTO,cGPGL])
```python
X,Y,Z,cdtr,cGGTO,cGPGL,sigma0_2,V,Qxx =  trilatGnss(PosSat,Dobs,X0,sat_index)
```
* TrilatGnssPonderationElev : trilateration with 4, 5 or 6 parameters (X,Y,Z,cdtr,[cGGTO,cGPGL]) avec with weighting given from elevation of each satellite.
```python
X,Y,Z,cdtr,cGGTO,cGPGL,sigma0_2,V,Qxx =  trilatGnssPonderationElev(PosSat,Dobs,X0,sat_index,ElevSat)
```


# Licence

Copyright (C) 2014-2025, Jacques Beilin - ENSG-Geomatics

Distributed under terms of the CECILL-C licence.
