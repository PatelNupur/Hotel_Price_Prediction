import pickle
from datetime import datetime
from django.shortcuts import render, redirect
import openpyxl
from django.contrib import messages
from django.http import JsonResponse
from .events import events
from datetime import date
from .weather_forecast import weather_report
from django.contrib.auth.decorators import login_required

# Create your views here.

ratemodel_file = 'modelXGB84.pkl'
occupancymodel_file = 'modeloccupancy.pkl'

# Loading saved model
loaded_ratemodel = pickle.load(
    open(f'D:\Price_prediction\pythonProject\hotel_price_prediction\price_prediction\{ratemodel_file}', 'rb'))


# loaded_occupancymodel = pickle.load(open(f'D:\Price_prediction\pythonProject\hotel_price_prediction\price_prediction\{occupancymodel_file}', 'rb'))


def trackcode(track_code):
    if track_code == "Corporate":
        return 0

    if track_code == "LEISURE":
        return 1

    if track_code == "Meeting Room":
        return 2

    if track_code == "Walk-In":
        return 3

    if track_code == "Missing":
        return 4


def roomtype(room_type):
    if room_type == "NHK":
        return 0

    if room_type == "NHQQ":
        return 1

    if room_type == "NK":
        return 2

    if room_type == "NQQ":
        return 3

    if room_type == "SNHK":
        return 4

    if room_type == "SNK":
        return 5

    if room_type == "SNQQ":
        return 6


def ratecode(rate_code):
    if rate_code == "BAR":
        return 0

    if rate_code == "Group":
        return 1

    if rate_code == "LBLREP":
        return 4

    if rate_code == "LCLC":
        return 5

    if rate_code == "LEXP":
        return 9

    if rate_code == "LOPQ":
        return 20

    if rate_code == "LOPQ2":
        return 21

    if rate_code == "LPSR":
        return 24

    if rate_code == "LPSS":
        return 25

    if rate_code == "S3A":
        return 41

    if rate_code == "SBOOK":
        return 58

    if rate_code == "SCPM":
        return 64

    if rate_code == "SGML":
        return 72

    if rate_code == "SNP":
        return 78

    if rate_code == "SRD Rate":
        return 103

    if rate_code == "SRTL":
        return 104

    if rate_code == "SSC":
        return 106


def price(request):
    if request.user.is_authenticated:
        return render(request, "price_prediction.html")
    else:
        return redirect('/auth/login')


def price_prediction(request):
    if request.user.is_authenticated:
        input_date = request.POST['date']

        if input_date == "":
            return JsonResponse({'status': 0, 'message': 'date required!!'})

        else:
            forecast_WB = openpyxl.load_workbook('price_prediction/forecast_df.xlsx')
            forecast_Sheet = forecast_WB.active

            forecast_revenue_WB = openpyxl.load_workbook('price_prediction/forecast_revenue_df.xlsx')
            forecast_revenue_Sheet = forecast_revenue_WB.active

            date_list = forecast_Sheet["B"][1:]
            yhat_list = forecast_Sheet["T"][1:]
            revenue_list = forecast_revenue_Sheet["T"][1:]
            # Getting saved model data
            for i, j in zip(date_list, yhat_list):

                if str(i.value.date()) == str(input_date):
                    ds = str(i.value.date())
                    predicted_occupancy = j.value
                    request.session["predicted_occupancy"] = predicted_occupancy
                    Occupancy_percent = int((predicted_occupancy * 100) / 110)
                    request.session['occupancy_percent'] = Occupancy_percent

            for date, revenue in zip(date_list, revenue_list):

                if str(date.value.date()) == str(input_date):
                    predicted_revenue = revenue.value
                    request.session['predicted_revenue'] = predicted_revenue
                    context = {
                        'ds': ds,
                        'predicted_occupancy': round(predicted_occupancy),
                        'predicted_revenue': round(predicted_revenue),
                    }
        return JsonResponse({'status': 1, 'data': context})


