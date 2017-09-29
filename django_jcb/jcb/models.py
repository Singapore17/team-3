from django.db import models

# Create your models here.
class Bizhong(models.Model):
	bibie=models.CharField(max_length=10)
	rate=models.DecimalField(max_digits=18,decimal_places=6)
	def __str__(self):
		return u'bibie:{0},rate:{1}'.format(self.bibie,str(self.rate))

class Cesuan_pre(models.Model):
	cust_name=models.CharField(max_length=50)
	acct_no=models.CharField(max_length=20)
	amt=models.DecimalField(max_digits=18,decimal_places=2)
	bibie=models.CharField(max_length=10)
	release_date=models.DateTimeField()
	release_limit=models.PositiveIntegerField()
	loan_rate=models.DecimalField(max_digits=18,decimal_places=6)
	FTP=models.DecimalField(max_digits=18,decimal_places=6)
	profit_rate=models.DecimalField(max_digits=18,decimal_places=6)
	risk_assets=models.DecimalField(max_digits=18,decimal_places=6)
	int_org=models.CharField(max_length=4)
	employee=models.CharField(max_length=10)

class Pro_cond(models.Model):
	acct_no=models.ForeignKey(Cesuan_pre)
	cust_name=models.CharField(max_length=10)
	deposit_acct_no=models.CharField(max_length=20)
	deposit_day_avg=models.DecimalField(max_digits=18,decimal_places=2)
	bibie=models.CharField(max_length=10)
	deposit_limit=models.PositiveIntegerField()
	deposit_rate=models.DecimalField(max_digits=18,decimal_places=6)
	FTP=models.DecimalField(max_digits=18,decimal_places=6)
	deposit_profit_rate=models.DecimalField(max_digits=18,decimal_places=6)
	int_org=models.CharField(max_length=4)
	zjywsr=models.DecimalField(max_digits=18,decimal_places=2)
	other_cond=models.CharField(max_length=200)
	index=models.PositiveIntegerField()
	