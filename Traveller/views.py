from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from . import models
from . import forms
# Create your views here.
def home(request):
    dests= models.destination.objects.all()[:6]
    testimonial= models.testimonial.objects.all()
    slider_info=[
        {'val':'1','name':'India','desc':"India is known for its rich cultural heritage and an element of mysticism."},
        {'val':'2','name':'Australia','desc':'Australia boasts stunning coastlines, iconic landmarks and unique wildlife.'},
        {'val':'3','name':'Switzerland','desc':'Switzerland, known for its breathtaking Alpine landscapes, is a paradise for nature lovers.'}
    ]
    pop_des=models.pop_dest.objects.all()
    return render(request,'index.html' ,{'dests':dests,'testimonial':testimonial,'slider_info':slider_info,'pop_des':pop_des})

def about(request):
    return render(request,'aboutus.html')

def contact(request):
    if request.method=='POST':
        form=forms.ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')
        else:
            return render(request, 'contact.html', {'form': form})
    form=forms.ContactForm()
    return render(request, 'contact.html',{'form':form})

def destination(request):
    country = request.GET.get('country')
    days = request.GET.get('days')
    price_range = request.GET.get('price_range')

    dests = models.destination.objects.all()

    if country:
        dests = dests.filter(cont=country)
    if days:
        dests = dests.filter(days=days)
    if price_range:
        price_range = price_range.replace('$', '').strip()
        min_price, max_price = map(int, price_range.split('-'))
        dests = dests.filter(price__gte=min_price, price__lte=max_price)

    return render(request, 'destination.html', {'dests': dests})


def travelplace(request, id):
    destin = get_object_or_404(models.destination, id=id)
    days = models.DestinationDay.objects.filter(name=destin).order_by('day_number')
    dests= models.destination.objects.all()[:3]
    is_authenticated = request.user.is_authenticated
    return render(request, 'travelplace.html',{'dests':dests,'destination': destin, 'days': days, 'is_authenticated':is_authenticated})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', request.GET.get('next', reverse('home')))

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect(next_url)
        else:
            messages.warning(request, "Invalid Credentials")
            return redirect(reverse('login') + f'?next={next_url}')
    else:
        next_url = request.GET.get('next', reverse('home'))
        return render(request, "login.html", {'next': next_url})

def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form=forms.RegisterForm()
    return render(request,'register.html',{
        'form': form,
    })

def logout(request):
    auth.logout(request)
    return redirect("/")

@login_required
def myprofile(request):
    user=request.user
    name=user
    email=user.email
    lname=user.last_name
    fname=user.first_name
    profile_picture = user.profile_picture.url if user.profile_picture else None
    count=models.BookTrip.objects.filter(user=name).count()
    return render(request,'myprofile.html',{'name':name,'email':email,'count':count,'lname':lname,'fname':fname, 'profile_picture':profile_picture})

def search_destination(request):
    if request.method == 'POST':
        search_term = request.POST.get('search_query', None)
        if search_term:
            matching_destination = models.destination.objects.filter(name=search_term).first()
            if matching_destination:
                return redirect('travelplace', id=matching_destination.id)
    return redirect('destination')


@login_required
def bookthetrip(request, id):
    destin = get_object_or_404(models.destination, id=id)
    if request.method == 'POST':
        form = forms.BookTripForm(request.POST)
        if form.is_valid():
            book_trip = form.save(commit=False)
            book_trip.user = request.user
            book_trip.destination = destin
            book_trip.save()
            return redirect('mytrips')
        else:
            messages.warning(request,"The Trip Booking is Unsuccessful. Please checkout the errors and complete the Trip Booking correctly")
            return render(request, 'travelplace.html', {'form': form, 'destination': destin})
    else:
        form = forms.BookTripForm()
    return render(request, 'travelplace.html', {'form': form, 'destination': destin})


def tripquery(request, id):
    destin = get_object_or_404(models.destination, id=id)
    
    if request.method == 'POST':
        form = forms.QueryForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.destination = destin
            query.save()
            return redirect('travelplace',id)
    else:
        form = forms.QueryForm()
    return render(request, 'travelplace.html', {'form': form, 'destination': destin})


@login_required
def mytrips(request):
    user = request.user
    bookings = models.BookTrip.objects.filter(user=user).order_by('start_date')
    return render(request, 'mytrips.html', {'bookings': bookings})


@login_required
def editprofile(request):
    if request.method == 'POST':
        form = forms.EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('myprofile')
    else:
        form = forms.EditProfileForm(instance=request.user)
    return render(request, 'editprofile.html', {'form': form})