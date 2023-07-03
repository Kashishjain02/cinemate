from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
# Create your models here.


class MyAccountManager(BaseUserManager):
    # create_user deals with creating the user of costumer type
    def create_user(self, email, name, viewpass=None, password=None, ):
        if not email:
            raise ValueError("enter email")
        if not name:
            raise ValueError("enter first name")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            viewpass=viewpass,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_vendor(self, shop_number, shop_name, shop_add, plan, gst, vendor, subscripton_amount):

    #     user = self.model(
    #         shop_number=shop_number,
    #         shop_name=shop_name,
    #         shop_add=shop_add,
    #         plan=plan,
    #         gst=gst,
    #         vendor=vendor,
    #         subscripton_amount=subscripton_amount,
    #     )
    #     user.save(using=self._db)
    #     return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            # viewpass=viewpass,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    viewpass = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    about = models.TextField(default="about")
    image = models.ImageField(upload_to= 'account/', null=True, blank=True, default='account/default.png')
    is_superuser = models.BooleanField(default=False)
    is_freelancer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    objects = MyAccountManager()

    def save(self, *args, **kwargs):
        # Custom save logic or modifications before saving
        print("username is ",self.username)
        if self.username == None:
            self.username = self.name.replace(" ", "")  + str(self.pk)
            print("username 77 ",self.username)
        if self.username == '':
            self.username = self.name.replace(" ", "")  + str(self.pk)
            print("username 80 ",self.username)
        elif self !=Account.objects.get(username=self.username):
                raise ValueError("username already exists")
        
        super().save(*args, **kwargs)  # Call the parent class's save() method

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return self.is_admin




class Freelancer(models.Model):
    freelancer = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True, )
    email = models.EmailField(verbose_name="email", max_length=100)
    # about = models.TextField(default="about")
    # username = models.CharField(max_length=100, unique=True)
    earning=models.IntegerField(default=0)
    expertise=models.CharField(max_length=50, default="videographer")
    rank=models.IntegerField(null=True,blank=True)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # objects= MyAccountManager()
    def __str__(self):
        return self.email


# only has permission to make changes or view anything in django administration can change it to staff later
#     def has_perm(self, perm,obj=None):
#         return self.is_admin
#
#     def has_module_perms(self, app_label):
#         return True
class Portfolio(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='previous_portfolio')
    image = models.ImageField(upload_to='portfolio/', null=True, blank=True)
    link = models.CharField(max_length=100, default="link")
    forclient= models.CharField(max_length=150, default="client")
    role = models.CharField(max_length=50, default="videographer")
    partnership = models.JSONField(default=[],null=True,blank=True)
    review = models.TextField(default="description")
    likes = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today)
    is_image = models.BooleanField(default=True)

    def __str__(self):
        return self.role


class Client(models.Model):
    # Blogger_id = models.AutoField(primary_key=True)
    client = models.OneToOneField(Account, default=None, on_delete=models.CASCADE, primary_key=True, )
    email = models.EmailField(verbose_name="email", max_length=100)
    company = models.CharField(max_length=50, null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email



class Order(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='previous_orders')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='previous_orders')
    amount = models.IntegerField()
    task=models.CharField(max_length=200, default='videographer')
    completion_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50, default='pending')
    payment_status = models.BooleanField(default=False)
    role=models.CharField(max_length=50, default='videographer')
    deadline=models.DateField()

class UpcomingOrder(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='pending_orders')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='pending_orders')
    amount = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
    task=models.CharField(max_length=200, default='videographer')
    deadline=models.DateField()
    role=models.CharField(max_length=50, default='videographer')


class AvailableProjects(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='available_orders')
    amount = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    task=models.CharField(max_length=200, default='videographer')
    description=models.TextField(null=True,blank=True)
    deadline=models.DateField()
    start_date=models.DateField()
    role=models.CharField(max_length=50, default='videographer')
    applicants=models.JSONField(default=[],null=True,blank=True)


class Invoice(models.Model):
    customer_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)