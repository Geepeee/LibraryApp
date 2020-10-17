from django.shortcuts import render
from catalog.models import Book,BookInstance,Author,Language,Genre
from django.views.generic import ListView,DetailView
from django.db.models import Sum
# Create your views here.

def index(request):
    """View function for home page, showing the overview of the library."""
    num_books = Book.objects.all().count()
    num_book_insta = BookInstance.objects.all().count()
    num_insta_available = BookInstance.objects.filter(status__exact="a").count()
    num_authors = Author.objects.all().count()

    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1

    ctx = {
       'totalBooks': num_books,
       'totalBookIns': num_book_insta,
       'totalBookAva': num_insta_available,
       'totalAuthor': num_authors,
       'num_visits': num_visits,
    }

    return render(request,'catalog/index.html',ctx)

class BookListView(ListView):
    model = Book
    context_object_name = 'booklist'
    template_name = 'catalog/list.html'

class BookDetailView(DetailView):
    model = Book

    def get(sef,request,pk):

        book = Book.objects.get(id=pk)
        bookins = BookInstance.objects.filter(book=pk)
        ctx = {'book':book,'instances':bookins}
        return render(request,'catalog/detail.html',ctx)
class AuthorListView(ListView):
    model = Author
    template_name = "catalog/author.html"
    def get(self,request):
        authors = Author.objects.all()
        ctx = {'authors': authors}
        return render(request,self.template_name,ctx)

class AuthorDeatailView(DetailView):
    model = Author
    template_name = 'catalog/authordetail.html'
    def get(self,request,pk):
        author = Author.objects.get(id=pk)
        books = Book.objects.filter(author=author.id)
        ctx = {'author': author,'books':books}
        return render(request,self.template_name,ctx)
