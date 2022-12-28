from django.urls import path,include
from Api.views import *


urlpatterns = [
#web urls  home
path('account',account.as_view()),
path('encryptpass',encryptpass.as_view()),
path('admindataadd',admindataadd.as_view()),
path('specificdata',specificdata.as_view()),
path('questions',questions.as_view()),
path('getSpecificquestion',getSpecificquestion.as_view()),
path('addanswer',addanswer.as_view()),
path('getspecificanswerdata',getspecificanswerdata.as_view()),
path('employeeealldata',employeeealldata.as_view()),
]