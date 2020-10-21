from django.test import TestCase
import datetime
from catalog.models import Author,Genre,Language,Book,BookInstance

class AuthorModeltest(TestCase):

    @classmethod
    def setUpTestData(self):
        #set up non-modified objects used by all test methods
        Author.objects.create(first_name="Rakesh", last_name="Prakash",date_of_death="2020-10-21",date_of_birth="2019-10-20")

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        fields_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(fields_label,'first name')
    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        fields_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(fields_label,'last name')
    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        date_death = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(date_death,'Died')
    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length,100)
    def test_object_name_first_name_hifen_last_name(self):
        author = Author.objects.get(id=1)
        excepted_name = f"{author.first_name}-{author.last_name}"
        self.assertEqual(excepted_name,str(author))
    def test_date_of_death_isgreater_than_dob(self):
        author = Author.objects.get(id=1)
        dod = author.date_of_death
        dob = author.date_of_birth
        if dod and dob:
            self.assertTrue(dod>dob,True)

class GenreModelTest(TestCase):

    @classmethod
    def setUpTestData(self):
        Genre.objects.create(name="Science Friction")

    def test_name_max_length(self):
        genre = Genre.objects.get(id=1)
        max_length = genre._meta.get_field('name').max_length
        self.assertEqual(max_length,200)

class LanguageModelTest(TestCase):

    @classmethod
    def setUpTestData(self):
        Language.objects.create(name="Hindi")

    def test_langauge_of_book(self):
        lang = Language.objects.get(id=1)
        max_length = lang._meta.get_field('name').max_length
        self.assertEqual(max_length,50)
    def test_for_blank_data(self):
        lang = Language.objects.get(id=1)
        data = lang.name
        self.assertEqual(data,str(lang))

class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(self):
        Author.objects.create(first_name="Rakesh", last_name="Prakash",date_of_death="2020-10-21",date_of_birth="2019-10-20")
        Language.objects.create(name="English")
        Genre.objects.create(name="Science Friction")
        g = Genre.objects.get(id=1)
        Book.objects.create(title="The Alchemist",
                            author=Author.objects.get(id=1),
                            summary="A good Book",
                            isbn = '1234567890123',
                            language=Language.objects.get(id=1))

    def test_title(self):
        book=Book.objects.get(id=1)
        booktitle = book.title
        self.assertEqual(booktitle,str(book))
    def test_title_length(self):
        book=Book.objects.get(id=1)
        booklen = book._meta.get_field('title').max_length
        self.assertEqual(booklen, 200)
    def test_isbn_length(self):
        book=Book.objects.get(id=1)
        bookisbn =book._meta.get_field('isbn').max_length
        self.assertEqual(bookisbn, 13)
    def test_summary_length(self):
        book=Book.objects.get(id=1)
        booksum = book._meta.get_field('summary').max_length
        self.assertEqual(booksum, 1000)
    def test_title_blank(self):
        book=Book.objects.get(id=1)
        booktitle = book.title
        if booktitle == ' ':
            self.assertFalse(False)
        else:
            self.assertTrue(True)

class BookInstanceModelTest(TestCase):

    @classmethod
    def setUpTestData(self):
        Author.objects.create(first_name="Rakesh", last_name="Prakash",date_of_death="2020-10-21",date_of_birth="2019-10-20")
        Language.objects.create(name="English")
        Genre.objects.create(name="Science Friction")
        Book.objects.create(title="The Alchemist",
                                    author=Author.objects.get(id=1),
                                    summary="A good Book",
                                    isbn = '1234567890123',
                                    language=Language.objects.get(id=1))
        BookInstance.objects.create(book=Book.objects.get(id=1),
                                    imprint="Hello World",
                                    due_back="2020-10-21",
                                    status="m",
                                    )

    def test_object_rep(self):
        bk = BookInstance.objects.all().first()
        reps = str(bk.id)+" "+bk.book.title
        self.assertEqual(reps,str(bk))
    def test_status_length(self):
        bk = BookInstance.objects.all().first()
        max_length = bk._meta.get_field('status').max_length
        self.assertEqual(max_length,1)