def rate(request):
    if request.user.is_authenticated:
        return render(request, "rate_prediction.html")
    else:
        return redirect('/auth/login')


# Rate according to LOS
def updated_rate(Los, Occupancy_percent, predicted_rate):
    if int(Los) <= 3:
        if 0 <= Occupancy_percent < 11:
            occ_rate = round(0.80 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 11 <= Occupancy_percent < 21:
            occ_rate = round(0.83 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 21 <= Occupancy_percent < 31:
            occ_rate = round(0.85 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 31 <= Occupancy_percent < 41:
            occ_rate = round(0.88 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 41 <= Occupancy_percent < 51:
            occ_rate = round(0.90 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 51 <= Occupancy_percent < 61:
            occ_rate = round(0.93 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 61 <= Occupancy_percent < 71:
            occ_rate = round(0.95 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 71 <= Occupancy_percent < 81:
            occ_rate = round(0.98 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 81 <= Occupancy_percent < 91:
            occ_rate = round(1.05 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 91 <= Occupancy_percent <= 100:
            occ_rate = round(1.1 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            print(occ_rate)
            return context

    if 3 < int(Los) <= 5:
        if 0 <= Occupancy_percent < 11:
            occ_rate = round(0.78 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 11 <= Occupancy_percent < 21:
            occ_rate = round(0.80 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 21 <= Occupancy_percent < 31:
            occ_rate = round(0.83 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 31 <= Occupancy_percent < 41:
            occ_rate = round(0.85 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 41 <= Occupancy_percent < 51:
            occ_rate = round(0.88 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 51 <= Occupancy_percent < 61:
            occ_rate = round(0.90 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 61 <= Occupancy_percent < 71:
            occ_rate = round(0.93 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 71 <= Occupancy_percent < 81:
            occ_rate = round(0.95 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 81 <= Occupancy_percent < 91:
            occ_rate = round(int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 91 <= Occupancy_percent <= 100:
            occ_rate = round(1.1 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            print(occ_rate)
            return context

    if 5 < int(Los) <= 7:
        if 0 <= Occupancy_percent < 11:
            occ_rate = round(0.80 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 11 <= Occupancy_percent < 21:
            occ_rate = round(0.83 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 21 <= Occupancy_percent < 31:
            occ_rate = round(0.85 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 31 <= Occupancy_percent < 41:
            occ_rate = round(0.88 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 41 <= Occupancy_percent < 51:
            occ_rate = round(0.90 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 51 <= Occupancy_percent < 61:
            occ_rate = round(0.93 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 61 <= Occupancy_percent < 71:
            occ_rate = round(0.95 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 71 <= Occupancy_percent < 81:
            occ_rate = round(0.98 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 81 <= Occupancy_percent < 91:
            occ_rate = round(1.1 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 91 <= Occupancy_percent <= 100:
            occ_rate = round(1.2 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            print(occ_rate)
            return context

    if 7 < int(Los) <= 10:
        if 0 <= Occupancy_percent < 11:
            occ_rate = round(0.85 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 11 <= Occupancy_percent < 21:
            occ_rate = round(0.88 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 21 <= Occupancy_percent < 31:
            occ_rate = round(0.90 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 31 <= Occupancy_percent < 41:
            occ_rate = round(0.93 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 41 <= Occupancy_percent < 51:
            occ_rate = round(0.95 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 51 <= Occupancy_percent < 61:
            occ_rate = round(0.98 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 61 <= Occupancy_percent < 71:
            occ_rate = round(1.05 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 71 <= Occupancy_percent < 81:
            occ_rate = round(1.1 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 81 <= Occupancy_percent < 91:
            occ_rate = round(1.2 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 91 <= Occupancy_percent <= 100:
            occ_rate = round(1.3 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            print(occ_rate)
            return context

    if 10 < int(Los) <= 15:
        if 0 <= Occupancy_percent < 11:
            occ_rate = round(0.85 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 11 <= Occupancy_percent < 21:
            occ_rate = round(0.88 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 21 <= Occupancy_percent < 31:
            occ_rate = round(0.90 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 31 <= Occupancy_percent < 41:
            occ_rate = round(0.93 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 41 <= Occupancy_percent < 51:
            occ_rate = round(0.98 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 51 <= Occupancy_percent < 61:
            occ_rate = round(1.02 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 61 <= Occupancy_percent < 71:
            occ_rate = round(1.07 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 71 <= Occupancy_percent < 81:
            occ_rate = round(1.15 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 81 <= Occupancy_percent < 91:
            occ_rate = round(1.2 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            return context
        if 91 <= Occupancy_percent <= 100:
            occ_rate = round(1.3 * int(predicted_rate))
            context = {
                'occ_rate': occ_rate
            }
            print(occ_rate)
            return context


# Rate according to Event
def updated_rate_date(date_time, rate_los):
    if date_time == '2023-01-01' or '2023-01-02' or '2023-01-16' or '2023-02-20' or '2023-04-09' or '2023-05-14' or '2023-05-29' or '2023-06-18' or '2023-06-19' or '2023-07-04' or '2023-09-04' or '2023-10-02' or '2023-10-09' or '2023-11-11' or '2023-11-13' or '2023-11-23' or '2023-11-24' or '2023-12-25' or '2023-12-27':
        predicted_rate = round(1.1 * int(rate_los))
        context = {
            'predicted_rate': predicted_rate
        }
        return context
    else:
        context = {
            'rate_los': rate_los
        }
        return context


def rate_prediction(request):
    if request.user.is_authenticated:
        date_time = request.POST['date']
        Los = request.POST['length_of_stay']
        track_code = request.POST['track_code']
        room_type = request.POST['room_type']
        rate_code = request.POST['rate_code']
        Occupied = request.session["predicted_occupancy"]
        Adr = int(request.session['predicted_revenue']) / int(Occupied)

        if date_time == "":
            return JsonResponse({'status': 0, 'message': "Provide Date!!"})
        else:
            date_object = datetime.strptime(date_time, '%Y-%m-%d').date()

        if Los == "":
            return JsonResponse({'status': 0, 'message': "Provide Length of Stay!!"})

        if room_type == "" or room_type == "Room Type":
            return JsonResponse({'status': 0, 'message': "Select Room Type!!"})

        if track_code == "" or track_code == "Track Code":
            return JsonResponse({'status': 0, 'message': "Select Track Code!!"})

        if rate_code == "" or rate_code == "Rate Code":
            return JsonResponse({'status': 0, 'message': "Select Rate Code!!"})

        else:
            context = {}
            date = date_time.split("-")
            month = date[1]
            days = date[2]
            # PREDICTION
            n = [[int(month), int(days), int(Los), trackcode(track_code), roomtype(room_type), ratecode(rate_code),
                  Occupied, Adr]]
            predicted_rate1 = loaded_ratemodel.predict(n)
            predicted_rate = predicted_rate1[0]
            Occupancy_percent = request.session['occupancy_percent']
            a = updated_rate(Los, Occupancy_percent, predicted_rate)
            rate_los = a["occ_rate"]
            rate_event = updated_rate_date(date_time, rate_los)
            context['predicted_rate'] = rate_event

            # WEATHER REPORT
            wea_forecast = weather_report()
            for weather in wea_forecast:
                months = int(weather['date'].split("/")[0])
                day = int(weather['date'].split("/")[1])
                weather_forecast_date = datetime(2023, months, day).date()
                if str(date_time) == str(weather_forecast_date):
                    weather_data = wea_forecast[wea_forecast.index(weather)]
                    context['weather_data'] = weather_data

            # HOLIDAY LIST
            holidaysList = events()
            for holyLst in holidaysList:
                if holyLst['date'] == date_object.strftime("%b %d"):
                    context['holiday'] = holyLst['holidays']
                    break
                else:
                    pass

            return JsonResponse({'status': 1, "data": context})
    else:
        return redirect('/auth/login')
