# *** USING GENERIC VIEWS ***
# we can use generic views to simplify our code.
# this is very similar to using 'partials' in EJS/Javascript


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


# We’re using two generic views here: ListView and DetailView.
# We call them 'ResultsView' and 'DetailView.'
# Respectively, those two views abstract the concepts of
# “display a list of objects” and “display a detail page for a particular type of object.”



class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        #Return the last five published questions.
        return Question.objects.order_by('-pub_date')[:5]


# For DetailView the question variable is provided automatically – since we’re
# using a Django model (Question), Django is able to determine an appropriate name
# for the context variable. However, for ListView, the automatically generated context
# variable is question_list. To override this we provide the context_object_name
# attribute, specifying that we want to use latest_question_list instead. As an
# alternative approach, you could change your templates to match the new default
# context variables – but it’s a lot easier to just tell Django to use the variable you want.


class DetailView(generic.DetailView):
    # Each generic view needs to know what model it will be acting upon.
    # This is provided using the model attribute.
    model = Question
    template_name = 'polls/detail.html'

# By default, the 'DetailView' generic view uses a template called <app name>/<model name>_detail.html.
# In our case, it would use the template "polls/question_detail.html". The template_name attribute is
# used to tell Django to use a specific template name instead of the autogenerated default template name.
# We also specify the template_name for the results list view – this ensures that the results view and
# the detail view have a different appearance when rendered, even though they’re both a DetailView behind the scenes.


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# Similarly, the 'ListView' generic view uses a default template called <app name>/<model name>_list.html;
# we use template_name to tell ListView to use our existing "polls/index.html" template.


def vote(request, question_id):   #pk stands for 'Primary Key'
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))








# end
