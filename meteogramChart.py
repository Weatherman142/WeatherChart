#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

import modules.URLhandler as URLhandler
import modules.timeHandler as timeHandler


# In[ ]:


# Rounding is performed because the NWS API can't handle precision higher than 4 places.
#lat = round(float(input("Enter the latitude of the city (e.g. Ames: 42.00, KOWA: 44.12):")), 4)
#lon = round(float(input("Enter the longitude of the city (e.g. Ames: -93.62, KOWA: -93.26):")), 4)

# Floater City:
#lat = 48.8534951
#lon = 2.3483915

# Reno, NV:
#lat = 39.48389
#lon = -119.77111

# Herriman, UT:
#lat = 40.51060
#lon = -112.05400

# Owatonna:
#lat = 44.12333
#lon = -93.26056

# Ames:
lat = 42.03470
lon = -93.61990

placeName = " for " + str(round(lat, 3)) + "°, " + str(round(lon, 3)) + "°"

saveImage = False

# Dark mode control settings.
darkMode = False
backgroundColor = "xkcd:dark"
axisColor = "xkcd:light grey"


# In[3]:


# General weather variable names that apply to all of the models.
# Naming here makes it much easier to handle in the event I want to change the names or the API changes.
modelName = "modelName"
timeName = "timestamp"

temperatureName = "temperature_2m"
dewpointName = "dew_point_2m"
rhName = "relative_humidity_2m"
feelsLikeName = "apparent_temperature"
cloudCoverName = "cloud_cover"

windSpeedName = "wind_speed_10m"
windGustsName = "wind_gusts_10m"
windDirName = "wind_direction_10m"
pressureMSLname = "pressure_msl"

rainName = "rain"
snowName = "snowfall"
rainTotalName = "rainTotals"
snowTotalName = "snowTotals"

CAPErawName = "cape"
CAPEname = "capeEdit"
CINname = "convective_inhibition"
LCLname = "lcl"

colorName = "lineColor"
linewidthName = "linewidth"


# In[4]:


# Names of variables relevant to the storm-relative helicity math.
SRH1name = "SRH1_values"
SRH3name = "SRH3_values"
EHIname = "energy_helicity_index"
STPname = "significant_tornado_parameter"

d1000hPa = "wind_direction_1000hPa"
d975hPa = "wind_direction_975hPa"
d950hPa = "wind_direction_950hPa"
d925hPa = "wind_direction_925hPa"
d900hPa = "wind_direction_900hPa"
d850hPa = "wind_direction_850hPa"
d700hPa = "wind_direction_700hPa"
d500hPa = "wind_direction_500hPa"

s1000hPa = "wind_speed_1000hPa"
s975hPa = "wind_speed_975hPa"
s950hPa = "wind_speed_950hPa"
s925hPa = "wind_speed_925hPa"
s900hPa = "wind_speed_900hPa"
s850hPa = "wind_speed_850hPa"
s700hPa = "wind_speed_700hPa"
s500hPa = "wind_speed_500hPa"


# In[5]:


# Model names as defined by the open-meteo API.
GFSname = "gfs_global"
HRRRname = "gfs_hrrr"
NBMname = "ncep_nbm_conus"
GFS_GCname = "gfs_graphcast025"

ECMWFname = "ecmwf_ifs025"
ECMWF_AIname = "ecmwf_aifs025"

GEMname = "gem_seamless"
GDPSname = "gem_global"
RDPSname = "gem_regional"
HRDPSname = "gem_hrdps_continental"

ICONname = "icon_seamless"

UKMETname = "ukmo_seamless"

BOMname = "bom_access_global"

KMAname = "kma_seamless"

ARPEGEname = "arpege_seamless"


# In[6]:


# Sets up the URL with the requested variables.
# Base of the URL used for the OpenMeteo API.
api_URL_base = "https://api.open-meteo.com/v1/forecast"

# Names of the variables requested from the API.
variableNames = "&hourly="+temperatureName+","+rhName+","+dewpointName+","+feelsLikeName+","+cloudCoverName+","+windSpeedName+","+windGustsName+","+windDirName+","+pressureMSLname+","+rainName+","+snowName+","+CAPErawName+","+CINname
SRH3variableNames = "&hourly="+s1000hPa+","+s925hPa+","+s850hPa+","+s700hPa+","+d1000hPa+","+d925hPa+","+d850hPa+","+d700hPa
SRH1variableNames = "&hourly="+s975hPa+","+s950hPa+","+s900hPa+","+s500hPa+","+d975hPa+","+d950hPa+","+d900hPa+","+d500hPa

# Names of the units the variables should be in.
variableUnits = "&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
SRH3variableUnits = "&wind_speed_unit=ms"
SRH1variableUnits = "&wind_speed_unit=ms"

# Enter in the number of forecast days. Must be an integer between 1 and 16.
forecastDays = str(int(10))

# Sets the latitude and longitude.
urlLatLon = "?latitude=" + str(lat) + "&longitude=" + str(lon)

# Combines the above variables.
api_URL_common = api_URL_base + urlLatLon + variableNames + variableUnits + "&forecast_days=" + forecastDays
api_URL_common_SRH3 = api_URL_base + urlLatLon + SRH3variableNames + SRH3variableUnits + "&forecast_days=" + forecastDays
api_URL_common_SRH1 = api_URL_base + urlLatLon + SRH1variableNames + SRH1variableUnits + "&forecast_days=" + forecastDays


# In[7]:


# NOAA model data (GFS, GFS_GC, HRRR, NBM) acquistion.
api_URL_NOAA = api_URL_common + "&models=" + GFSname + "," + HRRRname + "," + NBMname + "," + GFS_GCname

dataNOAA = URLhandler.URLcollectorJSON(api_URL_NOAA, "NOAA forecast data")


# In[8]:


# European Centre for Medium-Range Forecast model data (ECMWF, ECMWF_AI) acquistion.
api_URL_ECMWF = api_URL_common + "&models=" + ECMWFname + "," + ECMWF_AIname

dataECMWF = URLhandler.URLcollectorJSON(api_URL_ECMWF, "ECMWF forecast data")


# In[9]:


# Environment Canada model data (GDPS, RDPS, HDRPS) acquistion.
api_URL_GEM = api_URL_common + "&models=" + GDPSname + "," + RDPSname + "," + HRDPSname

dataGEM = URLhandler.URLcollectorJSON(api_URL_GEM, "GEM forecast data")


# In[10]:


# DWD model data (ICON) acquistion.
api_URL_DWD = api_URL_common + "&models=" + ICONname

