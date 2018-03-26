from django.urls import path

from . import views


# In production size Django projects, you'll have several 'apps'
# For example, the polls app has a detail view, and so might an app
# on the same project for say a 'blog.'
# 'namespacing' URL names is the Django convention for keeping them separate.


# add namespaces to your URLconf like so:

app_name = 'polls'

# then make sure to chage your ulr in your templates to reflect this namespacing

urlpatterns = [
    # /polls/
    path('', views.index, name='index'),
    # /polls/34
    # the 'name' value as called by the {% url %} template tag
    path('<int:question_id>/', views.detail, name='detail'),
    # /polls/34/results
    path('<int:question_id>/results/', views.results, name='results'),
    # /polls/34/vote
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
