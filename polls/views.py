from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

# serialization
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import QuestionSerializer

from .models import Question, Choice

# serialization
@api_view(['GET'])
def get_questions(request):
    """
    Get list of questions on the site
    """

    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def update_question(request, pk):
    """
    Get the list of questions on website
    """

    questions = Question.objects.get(id=pk)
    serializer = QuestionSerializer(questions, data=request.data, partial=True)
    if serializer.is_valid():
        
        # was not working in serializer class so moved here, works now
        serializer.save()
        return Response(serializer.data)
    return Response(status=400, data=serializer.errors)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ Return last five published questions """
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        
        # redisplay question voting form
        return render(request, 'polls/detail.html', { 
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        # return HttpResponseRedirect when successful POST
        # prevents reinput of data if Back button hit
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    

# view methods before refactoring

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})