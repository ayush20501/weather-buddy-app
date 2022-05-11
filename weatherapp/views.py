from django.shortcuts import render
import urllib.request
import json
from datetime import date
import calendar
import requests
import geonamescache

weeks = {"Sunday": ["saturday", "sunday", "monday", "tuesday", "wednesday", "thrusday"],
         "Monday": ["sunday", "monday", "tuesday", "wednesday", "thrusday", "friday"],
         "Tuesday": ["monday", "tuesday", "wednesday", "thrusday", "friday", "saturday"],
         "Wednesday": ["tuesday", "wednesday", "thrusday", "friday", "saturday", "sunday"],
         "Thrusday": ["wednesday", "thrusday", "friday", "saturday", "sunday", "monday"],
         "Friday": ["thrusday", "friday", "saturday", "sunday", "monday", "tuesday"],
         "Saturday": ["friday", "saturday", "sunday", "monday", "tuesday", "wednesday"]
        }

months = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", "07": "July", "08": "August",
          "09": "September", "10": "October", "11": "November", "12": "December"}


def firstfunction(request):
    if request.method == "POST":
        name = request.POST['city']
        gc = geonamescache.GeonamesCache()
        cities = gc.search_cities(name)
        if(cities == [] or name == ""):
            return render(request, "index2.html")
        else:
            name = request.POST['city']
            source = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?q=' +
                                            name + "&units=metric&appid=99254f7b204303d3e6a93b74c0d786be").read()
            list_of_data = json.loads(source)
            curr_date = date.today()

            today = date.today()

            data = {"temperature": str(list_of_data["main"]["temp"])[:2],
                    "minimumtemperature": str(list_of_data["main"]["temp_min"])[:2],
                    "maximumtemperature": str(list_of_data["main"]["temp_max"])[:2],
                    "realfeel": str(list_of_data["main"]["feels_like"])[:2],
                    "humidity": str(list_of_data["main"]["humidity"]),
                    "pressure": str(list_of_data["main"]["pressure"]),
                    "windspeed": str(list_of_data["wind"]["speed"]),
                    "visible": str(list_of_data["visibility"]),
                    "cityname": str(name),
                    "todayday": str(calendar.day_name[curr_date.weekday()]),
                    "desc": str(list_of_data["weather"][0]["description"]),
                    "date": str(today.strftime("%d %B")),
                    "icon": list_of_data['weather'][0]['icon'],
                    }

            app_id = "99254f7b204303d3e6a93b74c0d786be"
            name_of_the_place = name

            base_url = "http://api.openweathermap.org/data/2.5/forecast"
            complete_url = urllib.request.urlopen(
                base_url + "?q=" + name_of_the_place + "&appid=" + app_id).read()

            json_data = json.loads(complete_url)

            name_of_the_city = json_data['city']['name']
            print(name_of_the_city)

            dic = {}
            new = []
            dic2 = {}
            new3 = []
            for item in json_data['list']:
                time_forecasted = str(item['dt_txt']).split()
                a = time_forecasted[0]
                datee = a[-2]+a[-1]
                monthh = str(a[5]+a[6])
                st = datee+" "+months[monthh]
                if(st not in new3):
                    new3.append(st)
                temp = str(int(item['main']['temp']-273.15))
                weather_des = item['weather'][0]['description']

                if a in dic2:
                    pass
                else:
                    dic2[a] = weather_des

                if a in dic:
                    pass
                else:
                    dic[a] = [temp]

            for item in json_data['list']:
                time_forecasted = str(item['dt_txt']).split()
                a = time_forecasted[0]
                temp = str(int(item['main']['temp']-273.15))
                if(a not in new):
                    new.append(a)
                dic[a].append(temp)

            new1 = []
            new2 = []
            for i in new:
                a = dic[i]
                a.sort()
                s = a[0]+"°C"+"-"+a[-1]+"°C"
                new1.append(s)
                new2.append(dic2[i])

            data2 = {
                "firstdaydate": str(new3[0]),
                "firstdaytemp": str(new1[0]),
                "firstdaydesc": str(new2[0]),

                "seconddaydate": str(new3[1]),
                "seconddaytemp": str(new1[1]),
                "seconddaydesc": str(new2[1]),

                "thirddaydate": str(new3[2]),
                "thirddaytemp": str(new1[2]),
                "thirddaydesc": str(new2[2]),

                "fourthdaydate": str(new3[3]),
                "fourthdaytemp": str(new1[3]),
                "fourthdaydesc": str(new2[3]),

                "fivedaydate": str(new3[4]),
                "fivedaytemp": str(new1[4]),
                "fivedaydesc": str(new2[4]),

                "sixdaydate": str(new3[5]),
                "sixdaytemp": str(new1[5]),
                "sixdaydesc": str(new2[5]),
            }
    else:
        data = {}
        data2 = {}
    return render(request, "index.html", {"information": data, "information2": data2})


def secondfunction(request):
    return render(request, "index1.html")