dataDWD = URLhandler.URLcollectorJSON(api_URL_DWD, "DWD forecast data")


# In[11]:


# UK Met Office model data (UKMET) acquistion.
api_URL_UKMET = api_URL_common + "&models=" + UKMETname

dataUKMET = URLhandler.URLcollectorJSON(api_URL_UKMET, "UKMET forecast data")


# In[12]:


# Bureau of Meteorology model data (BOM) acquistion.
api_URL_BOM = api_URL_common + "&models=" + BOMname

dataBOM = URLhandler.URLcollectorJSON(api_URL_BOM, "BOM forecast data")


# In[13]:


# Korean Meteorological Agency model data (KMA) acquistion.
api_URL_KMA = api_URL_common + "&models=" + KMAname

dataKMA = URLhandler.URLcollectorJSON(api_URL_KMA, "KMA forecast data")


# In[14]:


# Meteo-France model data (ARPEGE) acquistion.
api_URL_ARPEGE = api_URL_common + "&models=" + ARPEGEname

dataARPEGE = URLhandler.URLcollectorJSON(api_URL_ARPEGE, "APREGE forecast data")


# In[15]:


# Storm-relative helicity (0-3 km) data acquistion.
api_URL_SRH3 = api_URL_common_SRH3 + "&models="+ECMWFname+","+GFSname+","+HRRRname+","+GEMname+","+ICONname+","+UKMETname+","+ARPEGEname

dataSRH3 = URLhandler.URLcollectorJSON(api_URL_SRH3, "SRH3 forecast data")


# In[16]:


# Storm-relative helicity (0-1 km) data acquistion.
api_URL_SRH1 = api_URL_common_SRH1 + "&models="+GFSname+","+HRRRname+","+GEMname+","+ICONname+","+UKMETname

dataSRH1 = URLhandler.URLcollectorJSON(api_URL_SRH1, "SRH1 forecast data")


# In[17]:


dataLength = max(len(dataNOAA['hourly']['time']), len(dataECMWF['hourly']['time']),  len(dataGEM['hourly']['time']),  \
                 len(dataDWD['hourly']['time']),  len(dataUKMET['hourly']['time']),  len(dataBOM['hourly']['time']),  \
                 len(dataKMA['hourly']['time']),  len(dataARPEGE['hourly']['time']), len(dataSRH3['hourly']['time']), \
                 len(dataSRH1['hourly']['time']))


# In[18]:


# Common dictionary format for all forecasts.
# modelName, colorName, and linewidthName are identical for all values.
dictForecast = {modelName:       [None]*dataLength,
                timeName:        [None]*dataLength,
                temperatureName: [None]*dataLength,
                dewpointName:    [None]*dataLength,
                rhName:          [None]*dataLength,
                feelsLikeName:   [None]*dataLength,
                cloudCoverName:  [None]*dataLength,
                windDirName:     [None]*dataLength,
                windSpeedName:   [None]*dataLength,
                windGustsName:   [None]*dataLength,
                pressureMSLname: [None]*dataLength,
                rainName:        [None]*dataLength,
                snowName:        [None]*dataLength,
                rainTotalName:   [None]*dataLength,
                snowTotalName:   [None]*dataLength,
                CAPErawName:     [None]*dataLength,
                CAPEname:        [None]*dataLength,
                CINname:         [None]*dataLength,
                LCLname:         [None]*dataLength,
                SRH1name:        [None]*dataLength,
                SRH3name:        [None]*dataLength,
                s1000hPa:        [None]*dataLength,
                s975hPa:         [None]*dataLength,
                s950hPa:         [None]*dataLength,
                s925hPa:         [None]*dataLength,
                s900hPa:         [None]*dataLength,
                s850hPa:         [None]*dataLength,
                s700hPa:         [None]*dataLength,
                s500hPa:         [None]*dataLength,
                d1000hPa:        [None]*dataLength,
                d975hPa:         [None]*dataLength,
                d950hPa:         [None]*dataLength,
                d925hPa:         [None]*dataLength,
                d900hPa:         [None]*dataLength,
                d850hPa:         [None]*dataLength,
                d700hPa:         [None]*dataLength,
                d500hPa:         [None]*dataLength,
                EHIname:         [None]*dataLength,
                STPname:         [None]*dataLength,
                colorName:       [None]*dataLength,
                linewidthName:   [None]*dataLength}

# Creates the data frames that are used for storing model data.
GFSdataframe = pd.DataFrame(dictForecast)
GFS_GCdataframe = pd.DataFrame(dictForecast)
HRRRdataframe = pd.DataFrame(dictForecast)
NBMdataframe = pd.DataFrame(dictForecast)

ECMWFdataframe = pd.DataFrame(dictForecast)
ECMWF_AIdataframe = pd.DataFrame(dictForecast)

GDPSdataframe = pd.DataFrame(dictForecast)
RDPSdataframe = pd.DataFrame(dictForecast)
HRDPSdataframe = pd.DataFrame(dictForecast)

ICONdataframe = pd.DataFrame(dictForecast)

UKMETdataframe = pd.DataFrame(dictForecast)

BOMdataframe = pd.DataFrame(dictForecast)

KMAdataframe = pd.DataFrame(dictForecast)

ARPEGEdataframe = pd.DataFrame(dictForecast)

# Used for the mean of the variables.
meanDataframe = pd.DataFrame(dictForecast)


# In[19]:


