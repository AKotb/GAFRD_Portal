import base64
import os.path
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render

from gafrd_portal_app.model_tools import TSModel
from gafrd_portal_app.run import ExecuteModel
import geopandas as gpd
from datetime import datetime
import zipfile

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
        model_final_out_files = ["FinalSuitabilityMapModel.tif", "SoilSubModel.tif", "SocioEconomic.tif", "WaterAvailabilitySubModel.tif"]
        polygonRequestDir = os.path.join(ststic_path, "polygons")
        polygonRequest = request.POST.get('polygonCoordinates')
        polygonRequest = eval(polygonRequest)
        polygonRequestName = request.POST.get('name')
        contents = TSModel.clip_using_polygon(model_final_out_files, out_dir, polygonRequest, polygonRequestDir, polygonRequestName)

        # return user to required page
        # return render(request, 'index.html')
        return HttpResponse(contents)
def download_shapefile(request):
    current_dir = os.path.dirname(__file__)
    download_dir = os.path.join(current_dir, 'static/drawn_layers')
    if request.is_ajax and request.method == "POST":
        geoJson = request.POST.get('geoJson')
        compressed_shp_file = create_shp(download_dir, geoJson)

        return HttpResponse(compressed_shp_file)

def create_shp(out_dir, str_geojson):
    datetime_str = datetime.now().strftime('%Y%m%d%H%M%S')
    cur_file = f"drawn_layers_{datetime_str}"
    shp_dir = os.path.join(out_dir, cur_file)
    if not os.path.exists(shp_dir):
        os.mkdir(shp_dir)

    gdf = gpd.read_file(str_geojson)
    gdf.to_file(os.path.join(shp_dir, f"{cur_file}.shp"))

    f_out = zipfile.ZipFile(f"{shp_dir}.zip", "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(shp_dir)
    for dirname, subdirs, files in os.walk(shp_dir):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print(f"zipping {os.path.join(dirname, filename)} as {arcname}")
            f_out.write(absname, arcname)
    f_out.close()
    '''with open(f"{shp_dir}.zip", "rb") as f:
        bytes = f.read()
        encoded = base64.b64encode(bytes)'''
    return f"{cur_file}.zip"