from rest_framework import serializers
from app.models import Craving, Goal, Habit, HabitCompletion, Journal, Mood, Profile
from django.db import transaction
from django.utils.timezone import localdate

class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)    
    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'start_date', 'saved_money']
        read_only_fields = ['id', 'user_id'] 



class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ['id', 'content', 'mood', 'triggers' , 'date']
    def create(self, validated_data):
        profile = Profile.objects.get(user_id=self.context['user_id'])
        return Journal.objects.create(profile=profile, **validated_data)

class UpdateJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ['content','mood','triggers','date']

class GoalSerializer(serializers.ModelSerializer):
    targetDate = serializers.DateField(source='target_date',required=False,allow_null=True)
    createdAt = serializers.DateField(source='created_at',required=False)
    class Meta:
        model = Goal
        fields = ['id','title', 'description', 'targetDate', 'completed','createdAt']
    def create(self, validated_data):
        profile = Profile.objects.get(user_id=self.context['user_id'])
        return Goal.objects.create(profile=profile, **validated_data)
    def get_createdAt(self, obj):
        return obj.created_at.isoformat()

class UpdateGoalSerializer(serializers.ModelSerializer):
    targetDate = serializers.DateField(source='target_date')
    createdAt = serializers.DateField(source='created_at')

    class Meta:
        model = Goal
        fields =['id', 'title', 'description', 'targetDate', 'completed','createdAt']
        read_only_fields = ['id', 'title', 'description', 'targetDate','createdAt']
class HabitSerializer(serializers.ModelSerializer):
    streak = serializers.SerializerMethodField()
    createdAt = serializers.DateField(source='created_at')

    class Meta:
        model = Habit
        fields = ['id', 'name', 'description', 'icon', 'color', 'streak', 'createdAt']
    
    def get_streak(self, obj):
        return obj.streak
    
    def get_createdAt(self, obj):
        return obj.created_at.isoformat()

class HabitCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitCompletion
        fields = ['date', 'completed']

class HabitToggleSerializer(serializers.Serializer):
    date = serializers.DateField()
    
    def to_internal_value(self, data):
        if 'date' in data and isinstance(data['date'], str):
            try:
                from datetime import datetime
                parsed = datetime.fromisoformat(data['date'])
                data['date'] = localdate(parsed)
            except ValueError:
                pass   
        return super().to_internal_value(data)    
class HabitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id','name','description','icon','color']    
        def create(self, validated_data):
            profile = Profile.objects.get(user_id=self.context['user_id'])
            return Habit.objects.create(profile=profile, **validated_data)

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ['id','mood', 'notes', 'activities', 'energy' ,'sleep','date']
    def create(self, validated_data):
        profile = Profile.objects.get(user_id=self.context['user_id'])
        return Mood.objects.create(profile=profile, **validated_data)
class CravingSerializer(serializers.ModelSerializer):
    copingStrategy = serializers.CharField(source = 'coping_strategy',allow_blank=True)
    class Meta:
        model = Craving
        fields = ['id','intensity', 'trigger', 'date', 'location' 
                  ,'copingStrategy','notes','duration','overcome']
    def create(self, validated_data):
        profile = Profile.objects.get(user_id=self.context['user_id'])
        return Craving.objects.create(profile=profile, **validated_data)
