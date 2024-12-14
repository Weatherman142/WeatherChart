import pandas as pd
import dateutil as du

def timeParser(timeList):
    if(type(timeList[0]) != pd._libs.tslibs.timestamps.Timestamp):
        timeList = [du.parser.parse(x) for x in timeList]

    return timeList