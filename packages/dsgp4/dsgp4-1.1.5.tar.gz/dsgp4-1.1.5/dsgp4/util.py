import datetime
import numpy as np
import torch

def get_gravity_constants(gravity_constant_name):
    if gravity_constant_name == 'wgs-72old':
        mu     = 398600.79964        #  in km3 / s2
        radiusearthkm = 6378.135     #  km
        xke    = 0.0743669161
        tumin  = 1.0 / xke
        j2     =   0.001082616
        j3     =  -0.00000253881
        j4     =  -0.00000165597
        j3oj2  =  j3 / j2
    elif gravity_constant_name == 'wgs-72':
       mu     = 398600.8            #  in km3 / s2
       radiusearthkm = 6378.135     #  km
       xke    = 60.0 / np.sqrt(radiusearthkm*radiusearthkm*radiusearthkm/mu)
       tumin  = 1.0 / xke
       j2     =   0.001082616
       j3     =  -0.00000253881
       j4     =  -0.00000165597
       j3oj2  =  j3 / j2
    elif gravity_constant_name=="wgs-84":
       mu     = 398600.5            #  in km3 / s2
       radiusearthkm = 6378.137     #  km
       xke    = 60.0 / np.sqrt(radiusearthkm*radiusearthkm*radiusearthkm/mu)
       tumin  = 1.0 / xke
       j2     =   0.00108262998905
       j3     =  -0.00000253215306
       j4     =  -0.00000161098761
       j3oj2  =  j3 / j2
    else:
       raise RuntimeError("Supported gravity constant names: wgs-72, wgs-84, wgs-72old while "+gravity_constant_name+" was provided")

    return torch.tensor(tumin), torch.tensor(mu), torch.tensor(radiusearthkm), torch.tensor(xke), torch.tensor(j2), torch.tensor(j3), torch.tensor(j4), torch.tensor(j3oj2)

def propagate_batch(tles, tsinces, initialized=True):
    """
    This function takes a list of TLEs and a tensor of times (which must be of same length), and returns the corresponding states.
    
    Parameters:
    ----------------
    tles (``list`` of ``dsgp4.tle.TLE``): list of TLE objects to be propagated
    tsinces (``torch.tensor``): propagation times in minutes (it has to be a tensor of the same size of the list of TLEs)
    initialized (``bool``): whether the TLEs have been initialized or not (default: True

    Returns:
    ----------------
    state (``torch.tensor``): (Nx2x3) tensor representing position and velocity in km and km/s, where the first dimension is the batch size.
    """
    from .sgp4_batched import sgp4_batched
    if not initialized:
        _,tles=initialize_tle(tles)
    state=sgp4_batched(tles, tsinces)
    return state

def propagate(tle, tsinces, initialized=True):
    """
    This function takes a tensor of inputs and a TLE, and returns the corresponding state.
    In particular, multiple behaviors are supported:
    - if a single TLE is provided, then the function returns the state of the satellite at the requested time(s)
    - if a list of TLEs is provided, then the function returns the state of each satellite at the requested times

    In the second case, the length of the list of TLEs must be equal to the length of the tensor of times.
    
    Parameters:
    ----------------
    tle (``dsgp4.tle.TLE`` or ``list`` of ``dsgp4.tle.TLE``): TLE object or list of TLE objects to be propagated
    tsinces (``torch.tensor``): propagation times in minutes
    initialized (``bool``): whether the TLEs have been initialized or not (default: True)

    Returns:
    ----------------
    state (``torch.tensor``): (2x3) tensor representing position and velocity in km and km/s.
    """
    from .sgp4 import sgp4
    if not initialized:
        initialize_tle(tle)
    state=sgp4(tle, tsinces)
    return state

