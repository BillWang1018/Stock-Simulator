# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Customer(models.Model):
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    identity = models.CharField(db_column='Identity', max_length=50)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=50)  # Field name made lowercase.
    ctfc = models.CharField(db_column='Ctfc', primary_key=True, max_length=50)  # Field name made lowercase.
    password = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'customer'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Inventory(models.Model):
    cid = models.OneToOneField(Customer, models.DO_NOTHING, db_column='Cid', primary_key=True)  # Field name made lowercase. The composite primary key (Cid, Tstmp) found, that is not supported. The first column is selected.
    snum = models.ForeignKey('Stock', models.DO_NOTHING, db_column='Snum', blank=True, null=True)  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tstmp = models.DateTimeField(db_column='Tstmp')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'inventory'
        unique_together = (('cid', 'tstmp'),)


class LoginCustomer(models.Model):
    name = models.CharField(max_length=50)
    identity = models.CharField(primary_key=True, max_length=50)
    account = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=20)
    ctfc = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'login_customer'


class LoginUserprofile(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'login_userprofile'


class MembersCustomer(models.Model):
    name = models.CharField(max_length=50)
    identity = models.CharField(primary_key=True, max_length=50)
    account = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=20)
    ctfc = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'members_customer'


class MembersUserprofile(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'members_userprofile'


class Quotations(models.Model):
    snum = models.OneToOneField('Stock', models.DO_NOTHING, db_column='Snum', primary_key=True)  # Field name made lowercase. The composite primary key (Snum, TStmp) found, that is not supported. The first column is selected.
    buyamt = models.IntegerField(db_column='BuyAmt')  # Field name made lowercase.
    sellamt = models.IntegerField(db_column='SellAmt')  # Field name made lowercase.
    tstmp = models.DateTimeField(db_column='TStmp')  # Field name made lowercase.
    sprice = models.DecimalField(db_column='Sprice', max_digits=6, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quotations'
        unique_together = (('snum', 'tstmp'),)


class Stock(models.Model):
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    number = models.IntegerField(db_column='Number', primary_key=True)  # Field name made lowercase.
    overamt = models.IntegerField(db_column='OverAmt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stock'
