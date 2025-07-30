from app.models import Craving, Goal, Habit, HabitCompletion, Journal, Mood, Profile
from app.serializers import  CravingSerializer, GoalSerializer, HabitCreateSerializer, HabitSerializer, HabitToggleSerializer, JournalSerializer, MoodSerializer, ProfileSerializer, UpdateGoalSerializer, UpdateJournalSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin,UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import date
 

class ProfileViewSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin,
                      GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    @action(detail=False, methods=['GET', 'PUT','PATCH'])
    def me(self, request):
        profile = Profile.objects.get(user_id = request.user.id)
        if request.method == "GET":
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        elif request.method == "PUT" or request.method=="PATCH":
            serializer = ProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class JournalViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    serializer_class = JournalSerializer
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
    def get_queryset(self):
        user = self.request.user
        profile_id = Profile.objects.only('id').get(user_id=user.id)
        return Journal.objects.filter(profile_id=profile_id)

class GoalViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post','patch', 'delete', 'head', 'options']
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdateGoalSerializer
        return GoalSerializer        
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Goal.objects.all()  
        profile_id = Profile.objects.only('id').get(user_id=user.id)
        return Goal.objects.filter(profile_id=profile_id)
    

class HabitViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return HabitCreateSerializer
        return HabitSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Habit.objects.all()  
        profile_id = Profile.objects.only('id').get(user_id=user.id)
        return Habit.objects.filter(profile_id=profile_id)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile= Profile.objects.get(user_id=self.request.user.id)
        habit = serializer.save(profile=profile)
        
        response_serializer = HabitSerializer(habit, context=self.get_serializer_context())
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )       
    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        habit = self.get_object()
        serializer = HabitToggleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        completion_date = serializer.validated_data['date']
        
        completion, created = HabitCompletion.objects.get_or_create(
            habit=habit,
            date=completion_date,
            defaults={'completed': True}
        )
        
        if not created:
            completion.completed = not completion.completed
            completion.save()
        
        return Response({
            'completed': completion.completed,
            'streak': habit.streak
        })    
    @action(detail=True, methods=['get'])
    def completed(self, request, pk=None):
        habit = self.get_object()
        date_param = request.query_params.get('date')
        
        if not date_param:
            return Response(
                {'error': 'Date parameter is required'},
                status=status.HTTP_400_BAD_REQUEST 
            )
        
        try:
            from django.utils.dateparse import parse_date
            completion_date = parse_date(date_param)
            if completion_date is None:
                raise ValueError
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            completion = HabitCompletion.objects.get(
                habit=habit,
                date=completion_date
            )
            return Response({'completed': completion.completed})
        except HabitCompletion.DoesNotExist:
            return Response({'completed': False})    
    @action(detail=True, methods=['get'])
    def completions(self, request, pk=None):
        habit = self.get_object()
        completions = HabitCompletion.objects.filter(
            habit=habit,
            completed=True
        ).values_list('date', flat=True)
        
        response_data = {str(date): True for date in completions}
        return Response(response_data)

class MoodViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=MoodSerializer
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
    def get_queryset(self):
        user = self.request.user
        profile_id = Profile.objects.only('id').get(user_id=user.id)
        return Mood.objects.filter(profile_id=profile_id)
    
class CravingViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=CravingSerializer
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
    def get_queryset(self):
        user = self.request.user        
        profile_id = Profile.objects.only('id').get(user_id=user.id)
        return Craving.objects.filter(profile_id=profile_id)

