from django.db import models
from datetime import date, datetime,time

from accounts.models import User,UserProfile
from accounts.utils import send_notification

# Create your models here.

class Shop(models.Model):
    user=models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    user_profile=models.OneToOneField(UserProfile,related_name='userprofile', on_delete=models.CASCADE)
    owner_name=models.CharField(max_length=50)
    shop_slug=models.SlugField(max_length=100,unique=True)
    shop_license=models.ImageField(upload_to='Shops/licenses')
    is_approved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner_name

    def is_open(self):
        #check current day's opening hours.
        today_date=date.today()
        today=today_date.isoweekday()
        currnt_opening_hours=OpeningHour.objects.filter(shop=self,day=today)
        now=datetime.now()
        current_time=now.strftime("%H:%M:%S")

        is_open = False
        now_time = datetime.now().time()
        for i in currnt_opening_hours:
            if not i.from_hour or not i.to_hour or i.is_closed:
                continue
            start = datetime.strptime(i.from_hour, "%I:%M %p").time()
            end = datetime.strptime(i.to_hour, "%I:%M %p").time()
            if start <= now_time < end:
                is_open = True
                break
        return is_open






    def save(self, *args,**kwargs):
        if self.pk is not None:
             #update
             orig=Shop.objects.get(pk=self.pk)
             if orig.is_approved !=self.is_approved:
                 mail_template='accounts/emails/admin_approval_email.html'
                 context={
                     'user':self.user,
                     'is_approved':self.is_approved,
                 }


                 if self.is_approved==True:
                     # send notification email
                     mail_subject="Congrutulations! Your Shop has been approved."
                     send_notification(mail_subject,mail_template, context)
                     
                 else:
                     # send notification email
                     mail_subject="Sorry! Your Shop has not been approved."
                     send_notification(mail_subject, mail_template, context)
        return super(Shop,self).save(*args,**kwargs)            
        

DAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
]

HOUR_OF_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]
class OpeningHour(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-from_hour')
        unique_together = ('shop', 'day', 'from_hour', 'to_hour')

    def __str__(self):
        return self.get_day_display()