# Severe parameter calculation (SRH, EHI, LCL, STP).
# Storm-Relative Helicity (0-3 km) calculation.
def SRH3calculator(SRH3dataframe):
    SRH3valueList = []
    for i in range(len(SRH3dataframe)):
        # Calculate vectors for the chosen layers at a given timestep i.
        vector1000 = (-SRH3dataframe[s1000hPa][i] * np.sin(np.deg2rad(SRH3dataframe[d1000hPa][i])), \
                      -SRH3dataframe[s1000hPa][i] * np.cos(np.deg2rad(SRH3dataframe[d1000hPa][i])))
        vector925 = (-SRH3dataframe[s925hPa][i] * np.sin(np.deg2rad(SRH3dataframe[d925hPa][i])), \
                     -SRH3dataframe[s925hPa][i] * np.cos(np.deg2rad(SRH3dataframe[d925hPa][i])))
        vector850 = (-SRH3dataframe[s850hPa][i] * np.sin(np.deg2rad(SRH3dataframe[d850hPa][i])), \
                     -SRH3dataframe[s850hPa][i] * np.cos(np.deg2rad(SRH3dataframe[d850hPa][i])))
        vector700 = (-SRH3dataframe[s700hPa][i] * np.sin(np.deg2rad(SRH3dataframe[d700hPa][i])), \
                     -SRH3dataframe[s700hPa][i] * np.cos(np.deg2rad(SRH3dataframe[d700hPa][i])))
        
        # Set the storm motion vector. In this case, 700 mb with a 0.75 speed multiplier and a 30° shift.
        stormMotionVector = (-SRH3dataframe[s700hPa][i] * 0.75 * np.sin(np.deg2rad(SRH3dataframe[d700hPa][i] + 30)), \
                             -SRH3dataframe[s700hPa][i] * 0.75 * np.cos(np.deg2rad(SRH3dataframe[d700hPa][i] + 30)))

        # Involved layers are marked with 3 numbers each for their pressures.
            # E.g.: 100925 = 1000 mb and 925 mb
        # Difference calculation between two levels.
        vector100925diff = (vector925[0] - vector1000[0], vector925[1] - vector1000[1])
        vector925850diff = (vector850[0] - vector925[0], vector850[1] - vector925[1])
        vector850700diff = (vector700[0] - vector850[0], vector700[1] - vector850[1])

        # Average between two levels with storm motion in account.
        vector100925SR = (((vector925[0] + vector1000[0]) / 2) - stormMotionVector[0], \
                          ((vector925[1] + vector1000[1]) / 2) - stormMotionVector[1])
        vector925850SR = (((vector850[0] + vector925[0]) / 2) - stormMotionVector[0], \
                          ((vector850[1] + vector925[1]) / 2) - stormMotionVector[1])
        vector850700SR = (((vector700[0] + vector850[0]) / 2) - stormMotionVector[0], \
                          ((vector700[1] + vector850[1]) / 2) - stormMotionVector[1])
        
        # Total SRH3 for this time step.
        SRH3total = (vector100925SR[1] * vector100925diff[0] - vector100925SR[0] * vector100925diff[1]) + \
                    (vector925850SR[1] * vector925850diff[0] - vector925850SR[0] * vector925850diff[1]) + \
                    (vector850700SR[1] * vector850700diff[0] - vector850700SR[0] * vector850700diff[1])
        
        # Appends this timestep's SRH3 value to the list used for plotting.
        SRH3valueList.append(SRH3total)

    return SRH3valueList


# Storm-Relative Helicity (0-1 km) calculation.
def SRH1calculator(SRH1dataframe):
    SRH1valueList = []
    for i in range(len(SRH1dataframe)):
        # Calculate vectors for the chosen layers at a given timestep i.
        vector1000 = (-SRH1dataframe[s1000hPa][i] * np.sin(np.deg2rad(SRH1dataframe[d1000hPa][i])), \
                      -SRH1dataframe[s1000hPa][i] * np.cos(np.deg2rad(SRH1dataframe[d1000hPa][i])))
        vector975 = (-SRH1dataframe[s975hPa][i] * np.sin(np.deg2rad(SRH1dataframe[d975hPa][i])), \
                     -SRH1dataframe[s975hPa][i] * np.cos(np.deg2rad(SRH1dataframe[d975hPa][i])))
        vector950 = (-SRH1dataframe[s950hPa][i] * np.sin(np.deg2rad(SRH1dataframe[d950hPa][i])), \
                     -SRH1dataframe[s950hPa][i] * np.cos(np.deg2rad(SRH1dataframe[d950hPa][i])))        
        vector925 = (-SRH1dataframe[s925hPa][i] * np.sin(np.deg2rad(SRH1dataframe[d925hPa][i])), \
                     -SRH1dataframe[s925hPa][i] * np.cos(np.deg2rad(SRH1dataframe[d925hPa][i])))
        vector900 = (-SRH1dataframe[s900hPa][i] * np.sin(np.deg2rad(SRH1dataframe[d900hPa][i])), \
                     -SRH1dataframe[s900hPa][i] * np.cos(np.deg2rad(SRH1dataframe[d900hPa][i])))
        
        # Set the storm motion vector. In this case, 700 mb with a 0.75 speed multiplier and a 30° shift.
        stormMotionVector = (-SRH1dataframe[s700hPa][i] * 0.75 * np.sin(np.deg2rad(SRH1dataframe[d700hPa][i] + 30)), \
                             -SRH1dataframe[s700hPa][i] * 0.75 * np.cos(np.deg2rad(SRH1dataframe[d700hPa][i] + 30)))

        # Involved layers are marked with 3 numbers each for their pressures.
            # E.g.: 100975 = 1000 mb and 975 mb
        # Difference calculation between two levels.
        vector100975diff = (vector975[0] - vector1000[0], vector975[1] - vector1000[1])
        vector975950diff = (vector950[0] - vector975[0], vector950[1] - vector975[1])
        vector950925diff = (vector925[0] - vector950[0], vector925[1] - vector950[1])
        vector925900diff = (vector900[0] - vector925[0], vector900[1] - vector925[1])

        # Average between two levels with storm motion in account.
        vector100975SR = (((vector975[0] + vector1000[0]) / 2) - stormMotionVector[0], \
                          ((vector975[1] + vector1000[1]) / 2) - stormMotionVector[1])
        vector975950SR = (((vector950[0] + vector975[0]) / 2) - stormMotionVector[0], \
                          ((vector950[1] + vector975[1]) / 2) - stormMotionVector[1])
        vector950925SR = (((vector925[0] + vector950[0]) / 2) - stormMotionVector[0], \
                          ((vector925[1] + vector950[1]) / 2) - stormMotionVector[1])
        vector925900SR = (((vector900[0] + vector925[0]) / 2) - stormMotionVector[0], \
                          ((vector900[1] + vector925[1]) / 2) - stormMotionVector[1])
        
        # Total SRH3 for this time step.
        SRH1total = (vector100975SR[1] * vector100975diff[0] - vector100975SR[0] * vector100975diff[1]) + \
                    (vector975950SR[1] * vector975950diff[0] - vector975950SR[0] * vector975950diff[1]) + \
                    (vector950925SR[1] * vector950925diff[0] - vector950925SR[0] * vector950925diff[1]) + \
                    (vector925900SR[1] * vector925900diff[0] - vector925900SR[0] * vector925900diff[1])
        
        # Appends this timestep's SRH3 value to the list used for plotting.
        SRH1valueList.append(SRH1total)

    return SRH1valueList


# Energy-Helicity Index calculation.
def EHIcalculator(dataFrameIn):
    EHIvalueList = []
    for i in range(len(dataFrameIn)):
        EHIvalue = (dataFrameIn[SRH3name][i] * dataFrameIn[CAPEname][i]) / 166000
        if(EHIvalue >= 0):
            EHIvalueList.append(EHIvalue)
        else:
            EHIvalueList.append(0)

    return EHIvalueList


