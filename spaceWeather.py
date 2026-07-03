#!/usr/bin/env python
# coding: utf-8

# In[26]:


import datetime
#%matplotlib inline
import matplotlib.pyplot as plt
from math import ceil, floor
import numpy as np
import pandas as pd

import modules.URLhandler as URLhandler
import modules.timeHandler as timeHandler


# In[27]:


darkMode = False
backgroundColor = "xkcd:dark"
axisColor = "xkcd:light grey"

timeName = 'timestamp'


# In[28]:


# This acquires the short-term DSCOVR data.
# DSCOVR data has been discontinued. As a result, 1 Hz data no longer exists.
# Relevant cells will be left commented in the event a similar product reappears at a later date.
#api_urlDSCOVR = "https://services.swpc.noaa.gov/json/dscovr/dscovr_mag_1s.json"

#dataDSCOVR = URLhandler.URLcollectorJSON(api_urlDSCOVR, "DSCOVR short-term")


# In[29]:


# This acquires the estimated Kp index. Not the same as the actual Kp index.
api_urlKP = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

dataKP = URLhandler.URLcollectorJSON(api_urlKP, "Kp index")


# In[30]:


# This acquires the real-time solar wind magnetometer data.
api_urlRTSWmag = "https://services.swpc.noaa.gov/json/rtsw/rtsw_mag_1m.json"

dataRTSWmag = URLhandler.URLcollectorJSON(api_urlRTSWmag, "RTSW mag")


# In[31]:


# This acquires the real-time solar wind proton data.
api_urlRTSWwind = "https://services.swpc.noaa.gov/json/rtsw/rtsw_wind_1m.json"

dataRTSWwind = URLhandler.URLcollectorJSON(api_urlRTSWwind, "RTSW wind")


# In[32]:


# This acquires the GOES X-ray data. Primary is usually GOES-18.
api_urlGOESxray = "https://services.swpc.noaa.gov/json/goes/primary/xrays-7-day.json"

dataGOESxray = URLhandler.URLcollectorJSON(api_urlGOESxray, "GOES X-ray")


# In[33]:


# This acquires the latest significant X-ray flares.
api_urlFlares = "https://services.swpc.noaa.gov/json/goes/primary/xray-flares-7-day.json"

dataFlares = URLhandler.URLcollectorJSON(api_urlFlares, "peak X-ray flares")


# In[34]:


# This acquires the proton flux data. Primary is usually GOES-18.
api_urlGOESproton = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-7-day.json"

dataGOESproton = URLhandler.URLcollectorJSON(api_urlGOESproton, "GOES proton")


# In[35]:


# This acquires the low-energy proton data from ACE's EPAM instrument.
api_urlACEproton = "https://services.swpc.noaa.gov/json/ace/epam/ace_epam_5m.json"

dataACEproton = URLhandler.URLcollectorJSON(api_urlACEproton, "ACE EPAM protons")


# In[36]:


# Processes the 1 Hz DSCOVR data.
# See above notice about discontinued data.

# DSCOVRlen = len(dataDSCOVR)
# dictDSCOVR = {'bt':        [None]*DSCOVRlen,
#               'bz':        [None]*DSCOVRlen,
#               'bx':        [None]*DSCOVRlen,
#               'by':        [None]*DSCOVRlen,
#               'timestamp': [None]*DSCOVRlen}
# DSCOVRdataframe = pd.DataFrame(dictDSCOVR)

# count01 = 0
# for i in dataDSCOVR:
#     # For some of these, it is as easy as grabbing the data directly from the JSON file.
#     DSCOVRdataframe['bt'][count01] = i['bt']
#     DSCOVRdataframe['bz'][count01] = i['bz_gsm']
#     DSCOVRdataframe['bx'][count01] = i['bx_gsm']
#     DSCOVRdataframe['by'][count01] = i['by_gsm']

#     DSCOVRdataframe[timeName][count01] = i['time_tag']
#     count01 += 1


# In[37]:


# Processes the minutely Kp data.
KPlen = len(dataKP)
dictKP = {'estimates': [None]*KPlen,
          timeName:    [None]*KPlen}
KPdataframe = pd.DataFrame(dictKP)

