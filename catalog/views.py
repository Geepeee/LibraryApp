from django.shortcuts import render
from catalog.models import Book,BookInstance,Author,Language,Genre
# Create your views here.

def index(request):
    """View function for home page, showing the overview of the library."""
    num_books = Book.objects.all().count()
    num_book_insta = BookInstance.objects.all().count()
    num_insta_available = BookInstance.objects.filter(status__exact="a").count()
    num_authors = Author.objects.all().count()

    ctx = {
       'totalBooks': num_books,
       'totalBookIns': num_book_insta,
       'totalBookAva': num_insta_available,
       'totalAuthor': num_authors,
    }

    return render(request,'catalog/index.html',ctx)
