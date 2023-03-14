from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Questao


def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    template = loader.get_template('votacao/index.html')
    context = {
    'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def detalhe(request, questao_id):
    return HttpResponse("Esta e a questao %s." %questao_id)


def resultados(request, questao_id):
    response = "Estes sao os resultados da questao %s."
    return HttpResponse(response % questao_id)


def voto(request, questao_id):
    return HttpResponse("Votacao na questao %s." %questao_id)