# Lifted Condensation Level approximation.
def LCLcalculator(dataFrameIn):
    LCLvalueList = []
    for i in range(len(dataFrameIn)):
        # The difference between the dry adiabatic and dew point lapse rates is around 8 K/km.
        # 8 K/km = 125 m/K = 69.44 m/°F
        LCLvalue = 69.44 * (dataFrameIn[temperatureName][i] - dataFrameIn[dewpointName][i])
        LCLvalueList.append(LCLvalue)

    return LCLvalueList


# Significant Tornado Parameter calculation.
def STPcalculator(dataFrameIn):
    STPvalueList = []
    for i in range(len(dataFrameIn)):
        CAPEterm = dataFrameIn[CAPEname][i] / 1500

        if(dataFrameIn[LCLname][i] < 1000):
            LCLterm = 1.0
        elif(dataFrameIn[LCLname][i] > 2000):
            LCLterm = 0.0
        else:
            LCLterm = (2000 - dataFrameIn[LCLname][i]) / 1000

        SRHterm = dataFrameIn[SRH1name][i] / 150

        vector1000 = (-dataFrameIn[s1000hPa][i] * np.sin(np.deg2rad(dataFrameIn[d1000hPa][i])), \
                      -dataFrameIn[s1000hPa][i] * np.cos(np.deg2rad(dataFrameIn[d1000hPa][i])))
        vector500  = (-dataFrameIn[s500hPa][i] * np.sin(np.deg2rad(dataFrameIn[d500hPa][i])), \
                      -dataFrameIn[s500hPa][i] * np.cos(np.deg2rad(dataFrameIn[d500hPa][i])))
        vectorBWD = (vector500[0] - vector1000[0], vector500[1] - vector1000[1])
        BWDval = abs(pow(pow(vectorBWD[0], 2) + pow(vectorBWD[1], 2), 0.5))
        if(BWDval > 30):
            BWDterm = 1.5
        elif(BWDval < 12.5):
            BWDterm = 0.0
        else:
            BWDterm = BWDval / 20.0 

        if(dataFrameIn[CINname][i] > -50):
            CINterm = 1.0
        elif(dataFrameIn[CINname][i] < -200):
            CINterm = 0.0
        else:
            CINterm = (200.0 + dataFrameIn[CINname][i]) / 150.0

        STPvalue = CAPEterm * LCLterm * SRHterm * BWDterm * CINterm
        if(STPvalue >= 0):
            STPvalueList.append(STPvalue)
        else:
            STPvalueList.append(0)

    return STPvalueList


# In[20]:


# DataFrameManager function and related functions.
# Checks input to see if is NoneType. Mainly used to handle None/null in precipitation.
def isValueNull(val):
    if(val == None or val == np.NaN):
        return np.NaN
    else:
        return val


# Because CAPE needs to be handled a little differently, needs a different function.
def isValueNullCAPE(val):
    if(val == None or val == np.NaN):
        return 0
    elif(val <= -300):
        return -300
    else:
        return val
    

# Manages the DataFrames in a single function rather than across the program.
def dataFrameManager(dataFrameIn, dataFrameOut, modelName):
    # Some models, do not have the model name included in the variable names.
    # The models with names require an underscore between the variable and model name.
    if(len(modelName) != 0):
        modelName = "_" + modelName
    
    dataFrameOut[timeName]        = dataFrameIn['hourly']['time']
    dataFrameOut[temperatureName] = dataFrameIn['hourly'][str(temperatureName + modelName)]
    dataFrameOut[dewpointName]    = dataFrameIn['hourly'][str(dewpointName + modelName)]
    dataFrameOut[rhName]          = dataFrameIn['hourly'][str(rhName + modelName)]
    dataFrameOut[feelsLikeName]   = dataFrameIn['hourly'][str(feelsLikeName + modelName)]
    dataFrameOut[cloudCoverName]  = dataFrameIn['hourly'][str(cloudCoverName + modelName)]

    dataFrameOut[windSpeedName]   = dataFrameIn['hourly'][str(windSpeedName + modelName)]
    dataFrameOut[windGustsName]   = dataFrameIn['hourly'][str(windGustsName + modelName)]
    dataFrameOut[windDirName]     = dataFrameIn['hourly'][str(windDirName + modelName)]
    dataFrameOut[pressureMSLname] = dataFrameIn['hourly'][str(pressureMSLname + modelName)]

    # The absolute value is needed due to issues with NBM snowfall accounting.
    # See open-meteo/open-meteo issue #1237.
    # Another issue: Some models (GFS, ECMWF_AI, ICON, GDPS, and KMA) have a special category for showers.
    # This is seperate from the normal rain category.
    dataFrameOut[rainName]        = [abs(isValueNull(x)) for x in dataFrameIn['hourly'][str(rainName + modelName)]]
    dataFrameOut[snowName]        = [abs(isValueNull(x)) for x in dataFrameIn['hourly'][str(snowName + modelName)]]
    # Accumulation totals.
    dataFrameOut[rainTotalName]   = np.cumsum(dataFrameOut[rainName])
    dataFrameOut[snowTotalName]   = np.cumsum(dataFrameOut[snowName])

    # isValueNull is needed for some models which return null instead of 0 CAPE.
    dataFrameOut[CAPErawName]     = [isValueNullCAPE(x) for x in dataFrameIn['hourly'][str(CAPErawName + modelName)]]
    dataFrameOut[CAPEname]        = [isValueNull(x) for x in dataFrameIn['hourly'][str(CAPErawName + modelName)]]
    dataFrameOut[CINname]         = [isValueNullCAPE(x) for x in dataFrameIn['hourly'][str(CINname + modelName)]]
    
    # Can't calculate LCL if you don't have dew point information.
    if(dataFrameOut[dewpointName][0] != None):
        dataFrameOut[LCLname] = LCLcalculator(dataFrameOut)

    return dataFrameOut


