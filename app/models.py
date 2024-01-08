from django.db import models
import re
from datetime import datetime

class GuestManager(models.Manager):
    def basic_validater(self,postData):
        errors={}
        if len(postData['fname'])<2:
            errors['fname']="firstname should be 2 char atleast"
        fname_regex=re.compile(r'^[a-zA-Z]')
        if not fname_regex.match(postData['fname']):
            errors['fname']="firstname should be char only "
        if len(postData['lname'])<2:
            errors['lname']="lastname should be 2 char atleast"       
        lname_regex=re.compile(r'^[a-zA-Z]')
        if not lname_regex.match(postData['lname']):
            errors['lname']="lastname should be char only "
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = "Invalid email address!"
        if len(Guest.objects.filter(email=postData['email']))>0:
            errors['email']="Email should be uniqe!"
        if len(postData['pwd'])<8:
            errors['pwd']="password should be 8 char atleast"
        if postData['pwd'] != postData['con-pwd']:
            errors['con-pwd']="password dont match"
        if postData['bdate'] == "":
            errors["bdate"] = "Birth date is mandatory"
        else:
            bdate = datetime.strptime(postData['bdate'],'%Y-%m-%d')
            date_num1 = datetime.today().year
            date_num2 = bdate.year
            if datetime.today() < bdate:
                errors["bdate"] = "Birth date should be in the past"
            elif (date_num1 - date_num2) < 18:
                errors["bdate"] = "Age should be 18 years old at least"
        return errors
    
class HotelManager(models.Manager):
    def basic_validation(self,postData):
        error={}
        if len(postData['hotel_des'])<8:
            error['hotel_des']="description should be 8 char at least"
        if len(postData['hname'])<2:
            error['hname']="hotel name  should be 2 char at least"
        if len(Hotel.objects.filter(hotel_name=postData['hname']))>0:
            error['hname']="Hotel name  should be unieq!"
        return error
    
class EventManager(models.Manager):
    def validation(self,postData):
        eror={}
        if len(postData['event_des'])<8:
            eror['event_des']="description should be 8 char at least"
        if len(postData['ename'])<2:
            eror['ename']="hotel name  should be 2 char at least"
        return eror
        
class PackageManager(models.Manager):
    def validat(self,postData):
        erors={}
        if len(postData['dest'])<2:
            erors['dest']="destination  should be 2 char at least"
        if len(postData['type'])<2:
            erors['type']="hotel name  should be 2 char at least"
        due=int(postData['duration'])
        print(due)
        if due < 1:
            erors['duration']="duration should be more than 0"

        people=int(postData['number'])
        if people < 1:
            erors['number']="number of people should be more than 0"
        if len(postData['package_des'])<8:
            erors['package_des']="description  name  should be 8 char at least"

        price1=int(postData['price'])
        if price1 < 1:
            erors['price']="Price should be more than 0"

        return erors

class Guest(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.CharField(max_length=45)
    password=models.CharField(max_length=45)
    is_admin=models.IntegerField(default=0)
    birthday=models.DateField(("Date"), null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=GuestManager()

    def admin():
        if Guest.id == 1:
            is_admin=0
            return is_admin
        else:
            is_admin=1 
            return is_admin

    def add_guest(first,last,email1,pass1,birth1):    
        return Guest.objects.create(
            first_name=first,
            last_name=last,
            email=email1,
            password=pass1,
            birthday=birth1,
            is_admin=Guest.admin())

class Feedback(models.Model):
    guest_feed=models.ForeignKey(Guest,related_name="feedbacks",on_delete=models.CASCADE)
    img=models.CharField(max_length=225, default = "https://as1.ftcdn.net/v2/jpg/03/39/45/96/1000_F_339459697_XAFacNQmwnvJRqe1Fe9VOptPWMUxlZP8.jpg")
    country = models.CharField(max_length=45, default = "USA")
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Event(models.Model):
    event_name=models.CharField(max_length=45)
    event_type=models.CharField(max_length=45)
    event_description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)  
    objects=EventManager()

    def add_event(e_name,e_type,e_desc):
        return Event.objects.create(
            event_name=e_name,
            event_type=e_type,
            event_description=e_desc)

class Hotel(models.Model):
    hotel_name=models.CharField(max_length=45)
    type_ofroom=models.CharField(max_length=45)
    hotel_description=models.TextField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True) 
    objects=HotelManager()

    def add_hotel(name,type,desc): 
        return Hotel.objects.create(
            hotel_name=name,
            type_ofroom=type,
            hotel_description=desc)

class Package(models.Model):
    package_destination=models.CharField(max_length=45,default="nablus")
    package_type=models.CharField(max_length=45)
    package_price=models.IntegerField()
    package_description=models.TextField()
    package_duration=models.IntegerField()
    number_of_person=models.IntegerField(default=2)
    start_date=models.DateTimeField(("Date"), null=True)
    end_date=models.DateTimeField(("Date"), null=True)
    img=models.CharField(max_length=225)
    location=models.TextField(null=True)
    events=models.ManyToManyField(Event,related_name="packages_for_event")
    hotels=models.ManyToManyField(Hotel,related_name="packages_for_hotel")
    likes_package=models.ManyToManyField(Guest,related_name="guest_likes")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=PackageManager()

    def update(pack_id,dest,type,price,desc,duration,number,start,end,pic,loc):
        r = Package.objects.get(id=int(pack_id))
        r.package_destination=dest
        r.package_type=type
        r.package_price=price
        r.package_description=desc
        r.package_duration=duration
        r.number_of_person=number
        r.start_date=start
        r.end_date=end
        r.img=pic
        r.location=loc
        r.save()

class Booking(models.Model):
    guest=models.ForeignKey(Guest,related_name="books",on_delete=models.CASCADE)
    package=models.ForeignKey(Package,related_name="books_package",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)  

class Bill(models.Model):
    # email_palpay=models.CharField(max_length=45,null=True)
    # pass_palpay=models.CharField(max_length=45,null=True)
    # bill_amount=models.IntegerField()
    #expiration=models.DateField(null=True)

    firstname_visa=models.CharField(max_length=45,null=True)
    lastname_visa=models.CharField(max_length=45,null=True)
    cvc=models.IntegerField(default="123")
    visa=models.IntegerField()
    method=models.CharField(max_length=45,null=True)
    phone_number=models.IntegerField(default=123)
    region=models.CharField(max_length=45,null=True)
    booking=models.ForeignKey(Booking,related_name="bills_of_booking",on_delete=models.CASCADE)
    year = models.IntegerField(default="123")
    month=models.IntegerField(default="123")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)  










