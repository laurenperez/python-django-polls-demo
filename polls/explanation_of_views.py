# These views represent a common case of basic Web development: getting data from
#  the database according to a parameter passed in the URL, loading a template and
#   returning the rendered template. Because this is so common, Django provides a shortcut,
#    called the “generic views” system. SEE GENERIC VIEWS FOR DETAILS.


from django.shortcuts import render
from django.http import HttpResponse # only needed if used below
from django.http import HttpResponseRedirect
from django.template import loader
from django.http import Http404  # replaced by get_object_or_404
from django.shortcuts import get_object_or_404
from django.urls import reverse


from .models import Choice, Question

# Create your views here.


# ***** INDEX *****

# Here’s one stab at a new index() view, which displays the latest 5 poll questions
# in the system, separated by commas, according to publication date
# we use httpResponse() to send back a response object

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)


# here we have added a template to render dynamic content
# context is a dictionary that maps template variable names to Python objects

def index(request):
    print("hey we're in {}".format(request))
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))



# ***** DETAIL *****

# Here is our first "detail" view, suing httpResponse() with a response hardcoded in

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)



# USING RENDER() AS A SHORTCUT
# here we trade the httpResponse() for a return render(1,2,3)
# the render() function takes the request object as its first argument
# a template name as its second argument and a dictionary as its optional third argument

def detail(request, question_id):   #pk stands for 'Primary Key'
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})



# It’s very common to use get() and raise Http404 if an object doesn’t exist
# Django provides a shortcut with get_object_or_404(1,...)
# this method takes a Django model as its first argument and an arbitrary number of keyword arguments

def detail(request, question_id):  #pk stands for 'Primary Key'
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})



# ***** VOTE *****

# this is the dummy view for vote with filler text

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


# POST
# request.POST is a dictionary-like object that lets you access submitted data by key name.
# request.POST values are always strings.

def vote(request, question_id):   #pk stands for 'Primary Key'
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        # request.POST['choice'] will raise KeyError if choice wasn’t provided in POST data.
    except (KeyError, Choice.DoesNotExist):
        # if they didnt select one redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        # After incrementing the choice count, the code returns an HttpResponseRedirect
        # rather than a normal HttpResponse. HttpResponseRedirect takes a single argument: the URL to which the user will be redirected
        selected_choice.save()
        # Returning an HttpResponseRedirect after successfully dealing
        # with POST data prevents data from being posted twice if a user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # reverse() - this function helps avoid having to hardcode a URL in the view function.
        # this reverse() call will return a string like '/polls/3/results/' where 3 is the value of question.id
        # Now after somebody votes on a question, the vote() view redirects to the results page for the question.



# The code for our vote() view does have a small problem. It first gets the selected_choice object
# from the database, then computes the new value of votes, and then saves it back to the database.
# If two users of your website try to vote at exactly the same time. This is called a 'race condition.''



# ***** RESULTS *****

# this is the dummy view for results with filler text

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


# with real user data from the database

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})








#end