count02 = 0
for i in dataKP:
    # This is the planetary Kp value. Updated every minute.
    # Seems to be revised upwards or downwards occasionally after the initial value.
    KPdataframe['estimates'][count02] = i['estimated_kp']
    
    KPdataframe[timeName][count02] = i['time_tag']

    count02 += 1


# In[38]:


# Processes the minutely magnetometer data from either SOLAR-1 or ACE, depending on which is selected.
# Set the Real-Time Solar Wind data source once for ease of changes.
# Main plan is to use the satellite tagged as active.
RTSWdataSourceMain = "SOLAR1"
RTSWdataSourceBackup = "ACE"
useActiveSat = True

RTSWmagLen = 0
for i in dataRTSWmag:
    if((i['active'] and useActiveSat) or (i['source'] == RTSWdataSourceMain and not useActiveSat)):
        RTSWmagLen += 1

# Sets up the dictionary and DataFrame for the magnetometer data.
dictRTSWmag = {'bt':     [None]*RTSWmagLen,
               'bz':     [None]*RTSWmagLen,
               'bx':     [None]*RTSWmagLen,
               'by':     [None]*RTSWmagLen,
               'source': [None]*RTSWmagLen,
               timeName: [None]*RTSWmagLen}
RTSWmagDataframe = pd.DataFrame(dictRTSWmag)

count03 = 0
for i in dataRTSWmag:
    # SOLAR-1 is the current primary satellite for space weather observations.
    if((i['active'] and useActiveSat) or (i['source'] == RTSWdataSourceMain and not useActiveSat)):
        RTSWmagDataframe['bt'][count03] = i['bt']
        RTSWmagDataframe['bz'][count03] = i['bz_gsm']
        RTSWmagDataframe['bx'][count03] = i['bx_gsm']
        RTSWmagDataframe['by'][count03] = i['by_gsm']

        RTSWmagDataframe['source'][count03] = i['source']
        RTSWmagDataframe[timeName][count03] = i['time_tag']

        count03 += 1

# In the event that the primary satellite has not been reporting, switch to the backup option.
# Currently this is set to ACE, but the backup is configurable above.
count03 = 0
if(RTSWmagDataframe[timeName][0] == None):
    for i in dataRTSWmag:
        if(i['source'] == RTSWdataSourceBackup):
            RTSWmagDataframe['bt'][count03] = i['bt']
            RTSWmagDataframe['bz'][count03] = i['bz_gsm']
            RTSWmagDataframe['bx'][count03] = i['bx_gsm']
            RTSWmagDataframe['by'][count03] = i['by_gsm']

            RTSWmagDataframe['source'][count03] = i['source']
            RTSWmagDataframe[timeName][count03] = i['time_tag']

            count03 += 1


# In[39]:


# Processes the minutely proton data from either DSCOVR or ACE, depending on which is selected above.
RTSWwindLen = 0
for i in dataRTSWwind:
    if((i['active'] and useActiveSat) or (i['source'] == RTSWdataSourceMain and not useActiveSat)):
        RTSWwindLen += 1

dictRTSWwind = {'density': [None]*RTSWwindLen,
                'speed':   [None]*RTSWwindLen,
                'temps':   [None]*RTSWwindLen,
                'source':  [None]*RTSWwindLen,
                timeName:  [None]*RTSWwindLen}
RTSWwindDataframe = pd.DataFrame(dictRTSWwind)

count04 = 0
for i in dataRTSWwind:
    # SOLAR-1 is the current primary satellite for space weather observations.
    if((i['active'] and useActiveSat) or (i['source'] == RTSWdataSourceMain and not useActiveSat)):
        # For some reason, it is possible for density to be zero.
        # I suspect that the SWPC is truncating the density data which goes to zero at low values.
        if(i['proton_density'] != 0):
            RTSWwindDataframe['density'][count04] = i['proton_density']
        else:
            RTSWwindDataframe['density'][count04] = None
        RTSWwindDataframe['speed'][count04] = i['proton_speed']
        RTSWwindDataframe['temps'][count04] = i['proton_temperature']

        RTSWwindDataframe[timeName][count04] = i['time_tag']

        count04 += 1

