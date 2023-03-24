from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Questao, Opcao, Aluno
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



def registar (request):
    return render(request, 'votacao/registpage.html')

def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('votacao:index'))
        else:
            return render(request, 'votacao/loginpage.html')
    else:
        return render(request, 'votacao/loginpage.html')

def userregister (request):
    user = User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password'])
    aluno = Aluno(curso=request.POST['curso'], user =user)
    aluno.save()
    return render(request, 'votacao/loginpage.html')

def userdetails(request):
    return render(request, 'votacao/personalinformation.html')
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:userlogin'))

def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list':latest_question_list}
    return render(request, 'votacao/index.html', context)


def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})


def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})


def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html', {
        'questao': questao,'error_message': "Não escolheu uma opção",})
    else:
        opcao_seleccionada.votos += 1
        opcao_seleccionada.save()
        request.user.aluno.votos += 1
        request.user.aluno.save()
        # Retorne sempre HttpResponseRedirect depois de
        # tratar os dados POST de um form
        # pois isso impede os dados de serem tratados
        # repetidamente se o utilizador
        # voltar para a página web anterior.
    return HttpResponseRedirect(reverse('votacao:resultados', args=[questao.id]))


def createquestion(request):
    try:
        questaotexto = request.POST['qname']
    except(KeyError, Questao.DoesNotExist):
        # Se não demos post de uma questão então mostra a página para criar a questão
        return render(request, 'votacao/createquestion.html')
    else:
        questao = Questao(questao_texto=questaotexto, pub_data=datetime.datetime.now())
        questao.save()
    return HttpResponseRedirect(reverse('votacao:index'))

def deletequestion(request , questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    questao.delete()
    return HttpResponseRedirect(reverse('votacao:index'))

def createoption(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcaotexto = request.POST['opname']
    except(KeyError, Opcao.DoesNotExist):
        # Se não demos post de uma opção então mostra a página para criar a opção
        return render(request, 'votacao/createoption.html', {'questao': questao})
    else:
        opcao = Opcao(questao=questao, opcao_texto=opcaotexto, votos=0)
        opcao.save()
    return HttpResponseRedirect(reverse('votacao:detalhe', args=[questao.id]))