# Sets up the parts of the DataFrames needed for the SRH3 calculations.
def SRH3frameManager(dataFrameIn, dataFrameOut, modelName):
    if(len(modelName) != 0):
        modelName = "_" + modelName

    # Wind speed data at 1000, 925, 850, and 700 hPa.
    dataFrameOut[s1000hPa] = dataFrameIn['hourly'][str(s1000hPa + modelName)]
    dataFrameOut[s925hPa]  = dataFrameIn['hourly'][str(s925hPa + modelName)]
    dataFrameOut[s850hPa]  = dataFrameIn['hourly'][str(s850hPa + modelName)]
    dataFrameOut[s700hPa]  = dataFrameIn['hourly'][str(s700hPa + modelName)]

    # Wind direction data at 1000, 925, 850, and 700 hPa.
    dataFrameOut[d1000hPa] = dataFrameIn['hourly'][str(d1000hPa + modelName)]
    dataFrameOut[d925hPa]  = dataFrameIn['hourly'][str(d925hPa + modelName)]
    dataFrameOut[d850hPa]  = dataFrameIn['hourly'][str(d850hPa + modelName)]
    dataFrameOut[d700hPa]  = dataFrameIn['hourly'][str(d700hPa + modelName)]

    dataFrameOut[SRH3name] = SRH3calculator(dataFrameOut)
    dataFrameOut[EHIname]  = EHIcalculator(dataFrameOut)

    return dataFrameOut


# Sets up the parts of the DataFrames needed for the SRH1 calculations.
def SRH1frameManager(dataFrameIn, dataFrameOut, modelName):
    if(len(modelName) != 0):
        modelName = "_" + modelName

    dataFrameOut[s975hPa]  = dataFrameIn['hourly'][str(s975hPa + modelName)]
    dataFrameOut[s950hPa]  = dataFrameIn['hourly'][str(s950hPa + modelName)]
    dataFrameOut[s900hPa]  = dataFrameIn['hourly'][str(s900hPa + modelName)]
    dataFrameOut[s500hPa]  = dataFrameIn['hourly'][str(s500hPa + modelName)]

    dataFrameOut[d975hPa]  = dataFrameIn['hourly'][str(d975hPa + modelName)]
    dataFrameOut[d950hPa]  = dataFrameIn['hourly'][str(d950hPa + modelName)]
    dataFrameOut[d900hPa]  = dataFrameIn['hourly'][str(d900hPa + modelName)]
    dataFrameOut[d500hPa]  = dataFrameIn['hourly'][str(d500hPa + modelName)]

    dataFrameOut[SRH1name] = SRH1calculator(dataFrameOut)
    dataFrameOut[STPname]  = STPcalculator(dataFrameOut)

    return dataFrameOut


# In[21]:


linewidth = 0.80
NBMlinewidth = 1.25


# In[22]:


# NOAA model data (GFS, GFS_GC, HRRR, NBM) processing.
# First checks if the data exists in the DataFrame then runs the data frame manager(s) if so,
# then converts the timestamps into a usable format.
# Finally sets the name, line color, and line width for each.
# May add the NAM at a later date.

if('temperature_2m_gfs_global' in dataNOAA['hourly']):
    GFSdataframe = dataFrameManager(dataNOAA, GFSdataframe, GFSname)
    GFSdataframe = SRH3frameManager(dataSRH3, GFSdataframe, GFSname)
    GFSdataframe = SRH1frameManager(dataSRH1, GFSdataframe, GFSname)
    GFSdataframe[timeName] = timeHandler.timeParser(GFSdataframe[timeName])
    GFSdataframe[modelName] = "GFS"
    GFSdataframe[colorName] = "royalblue"
GFSdataframe[linewidthName] = linewidth
    
if('temperature_2m_gfs_graphcast025' in dataNOAA['hourly']):
    GFS_GCdataframe = dataFrameManager(dataNOAA, GFS_GCdataframe, GFS_GCname)
    GFS_GCdataframe[timeName] = timeHandler.timeParser(GFS_GCdataframe[timeName])
    GFS_GCdataframe[modelName] = "Graphcast"
    GFS_GCdataframe[colorName] = "lightskyblue"
GFS_GCdataframe[linewidthName] = linewidth

if('temperature_2m_gfs_hrrr' in dataNOAA['hourly']):
    HRRRdataframe = dataFrameManager(dataNOAA, HRRRdataframe, HRRRname)
    #HRRRdataframe = SRH3frameManager(dataSRH3, HRRRdataframe, HRRRname)
    #HRRRdataframe = SRH1frameManager(dataSRH1, HRRRdataframe, HRRRname)
    HRRRdataframe[timeName] = timeHandler.timeParser(HRRRdataframe[timeName])
    HRRRdataframe[modelName] = "HRRR"
    HRRRdataframe[colorName] = "forestgreen"
HRRRdataframe[linewidthName] = linewidth

if('temperature_2m_ncep_nbm_conus' in dataNOAA['hourly']):
    NBMdataframe = dataFrameManager(dataNOAA, NBMdataframe, NBMname)
    NBMdataframe[timeName] = timeHandler.timeParser(NBMdataframe[timeName])
    NBMdataframe[modelName] = "NBM"
    NBMdataframe[colorName] = "red"
NBMdataframe[linewidthName] = NBMlinewidth


# In[23]:


# European Centre for Medium-Range Forecast model data (ECMWF, ECMWF_AI) processing.
if('temperature_2m_ecmwf_ifs025' in dataECMWF['hourly']):
    ECMWFdataframe = dataFrameManager(dataECMWF, ECMWFdataframe, ECMWFname)
    ECMWFdataframe = SRH3frameManager(dataSRH3, ECMWFdataframe, ECMWFname)
    ECMWFdataframe[timeName] = timeHandler.timeParser(ECMWFdataframe[timeName])
    ECMWFdataframe[modelName] = "ECMWF"
    ECMWFdataframe[colorName] = "xkcd:golden yellow"
ECMWFdataframe[linewidthName] = linewidth

if('temperature_2m_ecmwf_aifs025' in dataECMWF['hourly']):
    ECMWF_AIdataframe = dataFrameManager(dataECMWF, ECMWF_AIdataframe, ECMWF_AIname)
    ECMWF_AIdataframe[timeName] = timeHandler.timeParser(ECMWF_AIdataframe[timeName])
    ECMWF_AIdataframe[modelName] = "ECMWF AI"
    ECMWF_AIdataframe[colorName] = "xkcd:pumpkin"
ECMWF_AIdataframe[linewidthName] = linewidth


# In[24]:


# Environment Canada model data (GDPS, RDPS, HDRPS) processing.
if('temperature_2m_gem_global' in dataGEM['hourly']):
    GDPSdataframe = dataFrameManager(dataGEM, GDPSdataframe, GDPSname)
    GDPSdataframe = SRH3frameManager(dataSRH3, GDPSdataframe, GEMname)
    GDPSdataframe[timeName] = timeHandler.timeParser(GDPSdataframe[timeName])
    GDPSdataframe[modelName] = "GPDS"
    GDPSdataframe[colorName] = "xkcd:lilac"
GDPSdataframe[linewidthName] = linewidth