# In the event that the primary satellite has not been reporting, switch to the backup option.
# Currently this is set to ACE, but the backup is configurable above.
count04 = 0
if(RTSWwindDataframe[timeName][0] == None):
    for i in dataRTSWwind:
        if(i['source'] == RTSWdataSourceBackup):
            # For some reason, it is possible for density to be zero.
            # I suspect that the SWPC is truncating the density data which goes to zero at low values.
            if(i['proton_density'] != 0):
                RTSWwindDataframe['density'][count04] = i['proton_density']
            else:
                RTSWwindDataframe['density'][count04] = None
            RTSWwindDataframe['speed'][count04] = i['proton_speed']
            RTSWwindDataframe['temps'][count04] = i['proton_temperature']

            RTSWwindDataframe[timeName][count04] = i['time_tag']
            
            count04 += 1


# In[40]:


# Processes the GOES X-ray data.
GOESxrayLen = 0
for i in dataGOESxray:
    if(i['energy'] == "0.05-0.4nm"):
        GOESxrayLen += 1

dictGOESxray = {'short':  [None]*GOESxrayLen,
                'long':   [None]*GOESxrayLen,
                timeName: [None]*GOESxrayLen}
GOESxrayDataframe = pd.DataFrame(dictGOESxray)

count05 = 0
for i in dataGOESxray:
    # Because the x-ray flux is separated into two different ranges,
    # we need to break it into short- and long-wave x-rays.
    if(i['energy'] == "0.05-0.4nm"):
        GOESxrayDataframe['short'][count05] = i['flux']

    if(i['energy'] == "0.1-0.8nm"):
        GOESxrayDataframe['long'][count05] = i['flux']

        GOESxrayDataframe[timeName][count05] = i['time_tag']

        count05 += 1


# In[41]:


# Processes the significant flares over the last 7 days.
flaresLen = 0
for i in dataFlares:
    if(i['max_xrlong'] >= 0.00001):
        flaresLen += 1

dictFlares = {'maxClass':    [None]*flaresLen,
              'maxStrength': [None]*flaresLen,
              'maxTime':     [None]*flaresLen}
flaresDataframe = pd.DataFrame(dictFlares)

count08 = 0
for i in dataFlares:
    if(i['max_xrlong'] >= 0.00001):
        flaresDataframe['maxClass'][count08] = i['max_class']
        flaresDataframe['maxStrength'][count08] = i['max_xrlong']
        flaresDataframe['maxTime'][count08] = i['max_time']

        count08 += 1


# In[42]:


# Processes the GOES proton flux data.
GOESprotonLen = 0
for i in dataGOESproton:
    if(i['energy'] == "\u003E=10 MeV"):
        GOESprotonLen += 1

dictGOESproton = {'10MeV':  [None]*GOESprotonLen,
                  '50MeV':  [None]*GOESprotonLen,
                  '100MeV': [None]*GOESprotonLen,
                  '500MeV': [None]*GOESprotonLen,
                  timeName: [None]*GOESprotonLen}
GOESprotonDataframe = pd.DataFrame(dictGOESproton)

count06 = 0
for i in dataGOESproton:
    if(i['energy'] == "\u003E=10 MeV"):
        GOESprotonDataframe['10MeV'][count06] = i['flux']

    if(i['energy'] == "\u003E=50 MeV"):
        GOESprotonDataframe['50MeV'][count06] = i['flux']

    if(i['energy'] == "\u003E=100 MeV"):
        GOESprotonDataframe['100MeV'][count06] = i['flux']

    if(i['energy'] == "\u003E=500 MeV"):
        GOESprotonDataframe['500MeV'][count06] = i['flux']
        GOESprotonDataframe[timeName][count06] = i['time_tag']
        count06 += 1


# In[43]:


# Processes the ACE low-energy proton flux.
ACEprotonLen = len(dataACEproton)

dictACEproton = {'p1':     [None]*ACEprotonLen,
                 'p2':     [None]*ACEprotonLen,
                 'p3':     [None]*ACEprotonLen,
                 'p4':     [None]*ACEprotonLen,
                 'p5':     [None]*ACEprotonLen,
                 'p6':     [None]*ACEprotonLen,
                 'p7':     [None]*ACEprotonLen,
                 'p8':     [None]*ACEprotonLen,
                 timeName: [None]*ACEprotonLen}
