from django.contrib import admin
from .models import Book,BookInstance,Genre,Author,Language
# Register your models here.


#admin.site.register(Book)
#admin.site.register(BookInstance)
admin.site.register(Genre)
#admin.site.register(Author)
admin.site.register(Language)

class BookAdminInline(admin.TabularInline):
    model = Book
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','date_of_birth','date_of_death')
    fields = ['last_name','first_name',('date_of_birth','date_of_death')]
    inlines = [BookAdminInline]
admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','display_genre','language')
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','status','due_back','borrower','id')
    list_filter = ('status','due_back')
    fieldsets = (
      (
        None, {
           'fields': ('book','imprint','id')
        }
      ),
      (
        'Availability', {
           'fields': ('status','due_back','borrower',)
        }
      ),
    )
