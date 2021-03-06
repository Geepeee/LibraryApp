from django.shortcuts import render,redirect,get_object_or_404
from catalog.models import Book,BookInstance,Author,Language,Genre
from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.forms import RenewLoanBook,UserRegister,UserProfileForm,UserProfileDetails
from django.urls import reverse_lazy
from django.contrib.auth.models import User
import datetime
from django.contrib import messages
# Create your views here.
@login_required
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

def register(request):
    if request.method == "POST":
        data = UserRegister(request.POST)
        if data.is_valid():
            data.save()
            messages.success(request,f"You account is successfully created.")
            return redirect(reverse_lazy('login'))
        else:
            ctx = {'form': data}
            return render(request,'catalog/register.html',ctx)
    else:
        userdata = UserRegister()
    ctx = {
       'form': userdata,
    }
    return render(request,'catalog/register.html',ctx)


class BookListView(ListView):
    model = Book
    context_object_name = 'booklist'
    template_name = 'catalog/list.html'

class BookDetailView(LoginRequiredMixin,DetailView):
    model = Book

    def get(sef,request,pk):
        book = Book.objects.get(id=pk)
        bookins = BookInstance.objects.filter(book=pk)
        bookcount = BookInstance.objects.filter(book=pk).count()
        bookcountAva = BookInstance.objects.filter(book=pk).filter(status__exact="a").count()
        if bookcountAva > 0:
            diffbooks = bookcountAva
            requestBook = BookInstance.objects.filter(book=pk).filter(status__exact="a").first()
            proposed_date = datetime.date.today() + datetime.timedelta(weeks=3)
            form = RenewLoanBook(initial={'renewal_date':proposed_date})
            ctx = {'book':book,'instances':bookins,'availablebooks':diffbooks,
                   'requestbook':requestBook,'form':form}
            return render(request,'catalog/detail.html',ctx)
        ctx = {'book':book,'instances':bookins}
        return render(request,'catalog/detail.html',ctx)
class AuthorListView(ListView):
    model = Author
    paginate_by = 2
    template_name = "catalog/author.html"
    def get(self,request):
        authors = Author.objects.all()
        ctx = {'authors': authors}
        return render(request,self.template_name,ctx)

class AuthorDeatailView(LoginRequiredMixin,DetailView):
    model = Author
    template_name = 'catalog/authordetail.html'
    def get(self,request,pk):
        author = Author.objects.get(id=pk)
        books = Book.objects.filter(author=author.id)
        ctx = {'author': author,'books':books}
        return render(request,self.template_name,ctx)

class LoanedBooksByUser(LoginRequiredMixin,ListView):
    model = BookInstance
    paginate_by = 8
    template_name = 'catalog/loanedBooksByUser.html'
    def get(self,request):
        loaned = BookInstance.objects.filter(borrower=self.request.user).filter(status__exact="o").order_by('-due_back')
        ctx = {'loanBooks':loaned}
        return render(request,self.template_name,ctx)

class LoanedBooksByAll(LoginRequiredMixin,ListView):
    model = BookInstance
    template_name = 'catalog/loanedBooksByUser.html'
    def get(self,request):
        loaned = BookInstance.objects.filter(status__exact="o").order_by('-due_back')
        ctx = {'loanBooks':loaned}
        return render(request,self.template_name,ctx)

@permission_required('catalog.Can_mark_retuned')
def renew_books(request,pk):

    book_instance = get_object_or_404(BookInstance,id=pk)
    if request.method == "POST":
        form = RenewLoanBook(request.POST)
        print(form)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return redirect(reverse_lazy('catalog:allloanedbooks'))
    else:
        proposed_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewLoanBook(initial={'renewal_date':proposed_date})
    ctx = {
       'book_instance':book_instance,
       'form': form
    }

    return render(request,'catalog/renewal_book.html',ctx)

class AuthorCreateView(LoginRequiredMixin,CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '12/12/9999'}
    template_name = 'catalog/author_form.html'
    success_url = reverse_lazy('catalog:authors')

class AuthorUpdateView(LoginRequiredMixin,UpdateView):
    model = Author
    fields = '__all__'
    template_name = 'catalog/author_form.html'
    success_url = reverse_lazy('catalog:authors')

class AuthorDeleteView(LoginRequiredMixin,DeleteView):
    model = Author
    success_url = reverse_lazy('catalog:authors')
    template_name = 'catalog/author_confirm_delete.html'

class BookCreateView(LoginRequiredMixin,CreateView):
    model = Book
    fields = '__all__'
    template_name = 'catalog/book_form.html'
    success_url = reverse_lazy('catalog:booklist')

class BookUpdateView(LoginRequiredMixin,UpdateView):
    model = Book
    fields = ['author','summary','genre']
    template_name = 'catalog/book_form.html'
    success_url = reverse_lazy('catalog:booklist')

class BookDeleteView(LoginRequiredMixin,DeleteView):
    model = Book
    template_name = 'catalog/book_confirm_delete.html'
    success_url = reverse_lazy('catalog:booklist')

class UserProfile(UpdateView):
    model = User
    def get(self,request,pk):
        user = UserProfileForm(instance=request.user)
        ctx = {'form':user}
        return render(request,'catalog/profile.html',ctx)
    def post(self,request,pk):
        user = get_object_or_404(User,id=pk)

class LoanBookReturn(LoginRequiredMixin,ListView):

    model = BookInstance
    template_name = 'catalog/loanedBooksByUser.html'
    def get(self,request,pk):
        book = BookInstance.objects.get(id=pk)
        book.status = 'r'
        book.save()
        loaned = BookInstance.objects.filter(borrower=self.request.user).filter(status__exact="o").order_by('-due_back')
        ctx = {'loanBooks':loaned}
        return render(request,self.template_name,ctx)

class MakeBooksAvailable(LoginRequiredMixin,ListView):

    def get(self,request,**kwargs):
        if (kwargs):
            bookstatus = BookInstance.objects.get(id=kwargs['pk'])
            if bookstatus.status == 'r':
                bookstatus.status = 'a'
                bookstatus.due_back = None
                bookstatus.borrower = None
                bookstatus.save()
            if bookstatus.status == 'R':
                bookstatus.status = 'o'
                bookstatus.due_back = datetime.date.today()+datetime.timedelta(weeks=3)
                bookstatus.save()
        loanBooks = BookInstance.objects.filter(status__exact="r").order_by('-due_back')
        requestb = BookInstance.objects.filter(status__exact="R").order_by('-due_back')
        ctx = {'loanBooks':loanBooks,
                'requestb':requestb}
        return render(request,'catalog/returnbook.html',ctx)

class RequestAdvanceBook(LoginRequiredMixin,ListView):
    model = BookInstance
    def get(self,request,pk):
        booksave = BookInstance.objects.get(id=pk)
        booksave.status = 'A'
        booksave.save()
        book = Book.objects.get(id=pk)
        bookins = BookInstance.objects.filter(book=pk)
        bookcount = BookInstance.objects.filter(book=pk).count()
        bookcountAva = BookInstance.objects.filter(book=pk).filter(status__exact="a").count()
        if bookcountAva > 0:
            diffbooks = bookcountAva
            ctx = {'book':book,'instances':bookins,'availablebooks':diffbooks}
            return render(request,'catalog/detail.html',ctx)
        ctx = {'book':book,'instances':bookins}
        return render(request,'catalog/detail.html',ctx)

class RequestBook(LoginRequiredMixin,ListView):
    model = BookInstance
    def get(self,request,pk):
        bookstatus = BookInstance.objects.get(id=pk)
        bookstatus.status = 'R'
        bookstatus.borrower = request.user
        bookstatus.save()
        return redirect(reverse_lazy('catalog:bookdetail',kwargs={'pk':bookstatus.book.id}))
