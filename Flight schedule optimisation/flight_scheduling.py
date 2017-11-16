#____________________________________________________________________________________

#- Author name: Saurabh Patil                              
#- Last updated: 10/11/2017
#- Title : Flight schedule optimisation
#- Code version: v0.02
#- Type: Python source code
#
#- © All rights are reserved.
# ___________________________________________________________________________________


import pandas as pd
import numpy as np
from operator import itemgetter

#time parameters
CTAustin = 360
CTDallas = [360,360]
CTHouston = [360,360,360]
RelTimeAus = 0
RelTimeDal = [0,0]
RelTimeHou = [0,0,0]
endTime = 1320
#fights tuple
flight = ('T1','T2','T3','T4','T5','T6')
#gates counter at airport
gateAustin = 0
gateDallas = 1
gateHouston = 2
#flight times airport
ftAusDal = 50
ftAusHou = 45
ftDalHou = 65
#ground times airport
gtAustin = 25
gtDallas = 30
gtHouston = 35
#flight schedule data frame
cols = ['tail_number','origin','destination','departure_time','arrival_time']
n=55
idx = np.arange(n)
flightSchedule = pd.DataFrame(columns=cols,index=idx)
flightSchedule = flightSchedule.fillna(0)
endIndicator = 0
i = 0

def timeConversion(time):
    hour=time//60
    minutes=time%60
    if len(str(hour))==1:
        hour='{0:02d}'.format(hour)
    if len(str(minutes))==1:
        minutes=str(minutes).rjust(2,'0')
    newTime=str(hour)+str(minutes)
    return newTime

while (True) :
	if gateAustin <= 1  and gateHouston !=0 and gateDallas !=0 :
		flightSchedule.loc[i,'tail_number'] = flight[i%6]
		flightSchedule.loc[i,'origin'] = 'AUS'
		flightSchedule.loc[i,'departure_time'] = timeConversion(CTAustin)
		if gateHouston !=0 :
			flightSchedule.loc[i,'destination'] = 'HOU'
			CTAustin = CTAustin + ftAusHou
			if CTAustin > endTime:
				flightSchedule.loc[i] = 0
				break
			flightSchedule.loc[i,'arrival_time'] = timeConversion(CTAustin)
			RelTimeHou[gateHouston-1] = CTAustin + gtHouston
			gateHouston = gateHouston - 1
		elif gateDallas !=0 :
			flightSchedule.loc[i,'destination'] = 'DAL'
			CTAustin = CTAustin + ftAusDal
			if CTAustin > endTime:
				flightSchedule.loc[i] = 0
				break
			flightSchedule.loc[i,'arrival_time'] = timeConversion(CTAustin)
			RelTimeDal[gateDallas-1] = CTAustin + gtDallas
			gateDallas = gateDallas - 1
	if (flightSchedule.loc[i,'origin'] == 'AUS'):
		i += 1

	if gateHouston <= 3 and gateDallas !=0 :
		flightSchedule.loc[i,'tail_number'] = flight[i%6]
		flightSchedule.loc[i,'origin'] = 'HOU'
		flightSchedule.loc[i,'departure_time'] = timeConversion(CTHouston[gateHouston-1])
		if gateAustin !=0 :
			flightSchedule.loc[i,'destination'] = 'AUS'
			CTHouston[gateHouston-1] = CTHouston[gateHouston-1] + ftAusHou
			if CTHouston[gateHouston-1] > endTime:
				flightSchedule.loc[i] = 0
				break
			flightSchedule.loc[i,'arrival_time'] = timeConversion(CTHouston[gateHouston-1])
			RelTimeAus = CTHouston[gateHouston-1] + gtAustin
			gateAustin = gateAustin - 1
		elif gateDallas !=0 :
			flightSchedule.loc[i,'destination'] = 'DAL'
			CTHouston[gateHouston-1] = CTHouston[gateHouston-1] + ftDalHou
			if CTHouston[gateHouston-1] > endTime:
				flightSchedule.loc[i] = 0
				break
			flightSchedule.loc[i,'arrival_time'] = timeConversion(CTHouston[gateHouston-1])
			RelTimeDal[gateDallas-1] = CTHouston[gateHouston-1] + gtDallas
			gateDallas = gateDallas - 1
	if (flightSchedule.loc[i,'origin'] == 'HOU'):
		i += 1
	
	if gateDallas <= 2 and gateHouston !=0 :
		flightSchedule.loc[i,'tail_number'] = flight[i%6]
		flightSchedule.loc[i,'origin'] = 'DAL'
		flightSchedule.loc[i,'departure_time'] = timeConversion(CTDallas[gateDallas-1])
		if gateAustin !=0 :
			flightSchedule.loc[i,'destination'] = 'AUS'
			CTDallas[gateDallas-1] = CTDallas[gateDallas-1] + ftAusDal
			if CTDallas[gateDallas-1] > endTime:
				flightSchedule.loc[i] = 0
				break
			flightSchedule.loc[i,'arrival_time'] = timeConversion(CTDallas[gateDallas-1])
			RelTimeAus = CTDallas[gateDallas-1] + gtAustin
			gateAustin = gateAustin - 1
		elif gateHouston !=0 :
			flightSchedule.loc[i,'destination'] = 'HOU'
			CTDallas[gateDallas-1] = CTDallas[gateDallas-1] + ftDalHou
			if CTDallas[gateDallas-1] > endTime:
				flightSchedule.loc[i] = 0
				break
			flightSchedule.loc[i,'arrival_time'] = timeConversion(CTDallas[gateDallas-1])
			RelTimeHou[gateHouston-1] = CTDallas[gateDallas-1] + gtHouston
			gateHouston = gateHouston - 1
	if (flightSchedule.loc[i,'origin'] == 'DAL'):
		i += 1

	for x in range(3) :
		if (RelTimeHou[x] <= CTDallas[0] or RelTimeHou[x] <= CTDallas[1] or RelTimeHou[x] <= CTAustin) :
			if gateHouston == 3:
				break
			gateHouston += 1

	for j in range(2):
		if (RelTimeDal[j] <= CTHouston[0] or RelTimeDal[j] <= CTHouston[1] or RelTimeDal[j] <= CTHouston[2] or RelTimeDal[j] <= CTAustin) :
			if gateDallas == 2:
				break
			gateDallas += 1

	if (RelTimeAus <= CTHouston[0] or RelTimeAus <= CTHouston[1] or RelTimeAus <= CTHouston[2] or RelTimeAus <= CTDallas[0]  or RelTimeAus <= CTDallas[1]) :
		if gateAustin < 1:
			gateAustin += 1

    
flightSchedule.to_csv('flight_schedule.csv', columns=cols, index=False)