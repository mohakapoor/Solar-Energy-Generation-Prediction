from django.shortcuts import render
from main import predict_for_coords
from main_rfr import predict_for_coords_rfr

def solar_energy_prediction(request):
    energy_generated = None  
    
    if request.method == 'POST':
        model_selected = request.POST.get('model')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if latitude and longitude:
            try:
                latitude = float(latitude)
                longitude = float(longitude)

                if model_selected == 'prophet':
                    energy_generated = predict_for_coords(latitude, longitude)
                elif model_selected == 'rfr':
                    energy_generated = predict_for_coords_rfr(latitude, longitude)
                else:
                    return render(request, 'power_app/input.html', {'error': 'Invalid model selected. Please choose a valid model.'})
            except ValueError:
                return render(request, 'power_app/input.html', {'error': 'Invalid coordinates. Please enter valid numbers.'})
        else:
            return render(request, 'power_app/input.html', {'error': 'Please enter both latitude and longitude.'})
    
    
    return render(request, 'power_app/input.html', {'energy_generated': energy_generated})

def model_page(request):
    return render(request, 'power_app/model.html')

def idea_page(request):
    return render(request, 'power_app/idea.html')

def input_page(request):
    return render(request, 'power_app/input.html')

def about_us_page(request):
    return render(request, 'power_app/about_us.html')