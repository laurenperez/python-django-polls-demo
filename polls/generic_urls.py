from django.urls import path

from . import views

# Amended URLconf for GENERIC VIEWS

# Now we refactor to simplify:

# Generally, when writing a Django app, you’ll evaluate whether generic views
# are a good fit for your problem, and you’ll use them from the beginning, rather than
# refactoring your code.

app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # The DetailView generic view expects the primary key value captured from the URL to be
    # called "pk", so we’ve changed question_id to pk for the generic views.
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),

    path('<int:question_id>/vote/', views.vote, name='vote'),
]
