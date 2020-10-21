from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django_countries.fields import CountryField

# What happens when a user gets created, and when a superuser gets created
class MyAccountManager(BaseUserManager):
    # Make sure to include arguments if you added more items to the REQUIRED_FIELDS in the Account class.
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError('Can not register without email address.')
        if not username:
            raise ValueError('Can not register without username.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Role(models.Model):
    ADMIN = 1
    APPROVER = 2
    WRITER = 3
    EDITOR = 4
    IMPLEMENTOR = 5
    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (APPROVER, 'approver'),
        (WRITER, 'writer'),
        (EDITOR, 'editor'),
        (IMPLEMENTOR, 'implementor'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    # Required fields
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # Optional fields
    is_researcher = models.BooleanField(default=False)
    last_name = models.CharField(verbose_name='last name', max_length=60, blank=True)
    first_name = models.CharField(verbose_name='first name', max_length=60, blank=True)
    phone = models.CharField(verbose_name='phone number', max_length=20, blank=True)
    nationality = models.CharField(verbose_name='nationality', max_length=60, blank=True)
    country = CountryField()
    city_or_town = models.CharField(verbose_name='city or town', max_length=80, blank=True)
    job_title = models.CharField(verbose_name='job title', max_length=80, blank=True)
    affiliation = models.CharField(verbose_name='affiliation', max_length=60, blank=True)
    bio = models.TextField(verbose_name='bio', blank=True)
    community_member = models.BooleanField(default=False)

    # This is what the user will log in with
    USERNAME_FIELD = 'email'
    # Fields that will be required upon user registration. 
    # If adding to this, make sure to update the argument list in MyAccountManager above.
    REQUIRED_FIELDS = ['username', 'last_name', 'first_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    #Required methods for custom user ( can do things if admin )
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Community(models.Model):
    community_name = models.CharField(max_length=80)
    community_code = models.CharField(max_length=80)
    address = models.CharField(max_length=80)
    contact_name = models.CharField(max_length=80)
    contact_email = models.EmailField(max_length=254)
    country = CountryField()
    members = models.ManyToManyField(Account)

    def __str__(self):
        return self.community_name

    class Meta:
        verbose_name = 'Community'
        verbose_name_plural = 'Communities'

class Institution(models.Model):
    institution_name = models.CharField(max_length=80)
    institution_code = models.CharField(max_length=80)
    address = models.CharField(max_length=80)
    contact_name = models.CharField(max_length=80)
    contact_email = models.EmailField(max_length=254)
    country = CountryField()
    members = models.ManyToManyField(Account)

    def __str__(self):
        return self.institution_name

    class Meta:
        verbose_name = 'Institution'
        verbose_name_plural = 'Institutions'

class UserCommunity(models.Model):
    name = models.CharField(max_length=10, default='')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=None)
    communities = models.ManyToManyField(Community)
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'User Community'
        verbose_name_plural = 'User Communities'

class UserInstitution(models.Model):
    name = models.CharField(max_length=10)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=None)
    institution = models.ManyToManyField(Institution)
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User Institution'
        verbose_name_plural = 'User Institutions'

class Project(models.Model):
    who = models.TextField()
    when = models.TextField()
    where = models.TextField()
    what = models.TextField()
    abstract = models.TextField()
    target_species = models.TextField()