ACEprotonDataframe = pd.DataFrame(dictACEproton)

count07 = 0
for i in dataACEproton:
    ACEprotonDataframe['p1'][count07] = i['p1']
    ACEprotonDataframe['p2'][count07] = i['p2']
    ACEprotonDataframe['p3'][count07] = i['p3']
    ACEprotonDataframe['p4'][count07] = i['p4']
    ACEprotonDataframe['p5'][count07] = i['p5']
    ACEprotonDataframe['p6'][count07] = i['p6']
    ACEprotonDataframe['p7'][count07] = i['p7']
    ACEprotonDataframe['p8'][count07] = i['p8']

    ACEprotonDataframe[timeName][count07] = i['time_tag']

    count07 += 1


# In[44]:


# Parse the timestamps into the correct format for plotting.
# DSCOVRdataframe[timeName] = timeHandler.timeParser(DSCOVRdataframe[timeName])
KPdataframe[timeName] = timeHandler.timeParser(KPdataframe[timeName])
RTSWmagDataframe[timeName] = timeHandler.timeParser(RTSWmagDataframe[timeName])
RTSWwindDataframe[timeName] = timeHandler.timeParser(RTSWwindDataframe[timeName])
GOESxrayDataframe[timeName] = timeHandler.timeParser(GOESxrayDataframe[timeName])
flaresDataframe['maxTime'] = timeHandler.timeParser(flaresDataframe['maxTime'])
GOESprotonDataframe[timeName] = timeHandler.timeParser(GOESprotonDataframe[timeName])
ACEprotonDataframe[timeName] = timeHandler.timeParser(ACEprotonDataframe[timeName])

# This is used to calculate the offset that has to be applied to the rectangles to allow them to be charted.
# Outputs the time in days since January 1, 1970 which is the date from which datetime calculates for the numeric equivalent.
# Technically, from 18Z December 31, 1969 due to time zones. Will need to be adjusted for DST.
dateInitial = datetime.datetime(1969,12,31,19,0)
dateCurrent = datetime.datetime.now()
dateOffset = (dateCurrent - dateInitial).total_seconds()/86400


# In[45]:


# Calculates the approximate conditions that are currently hitting Earth.
# Distance from Earth to SOLAR-1, in kilometers.
distanceSOLAR1 = 1500000

# Outputs time in days and minutes using latest solar wind speed data.
timeToArrival = (distanceSOLAR1 / RTSWwindDataframe['speed'][0]) / (24*60*60)
timeToArrivalMinutes = round(timeToArrival * (24 * 60))
#print(timeToArrival)
#print(timeToArrivalMinutes)


# In[46]:


# # Plots DSCOVR 1-second magnetometer data.
# plt.rcParams["figure.dpi"] = 150
# fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 8))

# # Sets the plot color to a darker value. Mainly useful at night.
# if(darkMode):
#     fig.patch.set(facecolor=backgroundColor)
#     for i in [ax1, ax2]:
#         i.set(facecolor=backgroundColor)
#         i.spines['bottom'].set_color(axisColor)
#         i.spines['top'].set_color(axisColor) 
#         i.spines['right'].set_color(axisColor)
#         i.spines['left'].set_color(axisColor)
#         i.tick_params(axis='x', colors=axisColor)
#         i.tick_params(axis='y', colors=axisColor, which='both')
#         i.yaxis.label.set_color(axisColor)
#         i.xaxis.label.set_color(axisColor)
#         i.title.set_color(axisColor)

# # Set the size of the viewing window for the magnetometer data.
# # Because sudden spikes can appear, this adjusts automatically.
# magViewingLimitS = max(ceil(max((DSCOVRdataframe['bt']), key=abs)/10)*10, 10)
# magLimitS = [-magViewingLimitS, magViewingLimitS]

# # The order of these plots matter for layering.
# ax1.plot(DSCOVRdataframe[timeName], DSCOVRdataframe['bx'], color='magenta', linewidth=1)
# ax1.plot(DSCOVRdataframe[timeName], DSCOVRdataframe['by'], color='deepskyblue', linewidth=1)
# ax1.plot(DSCOVRdataframe[timeName], DSCOVRdataframe['bt'], color='black', linewidth=1.5)
# ax1.plot(DSCOVRdataframe[timeName], DSCOVRdataframe['bz'], color='red', linewidth=2)