if('temperature_2m_gem_regional' in dataGEM['hourly']):
    RDPSdataframe = dataFrameManager(dataGEM, RDPSdataframe, RDPSname)
    RDPSdataframe[timeName] = timeHandler.timeParser(RDPSdataframe[timeName])
    RDPSdataframe[modelName] = "RDPS"
    RDPSdataframe[colorName] = "xkcd:electric purple"
RDPSdataframe[linewidthName] = linewidth

if('temperature_2m_gem_hrdps_continental' in dataGEM['hourly']):
    HRDPSdataframe = dataFrameManager(dataGEM, HRDPSdataframe, HRDPSname)
    HRDPSdataframe[timeName] = timeHandler.timeParser(HRDPSdataframe[timeName])
    HRDPSdataframe[modelName] = "HRDPS"
    HRDPSdataframe[colorName] = "xkcd:faded purple"
HRDPSdataframe[linewidthName] = linewidth


# In[25]:


# DWD model data (ICON) processing.
if('temperature_2m' in dataDWD['hourly']):
    ICONdataframe = dataFrameManager(dataDWD, ICONdataframe, '')
    ICONdataframe = SRH3frameManager(dataSRH3, ICONdataframe, ICONname)
    ICONdataframe = SRH1frameManager(dataSRH1, ICONdataframe, ICONname)
    ICONdataframe[timeName] = timeHandler.timeParser(ICONdataframe[timeName])
    ICONdataframe[modelName] = "ICON"
    ICONdataframe[colorName] = "xkcd:mint"
ICONdataframe[linewidthName] = linewidth


# In[26]:


# UK Met Office model data (UKMET) processing.
if('temperature_2m' in dataUKMET['hourly']):
    UKMETdataframe = dataFrameManager(dataUKMET, UKMETdataframe, '')
    UKMETdataframe = SRH3frameManager(dataSRH3, UKMETdataframe, 'ukmo_seamless')
    UKMETdataframe = SRH1frameManager(dataSRH1, UKMETdataframe, 'ukmo_seamless')
    UKMETdataframe[timeName] = timeHandler.timeParser(UKMETdataframe[timeName])
    UKMETdataframe[modelName] = "UKMET"
    UKMETdataframe[colorName] = "xkcd:green grey"
UKMETdataframe[linewidthName] = linewidth


# In[27]:


# Bureau of Meteorology model data (BOM) processing.
if('temperature_2m' in dataBOM['hourly']):
    BOMdataframe = dataFrameManager(dataBOM, BOMdataframe, '')
    BOMdataframe[timeName] = timeHandler.timeParser(BOMdataframe[timeName])
    BOMdataframe[modelName] = "BOM"
    BOMdataframe[colorName] = "xkcd:muted blue"
BOMdataframe[linewidthName] = linewidth


# In[28]:


# Korean Meteorological Agency model data (KMA) processing.
if('temperature_2m' in dataKMA['hourly']):
    KMAdataframe = dataFrameManager(dataKMA, KMAdataframe, '')
    KMAdataframe[timeName] = timeHandler.timeParser(KMAdataframe[timeName])
    KMAdataframe[modelName] = "KMA"
    KMAdataframe[colorName] = "xkcd:carnation pink"
KMAdataframe[linewidthName] = linewidth


# In[29]:


# Meteo-France model data (ARPEGE) processing.
if('temperature_2m' in dataARPEGE['hourly']):
    ARPEGEdataframe = dataFrameManager(dataARPEGE, ARPEGEdataframe, '')
    ARPEGEdataframe = SRH3frameManager(dataSRH3, ARPEGEdataframe, ARPEGEname)
    ARPEGEdataframe[timeName] = timeHandler.timeParser(ARPEGEdataframe[timeName])
    ARPEGEdataframe[modelName] = "ARPEGE"
    ARPEGEdataframe[colorName] = "xkcd:tangerine"
ARPEGEdataframe[linewidthName] = linewidth


# In[30]:


# Sets up the timestamps, model name, color, and linewidth for the mean plots.
meanDataframe[timeName] = timeHandler.timeParser(GFSdataframe[timeName])
meanDataframe[modelName] = "Average"
meanDataframe[colorName] = "black" if not darkMode else axisColor
meanDataframe[linewidthName] = NBMlinewidth

meanMarkerStyle = dict(marker='.', markersize=meanDataframe[linewidthName][0]*2, linewidth=0, color=meanDataframe[colorName][0])


# In[31]:


# Sets which models are plotted and in what order.
dataFrameList = (ARPEGEdataframe,
                 KMAdataframe,
                 BOMdataframe,
                 UKMETdataframe,
                 ICONdataframe,
                 GDPSdataframe,
                 RDPSdataframe,
                 HRDPSdataframe,
                 GFSdataframe,
                 GFS_GCdataframe,
                 HRRRdataframe,
                 ECMWFdataframe,
                 ECMWF_AIdataframe,
                 NBMdataframe)


# Lists out the meteorological variables used.
variableList = (temperatureName,
                dewpointName,
                rhName,
                feelsLikeName,
                cloudCoverName,
                windSpeedName,
                windGustsName,
                windDirName,
                pressureMSLname,
                rainName,
                snowName,
                rainTotalName,
                snowTotalName,
                CAPEname,
                CINname,
                LCLname,
                SRH3name,
                SRH1name,
                EHIname,
                STPname)


# In[32]:


# Finds the mean of all of the variables for each time step.
# First increments through timestamps...
for count in range(dataLength):
    #...then increments through each weather variable...
    for weather in variableList:
        valueList = []
        #...finally increments through each model.
        for model in dataFrameList:
            if(model.loc[count, weather] != None):
                valueList.append(model[weather][count])
        meanDataframe.loc[count, weather] = np.nanmean(valueList)
#print(meanDataframe)

# Calculating the mean precipitation total from the mean rate results in a smoother graph.
meanDataframe[rainTotalName]   = np.cumsum(meanDataframe[rainName])
meanDataframe[snowTotalName]   = np.cumsum(meanDataframe[snowName])


# In[33]:


# Plots temperature, dew point, apparent temperature, relative humidity, and cloud cover.
plt.rcParams["figure.dpi"] = 300
plt.rcParams["xtick.labelsize"] = 8
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, figsize=(10,15))

