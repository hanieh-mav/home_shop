from django.shortcuts import render ,get_object_or_404
from django.core.paginator import Paginator
from .models import Listing
from .choices import price_choices , bedroom_choices , state_choices
from contacts.models import Contact

# Create your views here.

def index(request,page=1):
    listings = Listing.objects.order_by('-list_date').filter(is_published = True)
    paginator = Paginator(listings,6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'listings':paged_listings,
    }
    return render(request,'listings/listings.html',context)


def listing(request,listing_id):
    listing = get_object_or_404( Listing ,pk = listing_id , is_published = True)
    #check if user has made inquiry already
    if request.user.is_authenticated:
        user_id = request.user.id
        has_contected = Contact.objects.filter(user_id=user_id,listing_id=listing.id)

    context = {
        'listing':listing,
        'has_contected':has_contected
    }

    return render(request,'listings/listing.html',context)


def search(request):  
    queryset_list = Listing.objects.order_by('-list_date')

    #Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    #city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    #state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state) 

    #bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)  

    #price                 
    if 'price' in request.GET:
        price  = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)


    context = { 
        'price_choices' : price_choices,
        'state_choices' : state_choices,
        'bedroom_choices' : bedroom_choices,
        'listings' : queryset_list,
        'values' : request.GET
        
    }
    return render(request,'listings/search.html',context)