# ax2.plot(KPdataframe[timeName], KPdataframe['estimates'], color='green')

# # Bolded centerline for the magnetometer 0 nT mark.
# ax1.hlines(y=0, xmin=0, xmax=dateOffset, linewidth=1, color='k')

# # Mark out the different geomagnetic categories (G1-G5).
# ax2.hlines(y=4.5, xmin=0, xmax=dateOffset, linewidth=1.5, color='yellow')
# ax2.hlines(y=5.5, xmin=0, xmax=dateOffset, linewidth=1.5, color='gold')
# ax2.hlines(y=6.5, xmin=0, xmax=dateOffset, linewidth=1.5, color='orange')
# ax2.hlines(y=7.5, xmin=0, xmax=dateOffset, linewidth=1.5, color='orangered')
# ax2.hlines(y=8.80, xmin=0, xmax=dateOffset, linewidth=2, color='red')

# # DSCOVRlen minus 1 accounts for the off-by-one issue with indexing.
# plt.setp(ax1, xlim=[DSCOVRdataframe[timeName][DSCOVRlen-1], DSCOVRdataframe[timeName][0]], ylim=magLimitS)
# plt.setp(ax2, xlim=[DSCOVRdataframe[timeName][DSCOVRlen-1], DSCOVRdataframe[timeName][0]], ylim=[0, 10])

# ax1.grid(True)
# ax2.grid(True)

# ax1.set_title("Short Term Data (last 5 minutes)")
# ax1.set_ylabel("Field Strength (nT)")
# ax2.set_ylabel("Planetary Kp Index")
# ax2.set_xlabel("Time of Observation (UTC)")

# fig.autofmt_xdate()

# plt.show()


# In[47]:


# Plots SOLAR-1/ACE 1-minute magnetometer and proton data.
plt.rcParams["figure.dpi"] = 300
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

# Bolded centerline for the magnetometer 0 nT mark.
if(not darkMode):
    ax1.hlines(y=0, xmin=0, xmax=dateOffset, linewidth=1, color='black')
else:
    ax1.hlines(y=0, xmin=0, xmax=dateOffset, linewidth=1, color='white')

# The order of these plots matter for layering.
ax1.plot(RTSWmagDataframe[timeName], RTSWmagDataframe['bx'], color='magenta', linewidth=0.75)
ax1.plot(RTSWmagDataframe[timeName], RTSWmagDataframe['by'], color='deepskyblue', linewidth=0.75)
if(not darkMode):
    ax1.plot(RTSWmagDataframe[timeName], RTSWmagDataframe['bt'], color='black', linewidth=1)
else:
    ax1.plot(RTSWmagDataframe[timeName], RTSWmagDataframe['bt'], color='white', linewidth=1)
ax1.plot(RTSWmagDataframe[timeName], RTSWmagDataframe['bz'], color='red', linewidth=1.5)

ax2.plot(RTSWwindDataframe[timeName], RTSWwindDataframe['density'], color='orange')

ax3.plot(RTSWwindDataframe[timeName], RTSWwindDataframe['speed'], color='mediumorchid')

ax4.plot(RTSWwindDataframe[timeName], RTSWwindDataframe['temps'], color='limegreen')

ax5.plot(KPdataframe[timeName], KPdataframe['estimates'], color="green")

# Sets the y-scale to logarithmic.
ax2.set_yscale('log')
ax4.set_yscale('log')

# Number of minutes to be plotted.
minutesPlotted = min(360, RTSWmagLen-1)
RTSWtimeLimit = [RTSWmagDataframe[timeName][minutesPlotted], RTSWmagDataframe[timeName][0]]

# Set the size of the viewing window for the magnetometer data.
# Because sudden spikes can appear, this adjusts automatically.
magViewingLimitL = max(ceil(max((RTSWmagDataframe['bt'][:minutesPlotted]), key=abs)/10)*10, 10)
magLimitL = [-magViewingLimitL, magViewingLimitL]

