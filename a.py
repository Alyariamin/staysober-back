from datetime import timedelta
from django.utils import timezone
today= timezone.now().date()
print(today - timedelta(days=1))
