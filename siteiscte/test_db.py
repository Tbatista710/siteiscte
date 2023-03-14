from votacao.models import Questao, Opcao

print("\n--------- Exercicio 4.4 ---------")

count = 0
for o in Opcao.objects.all():
    count += o.votos
print("Numero total de votos --", count)

for q in Questao.objects.all():
    options = q.opcao_set.all()
    current_max = 0
    current_option = ""
    for o in options:
        if o.votos >= current_max:
            current_max = o.votos
            current_option = o.opcao_texto
    print(q.questao_texto, current_option)

print("---------------------------------")