# Defines the limits on how much data is plotted vertically.
# Starts with density.
densityHigh = np.power(float(10), ceil(np.log10(max([i for i in RTSWwindDataframe['density'][:minutesPlotted] if i is not None]))))
densityLow = np.power(float(10), floor(np.log10(min([i for i in RTSWwindDataframe['density'][:minutesPlotted] if i is not None]))))
densityLimit = [densityLow, densityHigh]

# Then goes to solar wind speed.
speedMax = max(ceil(max([i for i in RTSWwindDataframe['speed'][:minutesPlotted] if i is not None])/100)*100, 700)
speedMin = min(floor(min([i for i in RTSWwindDataframe['speed'][:minutesPlotted] if i is not None])/100)*100, 300)
speedLimit = [speedMin, speedMax]

# Wraps up with the temperature data.
tempHigh = np.power(float(10), ceil(np.log10(max([i for i in RTSWwindDataframe['temps'][:minutesPlotted] if i is not None]))))
tempLow = np.power(float(10), floor(np.log10(min([i for i in RTSWwindDataframe['temps'][:minutesPlotted] if i is not None]))))
tempLimit = [tempLow, tempHigh]

# Set the actual bounds of each plot.
plt.setp(ax1, xlim=RTSWtimeLimit, ylim=magLimitL) # Magnetic (nT)
plt.setp(ax2, xlim=RTSWtimeLimit, ylim=densityLimit) # Density (cm^-3) 
plt.setp(ax3, xlim=RTSWtimeLimit, ylim=speedLimit) # Speed (km/s)
plt.setp(ax4, xlim=RTSWtimeLimit, ylim=tempLimit) # Temperature (K)
plt.setp(ax5, xlim=RTSWtimeLimit, ylim=[0, 10]) #Kp index


# Mark out the different geomagnetic categories (G1-G5).
ax5.hlines(y=4.5, xmin=0, xmax=dateOffset, linewidth=1.5, color='yellow')
ax5.hlines(y=5.5, xmin=0, xmax=dateOffset, linewidth=1.5, color='gold')
ax5.hlines(y=6.5, xmin=0, xmax=dateOffset, linewidth=1.5, color='orange')
ax5.hlines(y=7.5, xmin=0, xmax=dateOffset, linewidth=1.5, color='orangered')
ax5.hlines(y=8.80, xmin=0, xmax=dateOffset, linewidth=2, color='red')

# Draw lines at the estimated solar wind parameters arriving at Earth now.
ax1.vlines(x=dateOffset-timeToArrival, ymin=magLimitL[0], ymax=magLimitL[1], linewidth=1.5, color='g')
ax2.vlines(x=dateOffset-timeToArrival, ymin=densityLimit[0], ymax=densityLimit[1], linewidth=1.5, color='g')
ax3.vlines(x=dateOffset-timeToArrival, ymin=speedLimit[0], ymax=speedLimit[1], linewidth=1.5, color='g')
ax4.vlines(x=dateOffset-timeToArrival, ymin=tempLimit[0], ymax=tempLimit[1], linewidth=1.5, color='g')

ax1.grid(True)
ax2.grid(True)
ax3.grid(True)
ax4.grid(True)
ax5.grid(True)

ax1.set_title("Long Term Data using " + RTSWmagDataframe['source'][0] + " (up to 24 hours)\n" + \
              "Lead time: " + str(timeToArrivalMinutes) + " minutes")
ax1.set_ylabel("Field Strength (nT)")
ax2.set_ylabel("Density (1/cm^3)")
ax3.set_ylabel("Speed (km/s)")
ax4.set_ylabel("Temperature (K)")
ax5.set_ylabel("Planetary Kp Index")
ax5.set_xlabel("Time of Observation (UTC)")

fig.autofmt_xdate()

plt.show()


# In[48]:


# Plots GOES X-ray data.
plt.rcParams["figure.dpi"] = 300
fig, ax = plt.subplots(figsize=(10, 6))