def initialize_tle(tles,
                   gravity_constant_name="wgs-84",
                   with_grad=False):
    """
    This function takes a single `dsgp4.tle.TLE` object or a list of `dsgp4.tle.TLE` objects and initializes the SGP4 propagator.
    This is a necessary step to be ran before propagating TLEs (e.g. before calling `propagate` function).
    
    Parameters:
    ----------------
    tles (``dsgp4.tle.TLE`` or ``list`` of ``dsgp4.tle.TLE``): TLE object or list of TLE objects to be initialized
    gravity_constant_name (``str``): name of the gravity constant to be used (default: "wgs-84")    
    with_grad (``bool``): whether to use gradients or not (default: False)
    
    Returns:
    ----------------
    tle_elements (``torch.tensor``): tensor of TLE parameters (especially useful to retrieve gradients, when `with_grad` is `True`)
    """
    from .sgp4init import sgp4init
    from .sgp4init_batch import sgp4init_batch
    whichconst=get_gravity_constants(gravity_constant_name)
    deep_space_counter=0
    if isinstance(tles,list):
        tle_elements=[]#torch.zeros((len(tles),9),requires_grad=with_grad)
        for tle in tles:
                x=torch.tensor([tle._bstar,
                            tle._ndot,
                            tle._nddot,
                            tle._ecco,
                            tle._argpo,
                            tle._inclo,
                            tle._mo,
                            tle._no_kozai,
                            tle._nodeo
                            ],requires_grad=with_grad)
                tle_elements.append(x)
        xx=torch.stack(tle_elements)
        try:
            tles_batch=tles[0].copy()
            sgp4init_batch(whichconst=whichconst,
                            opsmode='i',
                            satn=tle.satellite_catalog_number,
                            epoch=(tle._jdsatepoch+tle._jdsatepochF)-2433281.5,
                            xbstar=xx[:,0],
                            xndot=xx[:,1],
                            xnddot=xx[:,2],
                            xecco=xx[:,3],
                            xargpo=xx[:,4],
                            xinclo=xx[:,5],
                            xmo=xx[:,6],
                            xno_kozai=xx[:,7],
                            xnodeo=xx[:,8],
                            satellite_batch=tles_batch,
                            )
        except Exception as e:
            _error_string="Error: deep space propagation not supported (yet). The provided satellite has \
an orbital period above 225 minutes. If you want to let us know you need it or you want to \
contribute to implement it, open a PR or raise an issue at: https://github.com/esa/dSGP4."
            if str(e)==_error_string:
                deep_space_counter+=1
            else:
                raise e
        if deep_space_counter>0:
            print("Warning: "+str(deep_space_counter)+" TLEs were not initialized because they are in deep space. Deep space propagation is currently not supported.")
        return tle_elements, tles_batch

    else:
        tle_elements=torch.tensor([tles._bstar,
                                    tles._ndot,
                                    tles._nddot,
                                    tles._ecco,
                                    tles._argpo,
                                    tles._inclo,
                                    tles._mo,
                                    tles._no_kozai,
                                    tles._nodeo
                                    ],requires_grad=with_grad)
        sgp4init(whichconst=whichconst,
                            opsmode='i',
                            satn=tles.satellite_catalog_number,
                            epoch=(tles._jdsatepoch+tles._jdsatepochF)-2433281.5,
                            xbstar=tle_elements[0],
                            xndot=tle_elements[1],
                            xnddot=tle_elements[2],
                            xecco=tle_elements[3],
                            xargpo=tle_elements[4],
                            xinclo=tle_elements[5],
                            xmo=tle_elements[6],
                            xno_kozai=tle_elements[7],
                            xnodeo=tle_elements[8],
                            satellite=tles)
        return tle_elements

def from_year_day_to_date(y,d):
    """
    Converts a year and day of the year to a date.
    
    Parameters:
    ----------------
    y (``int``): year
    d (``int``): day of the year

    Returns:
    ----------------
    ``datetime.datetime``: date
    """
    return (datetime.datetime(y, 1, 1) + datetime.timedelta(d - 1))

def gstime(jdut1):
    """
    This function computes the Greenwich Sidereal Time (GST) at the given Julian Date (UT1).
    
    Parameters:
    ----------------
    jdut1 (``float``): Julian Date (UT1)

    Returns:
    ----------------
    ``float``: Greenwich Sidereal Time (GST)
    """
    tut1 = (jdut1 - 2451545.0) / 36525.0
    temp = -6.2e-6* tut1 * tut1 * tut1 + 0.093104 * tut1 * tut1 + \
         (876600.0*3600 + 8640184.812866) * tut1 + 67310.54841  #  sec
    temp = (temp*(np.pi/180.0) / 240.0) % (2*np.pi) # 360/86400 = 1/240, to deg, to rad

     #  ------------------------ check quadrants ---------------------
    temp=torch.where(temp<0., temp+(2*np.pi), temp)
    return temp

def clone_w_grad(y):
    """
    This function takes a tensor and returns a copy of it with gradients.
    
    Parameters:
    ----------------
    y (``torch.tensor``): tensor to clone

    Returns:
    ----------------
    ``torch.tensor``: tensor with gradients
    """
    return y.clone().detach().requires_grad_(True)

