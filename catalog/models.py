from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date
# Create your models here.


class Genre(models.Model):
    """table for represting the genre of the book"""

    name = models.CharField(max_length=200, help_text="Enter a book genre (eg: Science Fiction)")

    def __str__(self):

        """for representation of the model"""
        return self.name

class Book(models.Model):
    """table for book representation"""

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,help_text="13 character unique number")
    genre = models.ManyToManyField(Genre, help_text="Select the genre of the book")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "Genre"

    def get_count(self):
        return BookInstance.objects.filter(book=self.id).count()

    def __str__(self):
        """for representation of the table"""
        return self.title

class BookInstance(models.Model):
    """table for book-instance representation"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID of the book")
    book = models.ForeignKey('Book',on_delete=models.CASCADE, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (('m','Maintenance'),('o','On Loan'),('a','Available'),('r', 'Received'))
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True,default='m', help_text="Book Availability")
    borrower = models.ForeignKey(User,on_delete=models.SET_NULL, null=True,blank=True)

    class Meta:
        ordering = ['due_back']
        permissions = (('Can_mark_retuned','Set book as returned'),)

    @property
    def is_overdure(self):
        if self.due_back and date.today() > self.due_back:
            return True
        else:
            return False
    def __str__(self):
        """for representation of the model"""
        return f"{self.id} {self.book.title}"

class Author(models.Model):
    """table for author representation"""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died',null=True, blank=True)

    class Meta:
        ordering = ['last_name','first_name']
    def __str__(self):
        """for representation of the model"""
        return f"{self.first_name}-{self.last_name}"

class Language(models.Model):
    """table for Language representation"""

    name = models.CharField(max_length=50, help_text="Language (eg: English, German)")

    def __str__(self):
        """for representation of the model"""
        return self.name

class PhoneNumber(models.Model):

    userdetails = models.OneToOneField(User, on_delete=models.CASCADE,null=False)
    contact = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.userdetails.username}'s contact is {self.contact}"