# Sets the plot color to a darker value. Mainly useful at night.
if(darkMode):
    fig.patch.set(facecolor=backgroundColor)
    for i in [ax1, ax2, ax3, ax4, ax5]:
        i.set(facecolor=backgroundColor)
        i.spines['bottom'].set_color(axisColor)
        i.spines['top'].set_color(axisColor) 
        i.spines['right'].set_color(axisColor)
        i.spines['left'].set_color(axisColor)
        i.tick_params(axis='x', colors=axisColor)
        i.tick_params(axis='y', colors=axisColor, which='both')
        i.yaxis.label.set_color(axisColor)
        i.xaxis.label.set_color(axisColor)
        i.title.set_color(axisColor)
        
# Iterates through the list of DataFrames. Much easier to work with than listing all of them out.
# Then plots the average of all of the models.
# Plots 2-meter air temperatures.
for i in dataFrameList:
    ax1.plot(i[timeName], i[temperatureName], color=i[colorName][0], linewidth=i[linewidthName][0])
ax1.plot(meanDataframe[timeName], meanDataframe[temperatureName], **meanMarkerStyle)

# Plots 2-meter dew point temperatures.
# Some models (GFS-GC) lack dew point information.
for i in dataFrameList:
    ax2.plot(i[timeName], i[dewpointName], color=i[colorName][0], linewidth=i[linewidthName][0])
ax2.plot(meanDataframe[timeName], meanDataframe[dewpointName], **meanMarkerStyle)

# Plots 2-meter apparent ("feels like") temperatures.
# Some models (GFS-GC) lack apparent temperature information.
for i in dataFrameList:
    ax3.plot(i[timeName], i[feelsLikeName], color=i[colorName][0], linewidth=i[linewidthName][0])
ax3.plot(meanDataframe[timeName], meanDataframe[feelsLikeName], **meanMarkerStyle)

# Plots 2-meter relative humidities.
# Some models (GFS-GC) lack relative humidity information.
for i in dataFrameList:
    ax4.plot(i[timeName], i[rhName], color=i[colorName][0], linewidth=i[linewidthName][0])
ax4.plot(meanDataframe[timeName], meanDataframe[rhName], **meanMarkerStyle)

# Plots total cloud cover data.
for i in dataFrameList:
    ax5.plot(i[timeName], i[cloudCoverName], color=i[colorName][0], linewidth=i[linewidthName][0], label=i[modelName][0])
ax5.plot(meanDataframe[timeName], meanDataframe[cloudCoverName], **meanMarkerStyle, label=meanDataframe[modelName][0])


# Enables gridding.
ax1.grid(True)
ax2.grid(True)
ax3.grid(True)
ax4.grid(True)
ax5.grid(True)

# Sets y-labels and title.
ax1.set_title("Temperature and Dew Point" + placeName)
ax1.set_ylabel("Temperature (°F)")
ax2.set_ylabel("Dew Point (°F)")
ax3.set_ylabel("Apparent Temperature (°F)")
ax4.set_ylabel("Relative Humidity (%)")
ax5.set_ylabel("Cloud Cover (%)")

# Adjust the bounds of the plot to make it consistent.
plt.setp(ax1, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])
plt.setp(ax2, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])
plt.setp(ax3, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])
plt.setp(ax4, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]], ylim=[-5, 105])
plt.setp(ax5, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]], ylim=[-5, 105])

# Sets the legend and size of it.
leg = ax5.legend(loc=(0, -0.5), ncol=6)

if(saveImage):
    plt.savefig("images/thermo.png", bbox_inches="tight")


# In[34]:


# Plots wind speed, wind gust, wind direction, and sea-level pressure.
plt.rcParams["figure.dpi"] = 300
plt.rcParams["xtick.labelsize"] = 8
fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(10,9))

# Sets the plot color to a darker value. Mainly useful at night.
if(darkMode):
    fig.patch.set(facecolor=backgroundColor)
    for i in [ax1, ax2, ax3]:
        i.set(facecolor=backgroundColor)
        i.spines['bottom'].set_color(axisColor)
        i.spines['top'].set_color(axisColor) 
        i.spines['right'].set_color(axisColor)
        i.spines['left'].set_color(axisColor)
        i.tick_params(axis='x', colors=axisColor)
        i.tick_params(axis='y', colors=axisColor, which='both')
        i.yaxis.label.set_color(axisColor)
        i.xaxis.label.set_color(axisColor)
        i.title.set_color(axisColor)

# Iterates through the list of DataFrames. Much easier to work with than listing all of them out.
# Plots wind speed information.
for i in dataFrameList:
    ax1.plot(i[timeName], i[windSpeedName], color=i[colorName][0], linewidth=i[linewidthName][0])
    ax1.plot(i[timeName], i[windGustsName], color=i[colorName][0], linewidth=i[linewidthName][0]/1.5, linestyle="dotted")

# Plots wind direction information. Plots as dots due to the wrapping between 0° and 359.9°.
# Mean wind direction is not plotted due to inherent issues with calculating the mean.
for i in dataFrameList:
    markerStyle = dict(marker='.', markersize=i[linewidthName][0]*5, linewidth=0)
    ax2.plot(i[timeName], i[windDirName], color=i[colorName][0], **markerStyle)

# Plots sea-level pressure data.
for i in dataFrameList:
    ax3.plot(i[timeName], i[pressureMSLname], color=i[colorName][0], linewidth=i[linewidthName][0], label=i[modelName][0])
ax3.plot(meanDataframe[timeName], meanDataframe[pressureMSLname], **meanMarkerStyle)

ax1.grid(True)
ax2.grid(True)
ax3.grid(True)

ax1.set_title("Wind Forecast Data" + placeName)
ax1.set_ylabel("Wind Speed/Gusts (mph)")
ax2.set_ylabel("Wind Direction (°)")
ax3.set_ylabel("Sea-Level Pressure (hPa)")

plt.setp(ax1, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])
plt.setp(ax2, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]], ylim=[0, 360])
plt.setp(ax3, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])

leg = ax3.legend(loc=(0, -0.5), ncol=6)

if(saveImage):
    plt.savefig("images/wind.png", bbox_inches="tight")


# In[35]:


# Plots rainfall, snowfall, rain accumulation, and snow accumulation.
plt.rcParams["figure.dpi"] = 300
plt.rcParams["xtick.labelsize"] = 8
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, figsize=(10,12))

# Sets the plot color to a darker value. Mainly useful at night.
if(darkMode):
    fig.patch.set(facecolor=backgroundColor)
    for i in [ax1, ax2, ax3, ax4]:
        i.set(facecolor=backgroundColor)
        i.spines['bottom'].set_color(axisColor)
        i.spines['top'].set_color(axisColor) 
        i.spines['right'].set_color(axisColor)
        i.spines['left'].set_color(axisColor)
        i.tick_params(axis='x', colors=axisColor)
        i.tick_params(axis='y', colors=axisColor, which='both')
        i.yaxis.label.set_color(axisColor)
        i.xaxis.label.set_color(axisColor)
        i.title.set_color(axisColor)

