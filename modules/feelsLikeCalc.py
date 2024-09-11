# Calculates wind chill.
def windChillCalculation(temp, windSpeed):
    # If temperature is below 50°F and winds below 3 mph, the wind chill formula applies.
    if(temp <= 50 and windSpeed >= 3):
        windChill = 35.74 + (0.6215 * temp) - (35.75 * pow(windSpeed, 0.16)) + (0.4275 * temp * pow(windSpeed, 0.16))
        
    # Otherwise, set the wind chill to the temperature. Much simpler than the heat index.
    else:
        windChill = temp

    # Simply returns the wind chill.
    return windChill


# Defines the function that finds heat index. Found this on the WPC's webpage (Rothfusz).
# This follows the WPC calculation as described on https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml
def heatIndexCalculation(T, RH):
    # The heat index only applies above 80 degrees Fahrenheit.
    # The placeholder for a non-existent temp and RH was -999, which resulted in bizarre heat indexes (Ames hit 4700°F!)
    if(T >= 80):  
        heatIndex = -42.379 + 2.04901523*T + 10.14333127*RH - 0.22475541*T*RH - 0.00683783*T*T \
                    - 0.05481717*RH*RH + 0.00122874*T*T*RH + 0.00085282*T*RH*RH - 0.00000199*T*T*RH*RH
        
        # There are some adjustments that can be made in high or low humidity regimes.
        # The first one is if there is low humidity, the second is for higher humidities.
        if(RH < 13 and T >= 80 and T < 112):
            heatIndex -= ((13 - RH) / 4) * pow(((17 - abs(T - 95.)) / 17), 0.5)
        elif(RH > 85 and T >= 80 and T < 87):
            heatIndex += ((RH - 85) / 10) * ((87 - T) / 5)

        # If the heat index as calculated is below 80°F, use this formula instead. 
        if(heatIndex < 80):
            heatIndex =  0.5 * (T + 61.0 + ((T - 68.0) * 1.2) + (RH * 0.094))

    # Otherwise, set it equal to the temperature.
    else:
        heatIndex = T
        
    return heatIndex