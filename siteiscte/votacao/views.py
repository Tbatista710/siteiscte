from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Questao, Opcao, Aluno
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import user_passes_test



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


def userregister(request):
    if request.method == 'POST':
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        aluno = Aluno(curso=request.POST['curso'], user=user, votos=0, grupo=request.POST['grupo'])
        aluno.save()
        return render(request, 'votacao/loginpage.html')
    else:
        return render(request, 'votacao/registpage.html')


@login_required(login_url='/votacao/userlogin')
def userdetails(request):
    return render(request, 'votacao/personalinformation.html')

@login_required(login_url='/votacao/userlogin')
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:userlogin'))

@login_required(login_url='/votacao/userlogin')
def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'votacao/index.html', context)

@login_required(login_url='/votacao/userlogin')
def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})

@login_required(login_url='/votacao/userlogin')
def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})

@login_required(login_url='/votacao/userlogin')
def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html', {
            'questao': questao, 'error_message': "Não escolheu uma opção", })
    else:
        if not request.user.is_superuser:
            num_grupo = request.user.aluno.grupo[-2:]
            if request.user.aluno.votos < int(num_grupo) + 10:
                opcao_seleccionada.votos += 1
                opcao_seleccionada.save()
                request.user.aluno.votos += 1
                request.user.aluno.save()
            else:
                return render(request, 'votacao/detalhe.html', {
                    'questao': questao, 'error_message': "Chegou ao seu limite de votos", })
        else:
            opcao_seleccionada.votos += 1
            opcao_seleccionada.save()
    return HttpResponseRedirect(reverse('votacao:resultados', args=[questao.id]))

@login_required(login_url='/votacao/userlogin')
def createquestion(request):
    try:
        questaotexto = request.POST['qname']
    except(KeyError, Questao.DoesNotExist):
        return render(request, 'votacao/createquestion.html')
    else:
        questao = Questao(questao_texto=questaotexto, pub_data=datetime.datetime.now())
        questao.save()
    return HttpResponseRedirect(reverse('votacao:index'))

@login_required(login_url='/votacao/userlogin')
def deletequestion(request, questao_id):
    if request.user.is_superuser and request.user.is_authenticated:
        questao = get_object_or_404(Questao, pk=questao_id)
        questao.delete()
    return HttpResponseRedirect(reverse('votacao:index'))

@login_required(login_url='/votacao/userlogin')
def createoption(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcaotexto = request.POST['opname']
    except(KeyError, Opcao.DoesNotExist):
        return render(request, 'votacao/createoption.html', {'questao': questao})
    else:
        opcao = Opcao(questao=questao, opcao_texto=opcaotexto, votos=0)
        opcao.save()
    return HttpResponseRedirect(reverse('votacao:detalhe', args=[questao.id]))

@login_required(login_url='/votacao/userlogin')
def deleteoption(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        return render(request, 'votacao/detalhe.html', {
            'questao': questao, 'error_message': "Não escolheu uma opção", })
    else:
        opcao_seleccionada.delete()
    return HttpResponseRedirect(reverse('votacao:detalhe', args=[questao.id]))

@login_required(login_url='/votacao/userlogin')
def fazer_upload(request):
    if request.method == 'POST' and request.FILES.get('myfile') is not None:
        myfile = request.FILES['myfile']
        aluno = get_object_or_404(Aluno, pk=request.user.aluno.id)
        aluno.imagem = myfile.name
        aluno.save()
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'votacao/fazer_upload.html', {'uploaded_file_url': uploaded_file_url})

    return render(request, 'votacao/fazer_upload.html')


