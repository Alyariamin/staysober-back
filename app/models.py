from datetime import timedelta
import json
from django.conf import settings
from django.db import models
from django.utils import timezone

class Profile(models.Model):
    start_date = models.DateTimeField(null=True, blank=True,default=timezone.now)
    saved_money = models.DecimalField(max_digits=6, decimal_places=2,default=0.00)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Journal(models.Model):
    MOOD_GREAT = 'Great'
    MOOD_GOOD = 'Good'
    MOOD_NEUTRAL = 'Neutral'
    MOOD_DIFFICULT = 'Difficult'
    MOOD_STRUGGLING = 'Struggling'

    MOOD_CHOICES = [
    (MOOD_GREAT , 'Great'),
    (MOOD_GOOD , 'Good'),
    (MOOD_NEUTRAL , 'Neutral'),
    (MOOD_DIFFICULT , 'Difficult'),
    (MOOD_STRUGGLING , 'Struggling')
    ]
    content = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='journals')
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES, default='Neutral')
    date = models.DateTimeField(auto_now_add=True)
    triggers = models.CharField(max_length=255, null=True, blank=True)

class Goal(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    target_date = models.DateField(blank=True,null=True)
    completed = models.BooleanField(blank=True,null=True)
    created_at = models.DateField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
class Habit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    @property
    def streak(self):
        completions = list(self.completions.filter(completed=True)
                         .order_by('-date')
                         .values_list('date', flat=True))
        if not completions:
            return 0
        today = timezone.now().date()
        streak = 0
        if completions[0] == today:
            streak = 1
            completions = completions[1:]
        else:
            return 0
        expected_date = today - timedelta(days=1)        
        for completion_date in completions:
            if completion_date == expected_date:
                streak += 1
                expected_date -= timedelta(days=1)
            else:
                break
        return streak
class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='completions')
    date = models.DateField()
    completed = models.BooleanField(default=True)
    class Meta:
        unique_together = ('habit', 'date')

class Mood(models.Model):
    mood = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    activities = models.JSONField(blank=True, null=True)
    energy = models.IntegerField()
    sleep = models.IntegerField()
    date = models.DateTimeField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    def get_activities_list(self):
        """Helper method to return activities as a list if stored as JSON array"""
        if self.activities:
            try:
                if isinstance(self.activities, str):
                    return json.loads(self.activities)
                return self.activities
            except json.JSONDecodeError:
                return []
        return []
    
class Craving(models.Model):
    date = models.DateTimeField(blank=True,null=True)
    intensity = models.IntegerField()
    trigger = models.CharField(max_length=255,blank=True,null=True)
    location = models.CharField(max_length=255)
    coping_strategy = models.CharField(max_length=255,blank=True,null=True)
    notes = models.TextField(blank=True,null=True)
    duration = models.IntegerField()
    overcome = models.BooleanField()
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)

