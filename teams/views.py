from django.shortcuts import render

from django.forms.models import model_to_dict
from rest_framework.views import APIView, Request, Response, status
from teams.models import Team
from .utils import data_processing
from .exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError


class TeamView(APIView):
    def get(self, request) -> Response:
       teams = Team.objects.all()

       teams_list = []
       #teams_list = [model_to_dict(team) for team in teams] 
       for team in teams:
           team_dict = model_to_dict(team)
           teams_list.append(team_dict)

       return Response(teams_list, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            data_processing(request.data)

        except NegativeTitlesError:
            return Response({"error": "titles cannot be negative"}, status.HTTP_400_BAD_REQUEST)
        
        except ImpossibleTitlesError:
            return Response({"error": "impossible to have more titles than disputed cups"}, status.HTTP_400_BAD_REQUEST)
        
        except InvalidYearCupError:
            return Response( {"error": "there was no world cup this year"}, status.HTTP_400_BAD_REQUEST)
        
        team = Team.objects.create(**request.data)
        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_201_CREATED)

class TeamDetailView(APIView):
    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        
        team_dict = model_to_dict(team)
        return Response(team_dict)
    
    def patch(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        
        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()

        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)
    
    def delete(self, request: Request, team_id: int) -> Response:

        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        
        team.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)