def jday(year, mon, day, hr, minute, sec):
    """
    Converts a date and time to a Julian Date. The Julian Date is the number of days since noon on January 1st, 4713 BC.
    
    Parameters:
    ----------------
    year (``int``): year
    mon (``int``): month
    day (``int``): day
    hr (``int``): hour
    minute (``int``): minute
    sec (``float``): second

    Returns:
    ----------------
    ``tuple``: Julian Date as integer and fractional part of the day
    """
    jd=(367.0 * year -
            7.0 * (year + ((mon + 9.0) // 12.0)) * 0.25 // 1.0 +
            275.0 * mon // 9.0 +
            day + 1721013.5)
    fr=(sec + minute * 60.0 + hr * 3600.0) / 86400.0
    return jd,fr

def invjday(jd):
    """
    Converts a Julian Date to a date and time. The Julian Date is the number of days since noon on January 1st, 4713 BC.
    
    Parameters:
    ----------------
    jd (``float``): Julian Date

    Returns:
    ----------------
    ``tuple``: year, month, day, hour, minute, second
    """
    temp    = jd - 2415019.5
    tu      = temp / 365.25
    year    = 1900 + int(tu // 1.0)
    leapyrs = int(((year - 1901) * 0.25) // 1.0)
    days    = temp - ((year - 1900) * 365.0 + leapyrs) + 0.00000000001
    if (days < 1.0):
        year    = year - 1
        leapyrs = int(((year - 1901) * 0.25) // 1.0)
        days    = temp - ((year - 1900) * 365.0 + leapyrs)
    mon, day, hr, minute, sec = days2mdhms(year, days)
    sec = sec - 0.00000086400
    return year, mon, day, hr, minute, sec

def days2mdhms(year, fractional_day):
    """
    Converts a number of days to months, days, hours, minutes, and seconds.
    
    Parameters:
    ----------------
    year (``int``): year
    fractional_day (``float``): number of days

    Returns:
    ----------------
    ``tuple``: month, day, hour, minute, second
    """
    d=datetime.timedelta(days=fractional_day)
    datetime_obj=datetime.datetime(year-1,12,31)+d
    return datetime_obj.month, datetime_obj.day, datetime_obj.hour, datetime_obj.minute, datetime_obj.second+datetime_obj.microsecond/1e6

def from_string_to_datetime(string):
    """
    Converts a string to a datetime object.
    
    Parameters:
    ----------------
    string (``str``): string to convert

    Returns:
    ----------------
    ``datetime.datetime``: datetime object
    """
    if string.find('.')!=-1:
        return datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f')
    else:
        return datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

def from_mjd_to_epoch_days_after_1_jan(mjd_date):
    """
    Converts a Modified Julian Date to the number of days after 1 Jan 2000.
    
    Parameters:
    ----------------
    mjd_date (``float``): Modified Julian Date

    Returns:
    ----------------
    ``float``: number of days after 1 Jan 2000
    """
    d = from_mjd_to_datetime(mjd_date)
    dd = d - datetime.datetime(d.year-1, 12, 31)
    days = dd.days
    days_fraction = (dd.seconds + dd.microseconds/1e6) / (60*60*24)
    return days + days_fraction

def from_mjd_to_datetime(mjd_date):
    """
    Converts a Modified Julian Date to a datetime object. The Modified Julian Date is the number of days since midnight on November 17, 1858.
    
    Parameters:
    ----------------
    mjd_date (``float``): Modified Julian Date

    Returns:
    ----------------
    ``datetime.datetime``: datetime
    """
    jd_date=mjd_date+2400000.5
    return from_jd_to_datetime(jd_date)

def from_jd_to_datetime(jd_date):
    """
    Converts a Julian Date to a datetime object. The Julian Date is the number of days since noon on January 1st, 4713 BC.
    
    Parameters:
    ----------------
    jd_date (``float``): Julian Date

    Returns:
    ----------------
    ``datetime.datetime``: datetime
    """
    year, month, day, hour, minute, seconds=invjday(jd_date)
    e_1=datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=0)
    return e_1+datetime.timedelta(seconds=seconds)

def get_non_empty_lines(lines):
    """
    This function returns the non-empty lines of a list of lines.
    
    Parameters:
    ----------------
    lines (``list``): list of lines

    Returns:
    ----------------
    ``list``: list of non-empty lines
    """
    if not isinstance(lines, str):
        raise ValueError('Expecting a string')
    lines = lines.splitlines()
    lines = [line for line in lines if line.strip()]
    return lines

def from_datetime_to_fractional_day(datetime_object):
    """
    Converts a datetime object to a fractional day. The fractional day is the number of days since the beginning of the year. For example, January 1st is 0.0, January 2nd is 1.0, etc.
    
    Parameters:
    ----------------
    datetime_object (``datetime.datetime``): datetime object to convert

    Returns:
    ----------------
    ``float``: fractional day
    """
    d = datetime_object-datetime.datetime(datetime_object.year-1, 12, 31)
    fractional_day = d.days + d.seconds/60./60./24 + d.microseconds/60./60./24./1e6
    return fractional_day

def from_datetime_to_mjd(datetime_obj):
    """
    Converts a datetime object to a Modified Julian Date. The Modified Julian Date is the number of days since midnight on November 17, 1858.
    
    Parameters:
    ----------------
    datetime_obj (``datetime.datetime``): datetime object to convert

    Returns:
    ----------------
    ``float``: Modified Julian Date
    """
    return from_datetime_to_jd(datetime_obj)-2400000.5

def from_datetime_to_jd(datetime_obj):
    """
    Converts a datetime object to a Julian Date. The Julian Date is the number of days since noon on January 1, 4713 BC.
    
    Parameters:
    ----------------
    datetime_obj (``datetime.datetime``): datetime object to convert

    Returns:
    ----------------
    ``float``: Julian Date
    """
    return sum(jday(year=datetime_obj.year, mon=datetime_obj.month, day=datetime_obj.day, hr=datetime_obj.hour, minute=datetime_obj.minute, sec=datetime_obj.second+float('0.'+str(datetime_obj.microsecond))))

def from_cartesian_to_keplerian(r_vec, v_vec, mu):
    """
    This function converts the provided state from Cartesian to Keplerian elements.

    Parameters:
    ----------------
    r_vec (``np.array``): position vector in Cartesian coordinates
    v_vec (``np.array``): velocity vector in Cartesian coordinates
    mu (``float``): gravitational parameter of the central body

    Returns:
    ----------------
    ``np.array``: array of Keplerian elements: (a, e, i, Omega, omega, M)
                                             (i.e., semi-major axis, eccentricity, inclination,
                                             right ascension of ascending node, argument of perigee,
                                             mean anomaly). All the angles are in radians, eccentricity is unitless
                                             and semi-major axis is in SI.
    """
    # Norms
    r = np.linalg.norm(r_vec)
    v = np.linalg.norm(v_vec)
    
    # Angular momentum vector and its magnitude
    h_vec = np.cross(r_vec, v_vec)
    h = np.linalg.norm(h_vec)
    
    # Inclination
    i = np.arccos(h_vec[2] / h) if h != 0 else 0
    
    # Node vector
    K = np.array([0, 0, 1])
    n_vec = np.cross(K, h_vec)
    n = np.linalg.norm(n_vec)
    
    # Eccentricity vector
    e_vec = (1/mu) * ((v**2 - mu/r) * r_vec - np.dot(r_vec, v_vec) * v_vec)
    e = np.linalg.norm(e_vec)

    # Semi-major axis (a)
    energy = v**2 / 2 - mu / r
    if abs(e - 1.0) > 1e-8:  # Elliptical or hyperbolic orbit
        a = -mu / (2 * energy)
    else:  # Parabolic orbit
        a = np.inf

    # Right ascension of ascending node (RAAN)
    Omega = 0
    if n != 0:
        Omega = np.arccos(n_vec[0] / n) if n_vec[1] >= 0 else 2 * np.pi - np.arccos(n_vec[0] / n)

    # Argument of perigee (ω)
    omega = 0
    if n != 0 and e != 0:
        omega = np.arccos(np.dot(n_vec, e_vec) / (n * e)) if e_vec[2] >= 0 else 2 * np.pi - np.arccos(np.dot(n_vec, e_vec) / (n * e))

    # True anomaly (ν)
    nu = 0
    if e != 0:
        nu = np.arccos(np.dot(e_vec, r_vec) / (e * r)) if np.dot(r_vec, v_vec) >= 0 else 2 * np.pi - np.arccos(np.dot(e_vec, r_vec) / (e * r))

    # Eccentric anomaly (E) and Mean anomaly (M)
    if e < 1.0:  # Elliptical orbit
        E = 2 * np.arctan(np.tan(nu / 2) * np.sqrt((1 - e) / (1 + e)))
        M = E - e * np.sin(E)
    elif e > 1.0:  # Hyperbolic orbit
        F = 2 * np.arctanh(np.tan(nu / 2) * np.sqrt((e - 1) / (e + 1)))
        M = e * np.sinh(F) - F
    else:  # Parabolic orbit
        M = np.nan  # Mean anomaly is undefined for parabolic orbits

    # Normalize angles to [0, 2π)
    Omega %= 2 * np.pi
    omega %= 2 * np.pi
    M %= 2 * np.pi

    return np.array([a, e, i, Omega, omega, M])
