from django.db import models

from django.db.models import Avg
from django.contrib.auth.models import User

class Book(models.Model):
	title = models.CharField(max_length=200)
	author = models.CharField(max_length=200,default='author')
	publication = models.CharField(max_length=200,default='pub')
	category = models.CharField(max_length=1000,default='category')
	def average_rating(self):
		return self.review_set.aggregate(Avg('rating'))['rating__avg']

	
	def __str__(self):
		return self.title
	



class Review(models.Model):
	RATING_CHOICES = (
		(1, '1'),
		(2, '2'),
		(3, '3'),
		(4, '4'),
		(5, '5'),
	)
	
	book = models.ForeignKey('book', on_delete=models.DO_NOTHING)
	user_id = models.ForeignKey(User, default=None, null=True,blank=True, on_delete=models.CASCADE)
	comment = models.CharField(max_length = 200, default='default comment')
	rating = models.FloatField(choices=RATING_CHOICES,default=None, null=True, blank=True)
	user_name = models.CharField(max_length = 200, default = 'user')


