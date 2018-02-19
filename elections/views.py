from django.shortcuts import render
from django.http import HttpResponse

from .models import Candidate

'''
def index(request):
    candidates = Candidate.objects.all()
    str = "" #마지막에 리턴해줄 문자열
    for candidate in candidates:
        str += "{name}기호 {num}번 ({area})<BR>".format(name=candidate.name, num=candidate.party_number, area=candidate.area)
        str += candidate.introduction + "<P>"
    return HttpResponse(str)
'''
def index(request):
    candidates = Candidate.objects.all()
    return render(request, 'elections/index.html', {'candidates':candidates})