# Sets the plot color to a darker value. Mainly useful at night.
if(darkMode):
    ax.set(facecolor=backgroundColor)
    ax.spines['bottom'].set_color(axisColor)
    ax.spines['top'].set_color(axisColor) 
    ax.spines['right'].set_color(axisColor)
    ax.spines['left'].set_color(axisColor)
    ax.tick_params(axis='x', colors=axisColor)
    ax.tick_params(axis='y', colors=axisColor, which='both')
    ax.yaxis.label.set_color(axisColor)
    ax.xaxis.label.set_color(axisColor)
    ax.title.set_color(axisColor)
    fig.patch.set(facecolor=backgroundColor)

# Lines for M- (black or white) and X- (red) class X-ray flares.
if(not darkMode):
    ax.hlines(y=0.00001, xmin=0, xmax=dateOffset+1, linewidth=1, color='black')
else:
    ax.hlines(y=0.00001, xmin=0, xmax=dateOffset+1, linewidth=1, color='white')
ax.hlines(y=0.0001, xmin=0, xmax=dateOffset+1, linewidth=2, color='red')

ax.plot(GOESxrayDataframe[timeName], GOESxrayDataframe['short'], color='mediumblue')
ax.plot(GOESxrayDataframe[timeName], GOESxrayDataframe['long'], color='orange')

ax.scatter(flaresDataframe['maxTime'], flaresDataframe['maxStrength'], s=25, zorder=3, color='red')


# Plots the data between two limits for the given time frame. Currently set from A1 to X100.
# An X100 would be interesting, to say the least.
hoursPlottedXray = 48
minutesPlottedXray = min(hoursPlottedXray * 60, GOESxrayLen)
plt.setp(ax, xlim=[GOESxrayDataframe[timeName][GOESxrayLen-minutesPlottedXray], GOESxrayDataframe[timeName][GOESxrayLen-1]], ylim=[0.00000001, 0.01])

if(not darkMode):
    flaresText = dict(horizontalalignment='center', verticalalignment='bottom', color='black')
else:
    flaresText = dict(horizontalalignment='center', verticalalignment='bottom', color=axisColor)

# Only labels the flares that occurred after the first flux data point. Necessary because the text does not respect the plot boundaries.
for i in range(flaresLen):
    if(flaresDataframe['maxTime'][i] >= GOESxrayDataframe[timeName][GOESxrayLen-minutesPlottedXray]):
        ax.text(flaresDataframe['maxTime'][i], flaresDataframe['maxStrength'][i], flaresDataframe['maxClass'][i], **flaresText)

# Sets the y-scale to logarithmic.
ax.set_yscale('log')

ax.grid(True)

ax.set_title("GOES X-Ray Flux")
ax.set_xlabel("Time of Observation (UTC)")
ax.set_ylabel("Flux (Watts/m^2)")

fig.autofmt_xdate()

plt.show()


# In[49]:


# Plots ACE proton flux data.
plt.rcParams["figure.dpi"] = 300
fig, ax = plt.subplots(figsize=(10, 6))

# Sets the plot color to a darker value. Mainly useful at night.
if(darkMode):
    ax.set(facecolor=backgroundColor)
    ax.spines['bottom'].set_color(axisColor)
    ax.spines['top'].set_color(axisColor) 
    ax.spines['right'].set_color(axisColor)
    ax.spines['left'].set_color(axisColor)
    ax.tick_params(axis='x', colors=axisColor)
    ax.tick_params(axis='y', colors=axisColor, which='both')
    ax.yaxis.label.set_color(axisColor)
    ax.xaxis.label.set_color(axisColor)
    ax.title.set_color(axisColor)
    fig.patch.set(facecolor=backgroundColor)

ACEthickness = 1
ax.plot(ACEprotonDataframe[timeName], ACEprotonDataframe['p1'], color='red', linewidth=ACEthickness)
ax.plot(ACEprotonDataframe[timeName], ACEprotonDataframe['p2'], color='orange', linewidth=ACEthickness)
ax.plot(ACEprotonDataframe[timeName], ACEprotonDataframe['p3'], color='gold', linewidth=ACEthickness)
ax.plot(ACEprotonDataframe[timeName], ACEprotonDataframe['p4'], color='green', linewidth=ACEthickness)
ax.plot(ACEprotonDataframe[timeName], ACEprotonDataframe['p5'], color='turquoise', linewidth=ACEthickness)
ax.plot(ACEprotonDataframe[timeName], ACEprotonDataframe['p6'], color='blue', linewidth=ACEthickness)
ax.plot(ACEprotonDataframe[timeName], ACEprotonDataframe['p7'], color='indigo', linewidth=ACEthickness)
ax.plot(ACEprotonDataframe[timeName], ACEprotonDataframe['p8'], color='purple', linewidth=ACEthickness)

