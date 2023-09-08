from django.shortcuts import render, redirect
from .models import Contact
import os 
from twilio.rest import Client

# Create your views here.

def index(request):
    contacts = Contact.objects.all()
    search_input = request.GET.get('search-area')
    if search_input:
        contacts = Contact.objects.filter(full_name__icontains=search_input)
    else:
        contacts = Contact.objects.all()
        search_input = ''
    return render(request, 'index2.html', {'contacts': contacts, 'search_input': search_input})

def addContact(request):
    if request.method == 'POST':

        new_contact = Contact(
            full_name=request.POST['fullname'],
            relationship=request.POST['relationship'],
            email=request.POST['email'],
            phone_number=request.POST['phone-number'],
            address=request.POST['address'],
            )
        new_contact.save()
        return redirect('/')

    return render(request, 'new2.html')

def editContact(request, pk):
    contact = Contact.objects.get(id=pk)

    if request.method == 'POST':
        contact.full_name = request.POST['fullname']
        contact.relationship = request.POST['relationship']
        contact.email = request.POST['email']
        contact.phone_number = request.POST['phone-number']
        contact.address = request.POST['address']
        contact.save()

        return redirect('/profile/'+str(contact.id))
    return render(request, 'edit.html', {'contact': contact})

def deleteContact(request, pk):
    contact = Contact.objects.get(id=pk)

    if request.method == 'POST':
        contact.delete()
        return redirect('/')

    return render(request, 'delete2.html', {'contact': contact})

def contactProfile(request, pk):
    contact = Contact.objects.get(id=pk)
    return render(request, 'contact-profile.html', {'contact':contact})
# placing call with twilo
def call(request, pk):
    contacts = Contact.objects.get(id=pk)
    contact = contacts.phone_number
    name = contacts.full_name
    name = str(name).upper()
    caller_number = "replace it with your twilio verify number"
    twilio_acc = "replace it with your twilio account"
    auth_token = "replace it with your twilio token"
    client = Client(twilio_acc,auth_token)
    call = client.calls.create(
        url= 'http://demo.twilio.com/docs/voice.xml',
        to = contact,
        from_= caller_number
    )
    #contact_details = call.start_time
    return render(request, 'call.html', {"contact":caller_number, 'info':contact, 'name':name})
