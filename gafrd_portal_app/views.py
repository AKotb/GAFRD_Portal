import os.path
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render

from gafrd_portal_app.model_tools import TSModel
from gafrd_portal_app.run import ExecuteModel


def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html
    return render(request, 'index.html')


def login(request):
    """View function for login page of site."""

    # Render the HTML template login.html
    return render(request, 'login.html')


def contactus(request):
    """View function for contact_us page of site."""

    # Render the HTML template contact_us.html
    return render(request, 'contact_us.html')


def services(request):
    """View function for services page of site."""

    # Render the HTML template services.html
    return render(request, 'services.html')


def elibrary(request):
    """View function for e_library page of site."""

    # Render the HTML template e_library.html
    return render(request, 'e_library.html')


def model_call(request):
    if request.method == 'POST' and 'run_module' in request.POST:
        current_dir = os.path.dirname(__file__)
        in_dir = os.path.join(current_dir, 'static/Model_Data/inputs/Egypt')
        out_dir = os.path.join(current_dir, 'static/Model_Data/outputs/Egypt')

        ExecuteModel.run(in_dir, out_dir)

        # return user to required page
        return render(request, 'contact_us.html')


def run_clip_polygon(request):
    if request.is_ajax and request.method == "POST":
        current_dir = os.path.dirname(__file__)
        out_dir = os.path.join(current_dir, 'static/Model_Data/outputs/Egypt')
        ststic_path = os.path.join(current_dir, 'static')
        model_final_out_files = ["FinalSuitabilityModel.tif", "SoilSubModel.tif", "SocioEconomic.tif", "WaterAvailabilitySubModel.tif"]
        polygonRequestDir = os.path.join(ststic_path, "polygons")
        polygonRequest = request.POST.get('polygonCoordinates')
        polygonRequest = eval(polygonRequest)
        polygonRequestName = request.POST.get('name')
        contents = TSModel.clip_using_polygon(model_final_out_files, out_dir, polygonRequest, polygonRequestDir, polygonRequestName)

        # return user to required page
        # return render(request, 'index.html')
        return HttpResponse(contents)
