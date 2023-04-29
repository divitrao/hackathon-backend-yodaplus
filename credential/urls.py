from django.urls import path


from . import views

urlpatterns = [

    path('create_get/', 
         views.CreateGetCredentialViewSet.as_view({'post':'create_credential','get':'get_credential'}),
           name='create_get_credential')
  
]