# Iterates through the list of DataFrames. Much easier to work with than listing all of them out.
# Plots rainfall rate information.
for i in dataFrameList:
    ax1.plot(i[timeName], i[rainName], color=i[colorName][0], linewidth=i[linewidthName][0])
ax1.plot(meanDataframe[timeName], meanDataframe[rainName], **meanMarkerStyle)

# Plots snowfall rate information.
for i in dataFrameList:
    ax2.plot(i[timeName], i[snowName], color=i[colorName][0], linewidth=i[linewidthName][0])
ax2.plot(meanDataframe[timeName], meanDataframe[snowName], **meanMarkerStyle)

# Plots rain accumulation.
for i in dataFrameList:
    ax3.plot(i[timeName], i[rainTotalName], color=i[colorName][0], linewidth=i[linewidthName][0])
ax3.plot(meanDataframe[timeName], meanDataframe[rainTotalName], **meanMarkerStyle)

# Plots snow accumulation.
for i in dataFrameList:
    ax4.plot(i[timeName], i[snowTotalName], color=i[colorName][0], linewidth=i[linewidthName][0], label=i[modelName][0])
ax4.plot(meanDataframe[timeName], meanDataframe[snowTotalName], **meanMarkerStyle, label=meanDataframe[modelName][0])

# Enables grids.
ax1.grid(True)
ax2.grid(True)
ax3.grid(True)
ax4.grid(True)

ax1.set_title("Precipitation Totals" + placeName)
ax1.set_ylabel("Rain Rate (in/hr)")
ax2.set_ylabel("Snow Rate (in/hr)")
ax3.set_ylabel("Rain Total (inches)")
ax4.set_ylabel("Snow Total (inches)")

plt.setp(ax1, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])
plt.setp(ax2, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])
plt.setp(ax3, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])
plt.setp(ax4, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])

leg = ax4.legend(loc=(0, -0.5), ncol=6)

if(saveImage):
    plt.savefig("images/precip.png", bbox_inches="tight")


# In[36]:


# Plots CAPE, CIN, SRH1, SRH3, LCL height, EHI, and STP.
plt.rcParams["figure.dpi"] = 300
plt.rcParams["xtick.labelsize"] = 8
fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = plt.subplots(7, figsize=(10,21))

# Sets the plot color to a darker value. Mainly useful at night.
if(darkMode):
    fig.patch.set(facecolor=backgroundColor)
    for i in [ax1, ax2, ax3, ax4, ax5, ax6, ax7]:
        i.set(facecolor=backgroundColor)
        i.spines['bottom'].set_color(axisColor)
        i.spines['top'].set_color(axisColor) 
        i.spines['right'].set_color(axisColor)
        i.spines['left'].set_color(axisColor)
        i.tick_params(axis='x', colors=axisColor)
        i.tick_params(axis='y', colors=axisColor, which='both')
        i.yaxis.label.set_color(axisColor)
        i.xaxis.label.set_color(axisColor)
        i.title.set_color(axisColor)

# Iterates through the list of DataFrames. Much easier to work with than listing all of them out.
# Plots Convective Available Potential Energy (CAPE).
for i in dataFrameList:
    ax1.plot(i[timeName], i[CAPErawName], color=i[colorName][0], linewidth=i[linewidthName][0])
ax1.plot(meanDataframe[timeName], meanDataframe[CAPEname], **meanMarkerStyle)

# Plots Convective Inhibition (CIN).
markerStyle = dict(marker='.', markersize=4, linewidth=0)
for i in dataFrameList:
    ax2.plot(i[timeName], i[CINname], color=i[colorName][0], linewidth=i[linewidthName][0])
ax2.plot(meanDataframe[timeName], meanDataframe[CINname], **meanMarkerStyle)

# Plots Storm-Relative Helicity (SRH1).
for i in dataFrameList:
    ax3.plot(i[timeName], i[SRH1name], color=i[colorName][0], linewidth=i[linewidthName][0], label=i[modelName][0])
ax3.plot(meanDataframe[timeName], meanDataframe[SRH1name], **meanMarkerStyle)

# Plots Storm-Relative Helicity (SRH3).
for i in dataFrameList:
    ax4.plot(i[timeName], i[SRH3name], color=i[colorName][0], linewidth=i[linewidthName][0], label=i[modelName][0])
ax4.plot(meanDataframe[timeName], meanDataframe[SRH3name], **meanMarkerStyle)

# Plots LCL height.
for i in dataFrameList:
    ax5.plot(i[timeName], i[LCLname], color=i[colorName][0], linewidth=i[linewidthName][0])
ax5.plot(meanDataframe[timeName], meanDataframe[LCLname], **meanMarkerStyle)

# Plots Energy-Helicity Index (EHI).
for i in dataFrameList:
    ax6.plot(i[timeName], i[EHIname], color=i[colorName][0], linewidth=i[linewidthName][0])
ax6.plot(meanDataframe[timeName], meanDataframe[EHIname], **meanMarkerStyle)

# Plots Significant Tornado Parameter (STP).
for i in dataFrameList:
    ax7.plot(i[timeName], i[STPname], color=i[colorName][0], linewidth=i[linewidthName][0], label=i[modelName][0])
ax7.plot(meanDataframe[timeName], meanDataframe[STPname], **meanMarkerStyle, label=meanDataframe[modelName][0])

ax1.grid(True)
ax2.grid(True)
ax3.grid(True)
ax4.grid(True)
ax5.grid(True)
ax6.grid(True)
ax7.grid(True)

ax1.set_title("Severe Forecast Data" + placeName)
ax1.set_ylabel("CAPE (J/kg)")
ax2.set_ylabel("CIN (J/kg)")
ax3.set_ylabel("SRH1 (m^2/s^2)")
ax4.set_ylabel("SRH3 (m^2/s^2)")
ax5.set_ylabel("LCL Height (m)")
ax6.set_ylabel("Energy-Helicity Index")
ax7.set_ylabel("Significant Tornado")

plt.setp(ax1, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])
plt.setp(ax2, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])
plt.setp(ax3, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])
plt.setp(ax4, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])
plt.setp(ax5, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])
plt.setp(ax6, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])
plt.setp(ax7, xlim=[GFSdataframe[timeName].iloc[0], GFSdataframe[timeName].iloc[-1]])

leg = ax7.legend(loc=(0, -0.5), ncol=6)

if(saveImage):
    plt.savefig("images/severe.png", bbox_inches="tight")


# In[ ]:




