from django.test import TestCase
from django.urls import reverse
from catalog.models import (Author,BookInstance,Genre,
                            Book,Language)
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
import uuid

class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        num_of_authors = 13
        for author_id in range(num_of_authors):
            Author.objects.create(first_name=f'Christain {author_id}',
                                  last_name=f'Bale {author_id}',)

    def test_view_url_exists_at_desire_loc(self):
        response=self.client.get('/catalog/books/authors/')
        self.assertEqual(response.status_code,200)

    def test_view_url_accessable_by_name(self):
        response = self.client.get(reverse('catalog:authors'))
        self.assertEqual(response.status_code,200)

    def test_view_usinf_crt_template(self):
        response = self.client.get(reverse('catalog:authors'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'catalog/author.html')

    def test_view_crct_paginate_by(self):
        response = self.client.get(reverse('catalog:authors'))
        self.assertEqual(response.status_code,200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated']==True)
        self.assertTrue(len(response.context['author_list'])==2)


class LoanedBookByUserModelTest(TestCase):


    def setUp(self):
        test_user1 = User.objects.create_user(username="testuser1",password="Python@1996")
        test_user2 = User.objects.create_user(username="testuser2",password="HelloWorld@2018")

        test_user1.save()
        test_user2.save()

        #Book Dummy
        test_author = Author.objects.create(first_name="John",last_name="Reese")
        test_genre = Genre.objects.create(name="Fantasy")
        test_language = Language.objects.create(name="English")
        test_book = Book.objects.create(title="The Alchemist",
                                        summary="This book Summary",
                                        isbn = 'ABCNDEF',
                                        author = test_author,
                                        language = test_language)
        genre_objects_for_books = Genre.objects.all()
        test_book.genre.set(genre_objects_for_books)
        test_book.save()

        num_of_books = 30
        for book_copy in range(num_of_books):
            return_date = timezone.localtime()+datetime.timedelta(days=book_copy%5)
            the_borrower = test_user1 if book_copy %2 else test_user2
            status = 'm'
            BookInstance.objects.create(book=test_book,
                                        imprint="Dont lnow",
                                        due_back = return_date,
                                        borrower = the_borrower,
                                        status = status,)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("catalog:loanedbooks"))
        self.assertRedirect(response,'/accounts/login/?next=/catalog/loanedbooks/')

    def test_logged_uses_crt_templates(self):
        login = self.client.login(username="testuser1", password="Python@1996")
        response = self.client.get(reverse('catalog:loanedbooks'))
        self.assertEqual(str(response.context['user']),'testuser1')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'catalog/loanedBooksByUser.html')

    def test_only_borrowed_list(self):
        login = self.client.login(username="testuser1",password="Python@1996")
        response = self.client.get(reverse('catalog:loanedbooks'))
        self.assertEqual(str(response.context['user']),'testuser1')
        self.assertEqual(response.status_code,200)
        self.assertTrue('loanBooks' in response.context)
        self.assertEqual(len(response.context['loanBooks']),0)

        books = BookInstance.objects.all()[:10]
        for book in books:
            book.status = 'o'
            book.save()

        response = self.client.get(reverse('catalog:loanedbooks'))
        self.assertEqual(str(response.context['user']),'testuser1')
        self.assertEqual(response.status_code,200)
        self.assertTrue('loanBooks' in response.context)

        for bookitem in response.context['loanBooks']:
            self.assertEqual(response.context['user'],bookitem.borrower)
            self.assertEqual('o',bookitem.status)

    def test_pages_by_ordered_due_date(self):

        for book in BookInstance.objects.all():
            book.status = 'o'
            book.save()

        login = self.client.login(username="testuser1",password="Python@1996")
        response = self.client.get(reverse('catalog:loanedbooks'))

        self.assertEqual(str(response.context['user']),'testuser1')
        self.assertEqual(response.status_code,200)

        last_date = 0
        for book in response.context['loanBooks']:
            if last_date == 0:
                last_date = book.due_back
            else:
                self.assertTrue(last_date<=book.due_back)
                last_date = book.due_back

class RenewalBookInstanceViewTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create(username="Rakesh",password="Python@1996")
        test_user2 = User.objects.create(username="Prathap",password="Cloths@1012")
        test_user1.is_super = True
        test_user1.save()
        test_user2.save()

        test_author=Author.objects.create(first_name="Harlod",last_name="Finch")
        test_genre = Genre.objects.create(name="Fiction")
        test_language = Language.objects.create(name='Hindi')
        test_book = Book.objects.create(title="Title only",
                                        author=test_author,
                                        summary='Good book',
                                        isbn="ABCHRF",
                                        language=test_language,)
        genre_objects = Genre.objects.all()
        test_book.genre.set(genre_objects)
        test_book.save()

        return_date = datetime.date.today()+datetime.timedelta(days=5)
        self.test_bookInstance1 = BookInstance.objects.create(book=test_book,
                                       imprint='Unimport,2020',
                                       due_back=return_date,
                                       borrower=test_user1,
                                       status='o',)
        self.test_bookInstance2 = BookInstance.objects.create(book=test_book,
                                       imprint='Unimport,2020',
                                       due_back=return_date,
                                       borrower=test_user2,
                                       status='o',)

    def test_redirect_if_not_loggedIn(self):
        response = self.client.get(reverse('catalog:renew_book_librarian',
                                           kwargs={'pk':self.test_bookInstance1.pk}))
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in_no_permission(self):
        login = self.client.login(username="Prathap",password="Cloths@1012")
        response = self.client.get(reverse('catalog:renew_book_librarian',
                                           kwargs={'pk':self.test_bookInstance1.pk}))
        self.assertEqual(response.status_code,403)

    def test_logged_in_with_permission(self):
        login = self.client.login(username="Rakesh",password="Python@1996")
        response = self.client.get(reverse('catalog:renew_book_librarian',
                                           kwargs={'pk':self.test_bookInstance1.pk}))
        self.assertEqual(response.status_code,200)
    def test_toView_other_borrwed_book(self):
        login = self.client.login(username="Rakesh",password="Python@1996")
        response = self.client.get(reverse('catalog:renew_book_librarian',
                                           kwargs={'pk':self.test_bookInstance1.pk}))
        self.assertEqual(response.status_code,200)

    def test_for_noBookInstance5(self):
        test_uuid = uuid.uuid4()
        login = self.client.login(username="Rakesh",password="Python@1996")
        response = self.client.get(reverse('catalog:renew_book_librarian',
                                           kwargs={'pk':test_uuid}))
        self.assertEqual(response.status_code,404)

    def test_uses_crct_template(self):
        login = self.client.login(username="Rakesh",password="Python@1996")
        response = self.client.get(reverse('catalog:renew_book_librarian',
                                           kwargs={'pk':self.test_bookInstance1.pk}))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(respone,"catalog/loanedBooksByUser.html")

    def test_inital_renewal_date_shown_in_view(self):
        login = self.client.login(username="Rakesh",password="Python@1996")
        response = self.client.get(reverse('catalog:renew_book_librarian',
                                           kwargs={'pk':self.test_bookInstance1.pk}))
        self.assertEqual(response.status_code,200)
        date_3_week_future=datetime.date.today()+datetime.timedelta(weeks=3)
        self.assertEqual(response.context['renewal_date'],date_3_week_future)

    def test_redirects_all_borrowed_books(self):
        login = self.client.login(username="Rakesh",password="Python@1996")
        valid_future_date = datetime.date.today()+datetime.timedelta(weeks=2)
        response = self.client.post(reverse('catalog:renew_book_librarian',kwargs={'pk':
                                            self.test_bookInstance1.pk}))
        self.assertRedirect(response,reverse('catalog:allloanedbooks'))

    def test_form_invalid_renewal_date(self):
        login = self.client.login(username="Rakesh",password="Python@1996")
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=2)
        response = self.client.post(reverse('catalog:renew_book_librarian',
                kwargs={'pk':self.test_bookInstance1.pk}),{'renewal_date':date_in_past})
        self.assertEqual(response.status_code,200)
        self.assertFormError(response,'form','renewal_date','Renewal date is in Past.')

    def test_form_renewal_date_future(self):
        login = self.client.login(username="Rakesh",password="Python@1996")
        date_in_past = datetime.date.today() + datetime.timedelta(weeks=5)
        response = self.client.post(reverse('catalog:renew_book_librarian',
                kwargs={'pk':self.test_bookInstance1.pk}),{'renewal_date':date_in_past})
        self.assertEqual(response.status_code,200)
        self.assertFormError(response,'form','renewal_date',
                   'Invalid date - as date is more than 4 weeeks ahead.')
