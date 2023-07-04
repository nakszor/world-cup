from django.urls import path
from .views import TeamView
from .views import TeamDetailView


urlpatterns = [
    path('teams/', TeamView.as_view()),
    path('teams/<int:team_id>/', TeamDetailView.as_view())
]