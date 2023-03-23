from django.urls import include, path
from . import views

app_name = 'votacao'
urlpatterns = [

 # ex: votacao/
 path("", views.index, name='index'),

 # ex: votacao/1
 path('<int:questao_id>', views.detalhe,name='detalhe'),

 # ex: votacao/3/resultados
 path('<int:questao_id>/resultados', views.resultados, name='resultados'),

 # ex: votacao/5/voto
 path('<int:questao_id>/voto', views.voto, name='voto'),

 # ex: votacao/createquestion
 path('createquestion', views.createquestion, name='createquestion'),

 # ex: votacao/5/createoption
 path('<int:questao_id>/createoption', views.createoption, name='createoption'),

 path('login', views.loginview, name='loginview'),

 path('userlogin', views.userlogin, name="userlogin"),

 path('registar', views.registar, name= "registar"),

 path('userregister', views.userregister, name="userregister")

]
