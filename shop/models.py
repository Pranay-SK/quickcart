from django.db import models

from accounts.models import User,UserProfile
from accounts.utils import send_notification

# Create your models here.

class Shop(models.Model):
    user=models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    user_profile=models.OneToOneField(UserProfile,related_name='userprofile', on_delete=models.CASCADE)
    owner_name=models.CharField(max_length=50)
    shop_license=models.ImageField(upload_to='Shops/licenses')
    is_approved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner_name

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
        
                                      