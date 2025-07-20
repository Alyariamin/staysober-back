from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('profiles',views.ProfileViewSet)
router.register('journals',views.JournalViewSet,basename='journals')
router.register('goals',views.GoalViewSet,basename='goals')
router.register('habits',views.HabitViewSet,basename='habits')
router.register('moods',views.MoodViewSet,basename='moods')
router.register('cravings',views.CravingViewSet,basename='cravings')

urlpatterns = router.urls
