#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime  


class Profile(models.Model):
	user = models.OneToOneField(User)

	def __str__(self):
		return "%s" % (self.user)



class Account(models.Model):
	url = models.CharField(max_length=100)
	social= (('Twitter', 'Twitter'),('Instagram', 'Instagram'))
	socialaccount = models.CharField(max_length=15, choices=social,null=True)

	def __str__(self):
		return "%s" % (self.url)

class Post(models.Model):
	likes = models.IntegerField(blank=True,null=True)
	likesraiting = models.IntegerField(blank=True,null=True)
	owner = models.ForeignKey('Account')
	date = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		return "%s" % (self.owner)

	