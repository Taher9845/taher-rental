from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Property, UserProfile, RentalApplication
from .form import PropertyForm


def property_list(request):
    properties = Property.objects.all()
    return render(request, 'rental/property_list.html', {'properties': properties})


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'rental/property_detail.html', {'property': property})


def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.owner = request.user
            prop.save()
            return redirect('owner_dashboard')
    else:
        form = PropertyForm()
    return render(request, 'rental/property_form.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('property_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def dashboard(request):
    profile = request.user.userprofile
    if profile.role == 'owner':
        return render(request, 'dashboard/owner_dashboard.html')
    elif profile.role == 'tenant':
        return render(request, 'dashboard/tenant_dashboard.html')


def owner_dashboard(request):
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'rental/owner_dashboard.html', {'properties': properties})


def tenant_applications(request):
    my_apps = RentalApplication.objects.filter(tenant=request.user)
    return render(request, 'rental/tenant_applications.html', {'applications': my_apps})

def apply_for_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    # Prevent duplicate applications
    if not RentalApplication.objects.filter(property=property_obj, tenant=request.user).exists():
        RentalApplication.objects.create(property=property_obj, tenant=request.user)
    return redirect('property_list')

def view_applications(request):
    if request.user.userprofile.role == 'owner':
        applications = RentalApplication.objects.filter(property__owner=request.user)
        return render(request, 'rental/owner_applications.html', {'applications': applications})
    
def update_application_status(request, application_id, status):
    application = get_object_or_404(RentalApplication, id=application_id)
    if application.property.owner == request.user:
        application.status = status
        application.save()
    return redirect('view_applications')

def apply_for_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('tenant_name')
        email = request.POST.get('tenant_email')

        RentalApplication.objects.create(
            property=property,
            tenant_name=name,
            tenant_email=email,
        )
        return redirect('property_list')

def application_status(request):
    applications = RentalApplication.objects.all()
    return render(request, 'rental/application_status.html', {'applications': applications})




