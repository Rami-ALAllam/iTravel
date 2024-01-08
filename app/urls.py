


from django.urls import path
from.import views
urlpatterns = [
    path('',views.home ),
    path('logpage',views.loginpage ),
    path('newaccount',views.newaccount),
    path('login',views.login),
    path('reg',views.regestration_user),
    path('home',views.home,name='homepage'),
    path('search/',views.search),
    path('about',views.aboutus),
    path('service',views.service_page),
    path('contact',views.contact_page),
    path('addhotel',views.add_hotel),
    path('logout',views.logout),
    path('hotel',views.addhotel),
    path('addevent',views.addevent),
    path('event',views.add_event),
    path('addpackage',views.addpackage),
    path('package',views.add_package),
    path('Packages',views.Packagespage),
    path('wishlist',views.wish),
    path('booked',views.booked),
    path('feedback',views.feedback),
    path('booking/<int:id>',views.booknow),
    path('book/<int:num>',views.booking),
# ************************************************************************************************
    path('delfeed/<int:id>',views.delfeed),
    path('delpack/<int:id>',views.delpack),
    path('editpack/<int:id>',views.editpack),
    path('updatepack/<int:id>',views.updatepack),
    path('showpack/<int:id>',views.showpack),
# ************************************************************************************************
    path('allhotels',views.allhotels),
    path('delete/<idhotel>',views.deletehotel),
    path('edit/<edithotel_id>',views.edithotel),
    path('edithotel/<num2>',views.makeedit),
    path('allevents',views.allevents),
    path('deleteevent/<num_event>',views.delte_event),
    path('editevent/<num10>',views.edit_event),
    path('eventedit/<id10>' ,views.makeedit_event),
    path('wish/<pacid>',views.likepackage),
    path('unwish/<pacid>',views.unlikepackage),
]

