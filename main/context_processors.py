# main/context_processors.py

def restaurant_name(request):
    return {'restaurant_name': 'Foodie Palace'}  # Or fetch from DB if necessary