# The proton flux is recorded every 5 minutes, so plotting by times requires adjustment.
hoursPlottedACE = 24
obsPlottedACE = min(hoursPlottedACE * int(60/5), ACEprotonLen)

# To make the plot look better, adjust the viewing window accordingly.
protonMax = max([i for i in ACEprotonDataframe['p1'][-obsPlottedACE:] if i is not None])
if(protonMax > 10000):
    protonBound = 1000000
elif(protonMax > 1000):
    protonBound = 100000
else:
    protonBound = 10000

plt.setp(ax, xlim=[ACEprotonDataframe[timeName][ACEprotonLen-1], ACEprotonDataframe[timeName][ACEprotonLen-obsPlottedACE]], \
             ylim=[0.01, protonBound])

# Sets the y-scale to logarithmic.
ax.set_yscale('log')

ax.grid(True)

ax.set_title("ACE Low-Energy Proton Flux (EPAM)")
ax.set_xlabel("Time of Observation (UTC)")
ax.set_ylabel("Flux (particles/m^2*s^1*sr or pfu)")

plt.show()


# In[50]:


# Plots GOES proton flux data.
plt.rcParams["figure.dpi"] = 300
fig, ax = plt.subplots(figsize=(10, 6))

# Sets the plot color to a darker value. Mainly useful at night.
if(darkMode):
    ax.set(facecolor=backgroundColor)
    ax.spines['bottom'].set_color(axisColor)
    ax.spines['top'].set_color(axisColor) 
    ax.spines['right'].set_color(axisColor)
    ax.spines['left'].set_color(axisColor)
    ax.tick_params(axis='x', colors=axisColor)
    ax.tick_params(axis='y', colors=axisColor, which='both')
    ax.yaxis.label.set_color(axisColor)
    ax.xaxis.label.set_color(axisColor)
    ax.title.set_color(axisColor)
    fig.patch.set(facecolor=backgroundColor)

ax.plot(GOESprotonDataframe[timeName], GOESprotonDataframe['500MeV'], color='orange')
ax.plot(GOESprotonDataframe[timeName], GOESprotonDataframe['100MeV'], color='limegreen')
ax.plot(GOESprotonDataframe[timeName], GOESprotonDataframe['50MeV'], color='blue')
ax.plot(GOESprotonDataframe[timeName], GOESprotonDataframe['10MeV'], color='red', linewidth=2.0)

# The proton flux is recorded every 5 minutes, so plotting by times requires adjustment.
hoursPlottedProton = 24
obsPlottedProton = min(hoursPlottedProton * int(60/5), GOESprotonLen)

# Under normal conditions, matches the SWPC proton flux limits. Expands it in the case of S4+ conditions.
protonMax = max([i for i in GOESprotonDataframe['10MeV'][-obsPlottedProton:] if i is not None])
if(protonMax > 10000):
    protonBound = 100000
else:
    protonBound = 10000

plt.setp(ax, xlim=[GOESprotonDataframe[timeName][GOESprotonLen-obsPlottedProton], GOESprotonDataframe[timeName][GOESprotonLen-1]], \
             ylim=[0.01, protonBound])

# Sets the lines for the SWPC's warning (S1) and the S4 criteria.
ax.hlines(y=10, xmin=0, xmax=dateOffset+1, linewidth=1.5, color='salmon', linestyles='dashed')
ax.hlines(y=10000, xmin=0, xmax=dateOffset+1, linewidth=2.5, color='r')

# Sets the y-scale to logarithmic.
ax.set_yscale('log')

ax.grid(True)

ax.set_title("GOES Proton Flux")
ax.set_xlabel("Time of Observation (UTC)")
ax.set_ylabel("Flux (particles/m^2*s^1*sr)")

plt.show()


# In[ ]:




