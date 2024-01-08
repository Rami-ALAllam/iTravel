

from django.shortcuts import render ,redirect
from.models import *
from django.contrib import messages
import bcrypt

# ************************************************************************************
# ***************************** Log/Reg **********************************************
# ************************************************************************************

def loginpage(request):   
    
    if 'id'  in  request.session :
        context={
            'page':1
        }
        return render(request,'log.html',context )
    else:
        return render(request,'log.html' )

def login(request):
    user1=Guest.objects.filter(email=request.POST['email'])
    if user1:
        user=user1[0]
        if bcrypt.checkpw(request.POST['pwd'].encode(), user.password.encode()):
            request.session['id']=user.id
            request.session['username'] = user.first_name
            return redirect('/')
        else:
            messages.error(request,"incorrect password")
            return redirect ("/logpage")
    else:
        messages.error(request,"incorrect username or password")
        return redirect ("/logpage")

def newaccount(request):
    if 'id'  in  request.session :
        context={
            'page':1
        }  
        return render(request,'reg.html',context )
    else:
            
        return render(request,'reg.html')

def regestration_user(request):
    errors=Guest.objects.basic_validater(request.POST)
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/newaccount')
    else:
        password=request.POST['pwd']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        x = Guest.add_guest(
            first=request.POST['fname'],
            last=request.POST['lname'],
            birth1=request.POST['bdate'],
            email1=request.POST['email'],
            pass1=pw_hash 
            )
        request.session['id'] = x.id
        request.session['username'] = x.first_name
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def search(request):
    print('Motaz')
    print(request.POST['search_ajax'])
    if len(request.POST['search_ajax']) <3 :
        return render(request,'search.html',{"search": []})
    search = Package.objects.filter(package_destination__contains=request.POST['search_ajax'])
    if search:
        print(request.POST['search_ajax'])
        for items in  search.all():
            print(items.package_destination)
        context={
            'search':search.all()
        }
            
    return render(request,'search.html',context)

# ************************************************************************************
# ***************************** Main *************************************************
# ************************************************************************************

def home(request):
    if 'id'  in  request.session :
        context={
            'page':1,
            'logged':request.session['username']
        }
        return render(request,'index.html',context )
    else:
        return render(request,'index.html' )

# ************************************************************************************
# ***************************** About-Us *********************************************
# ************************************************************************************

def aboutus(request):
    if 'id'  in  request.session :
        context={
            'page':1,
            'allfeedback':Feedback.objects.all()
        }
        return render(request,'about.html',context )
    else:
        context={
            'allfeedback':Feedback.objects.all()
        }
        return render(request,'about.html',context )

# ************************************************************************************
# ***************************** Service *********************************************
# ************************************************************************************

def service_page(request):
    if 'id'  in  request.session :
        context={
            'page':1
        }
        return render(request,'service.html' ,context)
    else:
        return render(request,'service.html' )

# ************************************************************************************
# ***************************** Hotel ************************************************
# ************************************************************************************

def add_hotel(request):
    if 'id' not in request.session:
        messages.error(request,"you must log in ")
        return redirect ('/logpage')
    if request.session['id'] == 1:
        if request.session['id']==1:
            context={
            'which':1,
        }
            return render(request,'add-hotel.html',context)
        else:
            messages.error(request,"you are not admin  ")
            return redirect('/logpage')

def addhotel(request):
    error=Hotel.objects.basic_validation(request.POST)
    if len(error)>0:
        for key,value in error.items():
            messages.error(request,value)
        return redirect('/addhotel')
    else:
        Hotel.add_hotel(
            request.POST['hname'],
            request.POST['roomtype'],
            request.POST['hotel_des']
            )
    return redirect('/addhotel')

def allhotels(request):
    if 'id'  in  request.session :
        context={
            'page':1,
            'allhotel':Hotel.objects.all()
        }
        return render(request,'allhotel.html',context )
    else:
        context={
            'allhotel':Hotel.objects.all()
        }
        return render(request,'allhotel.html',context )

def deletehotel (request,idhotel):
    hotel1=Hotel.objects.get(id=int(idhotel))
    hotel1.delete()
    return redirect('/allhotels')

def edithotel(request,edithotel_id):
    if 'id' not in request.session:
        messages.error(request,"you must log in ")
        return redirect ('/logpage')
    if request.session['id'] == 1:
        if request.session['id']==1:
            context={
            'which':1,
            'onehotel':Hotel.objects.get(id=int(edithotel_id)),
        }
        
            return render(request,'edithotel.html',context)
        else:
            messages.error(request,"you are not admin  ")
            return redirect('/logpage')

def makeedit(request,num2):
    error=Hotel.objects.basic_validation(request.POST)
    if len(error)>0:
        for key,value in error.items():
            messages.error(request,value)
        return redirect('/edit/'+str(num2))
    else:
        Hotel1=Hotel.objects.get(id=int(num2))
        Hotel1.hotel_name=request.POST['hname']
        Hotel1.type_ofroom=request.POST['roomtype']
        Hotel1.hotel_description=request.POST['hotel_des']
        Hotel1.save()
        return redirect('/allhotels')

# ************************************************************************************
# ***************************** Event ************************************************
# ************************************************************************************

def addevent(request):
    if 'id' not in request.session:
        messages.error(request,"you must log in ")
        return redirect ('/')
    if request.session['id'] == 1:
        if request.session['id']==1:
            context={
            'which':1,
        }
            return render(request,'add-event.html',context)
        else:
            messages.error(request,"you are not admin  ")
            return redirect('/')

def add_event (request):
    eror=Event.objects.validation(request.POST)
    if len(eror)>0:
        for key,value in eror.items():
            messages.error(request,value)
        return redirect('/addevent')
    else:
        Event.add_event(e_name=request.POST['ename'],e_type=request.POST['etype'],e_desc=request.POST['event_des'])
        return redirect('/addevent')

def allevents(request):
    if 'id'  in  request.session :
        context={
            'page':1,
            'allevent':Event.objects.all()
        }
        return render(request,'allevents.html',context )
    else:
        context={
            'allevent':Event.objects.all()
        }
        return render(request,'allevents.html',context )

def delte_event(request,num_event):
    event1=Event.objects.get(id=int(num_event))
    event1.delete()
    return redirect('/allevents')

def edit_event(request,num10):
    if 'id' not in request.session:
        messages.error(request,"you must log in ")
        return redirect ('/')
    if request.session['id'] == 1:
        if request.session['id']==1:
            context={
            'which':1,
            'oneevent':Event.objects.get(id=int(num10)),
            
        }
            return render(request,'editevent.html',context)
        else:
            messages.error(request,"you are not admin  ")
            return redirect('/')
        

def  makeedit_event(request,id10):
    eror=Event.objects.validation(request.POST)
    if len(eror)>0:
        for key,value in eror.items():
            messages.error(request,value)
        return redirect('/editevent/'+str(id10))
    else:
        event1=Event.objects.get(id=int(id10))
        event1.event_name=request.POST['ename']
        event1.event_type=request.POST['etype']
        event1.event_description=request.POST['event_des']
        event1.save()
        return redirect('/allevents')

# ************************************************************************************
# ***************************** Package **********************************************
# ************************************************************************************

def Packagespage(request):
    
    if 'id'  in  request.session :
        context={
            'page':1 ,
            'all_package':Package.objects.all(),
            'oneuser': Guest.objects.get(id=request.session['id'])
        }
        return render(request,'package.html',context )
    else:
            context={
        'all_package':Package.objects.all()
    }
        
            return render(request,'package.html',context )

def addpackage (request):
    if 'id' not in request.session:
        messages.error(request,"you must log in ")
        return redirect ('/')
    if request.session['id'] == 1:
        if request.session['id']==1:
            context={
            'which':1,
            'allhotel':Hotel.objects.all(),
            'allevent':Event.objects.all(),
        }
        
            return render(request,'add-package.html',context)
        else:
            messages.error(request,"you are not admin  ")
            return redirect('/')

def add_package(request,):
    erors=Package.objects.validat(request.POST)
    if len(erors)>0:
        for key,value in erors.items():
            messages.error(request,value)
        return redirect('/addpackage')
    else:
        package1=Package.objects.create(
            package_destination=request.POST['dest'],
            package_type=request.POST['type'],
            package_duration=request.POST['duration'],
            number_of_person=request.POST['number'],
            start_date=request.POST['strat'],
            end_date=request.POST['end'],
            package_description=request.POST['package_des'],
            location=request.POST['loc'],
            img=request.POST['picture'],
            package_price=request.POST['price']
        )
        hotel=request.POST['hname']
        evnt=request.POST['ename']
        event1=Event.objects.get(id=int(evnt))
        hotel1=Hotel.objects.get(id=int(hotel))
        package1.events.add(event1)
        package1.hotels.add(hotel1)
        return redirect('/addpackage')

def updatepack(request,id):
    Package.update(
        id,
        request.POST['dest'],
        request.POST['type'],
        request.POST['price'],
        request.POST['package_des'],
        request.POST['duration'],
        request.POST['number'],
        request.POST['strat'],
        request.POST['end'],
        request.POST['picture'],
        request.POST['loc'],
    )
    return redirect('/Packages')

def editpack(request,id):
    context={
        'pack':Package.objects.get(id=int(id)),
        'allhotel':Hotel.objects.all(),
        'allevent':Event.objects.all(),
    }
    return render(request,"editpack.html",context)

def delpack(request,id):
    r = Package.objects.get(id=int(id))
    r.delete()
    return redirect('/Packages')

def showpack(request,id):
    if 'id'  in  request.session :
        context={
            'pack':Package.objects.get(id=int(id)),
            'page':1,
            'oneuser1': Guest.objects.get(id=request.session['id']),
        }
        return render(request,"show.html",context)
    else:
        context={
            'pack':Package.objects.get(id=int(id)),
        }
    return render(request,"show.html",context)

# ************************************************************************************
# ***************************** FeedBack *********************************************
# ************************************************************************************

def contact_page (request):
    if 'id'  in  request.session :
        context={
            'page':1
        }
        return render(request,'contact.html' ,context)
    else:
    
        return render(request,'contact.html' )

def feedback(request):
    if 'id' not in request.session:
        messages.error(request,"You must log in first")
        return redirect('/contact')
    else:
        if request.POST['img'] == '':
            Feedback.objects.create(
                guest_feed=Guest.objects.get(id=request.session['id']),
                country = request.POST['country'],
                description=request.POST['package_feed'],
        )
        else:
            Feedback.objects.create(
                guest_feed=Guest.objects.get(id=request.session['id']),
                img = request.POST['img'],
                country = request.POST['country'],
                description=request.POST['package_feed'],
            )
        return redirect('/about')

def delfeed(request,id):
    r = Feedback.objects.get(id=int(id))
    r.delete()
    return redirect('/about')

# ************************************************************************************
# ***************************** Booking **********************************************
# ************************************************************************************

def booknow(request ,id):
    if 'id' not in request.session:
        messages.error(request,"You must log in first")
        return redirect('/newaccount')
    else: 
        context={
            'package' : int(id),
            'package1' : Package.objects.get(id=int(id)),
            'page':1
        }
        return render(request,'booking1.html' ,context)

def booking (request,num):
    pkg1=Package.objects.get(id=int(num))
    book1= Booking.objects.create(
        guest=Guest.objects.get(id=request.session['id']),
        package=pkg1
        )

    Bill.objects.create(
        region=request.POST['regon'],
        year=request.POST['card_expy'],
        month=request.POST['card_expy'],
        phone_number=request.POST['phone'],
        method=request.POST['payment'],
        firstname_visa=request.POST['fname_visa'],
        lastname_visa=request.POST['lname_visa'],
        visa=request.POST['cnumber'],
        cvc=request.POST['cvcnumber'],
        booking=book1
        )
    return redirect('/booked')

def booked(request):
    if 'id'  in  request.session :
        context={
            'page':1,
            'allbook':Booking.objects.filter(guest=Guest.objects.get(id=request.session['id']))
        }
        return render(request,'booked.html',context )
    else:
        context={
        'allbook':Booking.objects.filter(guest=Guest.objects.get(id=request.session['id'])) 
        }
        return render(request,'booked.html' ,context)

# ************************************************************************************
# ***************************** WishList **********************************************
# ************************************************************************************

def wish(request):
    if 'id'  in  request.session :
        context={
            'page':1,
            'userwish':Guest.objects.get(id=request.session['id'])
        }  
        return render(request,'wishlist.html',context )
    else: 
        return render(request,'wishlist.html')

def likepackage(request,pacid):
    if 'id' not in request.session:
        messages.error(request,"you must log in ")
        return redirect ('/logpage')
    else:
        user1=Guest.objects.get(id=int(request.session['id']))
        package1=Package.objects.get(id=int(pacid))
        package1.likes_package.add(user1)
    return redirect('/wishlist')

def unlikepackage(request,pacid):
    if 'id' not in request.session:
        messages.error(request,"you must log in ")
        return redirect ('/logpage')
    else:
        user1=Guest.objects.get(id=int(request.session['id']))
        package1=Package.objects.get(id=int(pacid))
        package1.likes_package.remove(user1)
    return redirect('/wishlist')