from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
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

        in_dir = r'D:\Work\GAFRD_Portal\Model_Data\inputs'
        out_dir = r'D:\Work\GAFRD_Portal\Model_Data\outputs'

        ExecuteModel.run(in_dir, out_dir)

        # return user to required page
        return render(request, 'contact_us.html')
