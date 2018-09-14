import requests
import statistics
#This script will output a csv file that shows the average temperature for each longitude in 
#the United States that intersects with a State Capital City


#returns array of location key and longitude
def getLocationKey(zipCode):
    try:
        response=requests.get('http://dataservice.accuweather.com/locations/v1/cities/us/search?apikey={}&q={}'.format(vApiKey,zipCode)).json()
        return [response[0]['Key'],int(response[0]['GeoPosition']['Longitude'])]
    except:
        return 'Error: called failed for {}'.format(zipCode)

#Ideally this is an env. variable and not in the script itself
vApiKey = 'U9RD5JrOZyoMPMrdeKtecydmMnoS4XVr'
stateCapitalZips = ['36101', '99801', '85001', '72201', '94203', '80201', '06101', '19901', '32301', '30301', '96801', '83701', '62701', '46201', '50301', '66601', '40601', '70801', '04330', '21401', '02108', '48901', '55101', '39201', '65101', '59601', '68501', '89701', '03301', '08601', '87501', '12201', '27601', '58501', '43201', '73101', '97301', '17101', '02901', '29201', '57501', '37201', '73301', '84101', '05601', '23218', '98501', '25301', '53701', '82001']
resultsFileName='results.csv'
forecasts = {}

#get location keys for capitals in usa
locations = []
for z in stateCapitalZips:
    locations.append(getLocationKey(z))

#iterate through cities
for l in locations:
    locationKey=l[0]
    locationLongitude=l[1]
    forecastResponse=requests.get('http://dataservice.accuweather.com/forecasts/v1/daily/5day/{}?apikey={}'.format(locationKey,vApiKey)).json()
    
    #iterate through forecast days
    #use to calculate the mean temp using only max temperatures
    for day in forecastResponse['DailyForecasts']:
        date=day['Date'][:10]
        maxTemp=day['Temperature']['Maximum']['Value']
        if date in forecasts:
            if locationLongitude in forecasts[date]:
                forecasts[date][locationLongitude].extend([maxTemp])
            else:
                #create new longitude
                forecasts[date][locationLongitude]=[maxTemp]
        else:
            #create new date record
            forecasts[date]={locationLongitude:[maxTemp]}
            
#     #use to calculate the mean temp using min and max temperatures
#     for day in forecastResponse['DailyForecasts']:
#         date=day['Date'][:10]
#         minTemp=day['Temperature']['Minimum']['Value']
#         maxTemp=day['Temperature']['Maximum']['Value']
#         if date in forecasts:
#             if locationLongitude in forecasts[date]:
#                 forecasts[date][locationLongitude].extend([minTemp,maxTemp])
#             else:
#                 #create new longitude
#                 forecasts[date][locationLongitude]=[minTemp,maxTemp]
#         else:
#             #create new date record
#             forecasts[date]={locationLongitude:[minTemp,maxTemp]}

#write to file
results = open(resultsFileName,'w') 
results.write('{},{},{}\n'.format('date','longitude','temperature'))
for d in forecasts:
    for lng in forecasts[d]:
        results.write('{},{},{}\n'.format(d,lng,statistics.mean(forecasts[d][lng])))
results.close()

print('Script complete!')