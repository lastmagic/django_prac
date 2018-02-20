from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Sum
from .models import Candidate, Poll, Choice
import datetime

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
    context = {'candidates':candidates}
    return render(request, 'elections/index.html', context)

def areas(request, area):
    today = datetime.datetime.now()
    try:
        poll = Poll.objects.get(area=area, start_date__lte = today, end_date__gte=today)
        candidates = Candidate.objects.filter(area = area)
    except:
        poll = None
        candidates = None
    context = {'candidates': candidates, 'area':area, 'poll':poll}
    return render(request, 'elections/area.html', context)


def polls(request, poll_id):
    poll = Poll.objects.get(pk = poll_id)
    selection = request.POST['choice']

    try:
        choice = Choice.objects.get(poll_id = poll.id, candidate_id = selection)
        choice.votes += 1
        choice.save()
    except:
        #최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성합니다
        choice = Choice(poll_id = poll.id, candidate_id = selection, votes = 1)
        choice.save()

    #return HttpResponse("Finish, now votes = {votes}".format(votes=choice.votes))
    return HttpResponseRedirect("/areas/{area}/results".format(area=poll.area))


def results(request, area):
    candidates = Candidate.objects.filter(area=area)
    polls = Poll.objects.filter(area = area)
    poll_results = []
    for poll in polls:
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date

        #poll.id에 해당하는 전체 투표수 알아오기
        total_votes = Choice.objects.filter(poll_id=poll.id).aggregate(Sum('votes'))
        result['total_votes'] = total_votes['votes__sum']

        rates = [] #지지율
        for candidate in candidates:
            try:
                choice = Choice.objects.get(poll=poll, candidate_id=candidate.id)
                rates.append(round(choice.votes *100 / result['total_votes'], 1))
            except:
                rates.append(0)
        result['rates'] =rates
        poll_results.append(result)

    context = {'candidates':candidates, 'area':area, 'poll_results':poll_results}
    return render(request, 'elections/result.html', context)
