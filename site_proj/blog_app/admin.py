from django.contrib import admin
from .models import Post, Comment

#? zwykly sposob registracji
# admin.site.register(Post)

#? personalny sposob wyswietlenia danych
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status') #? tablica
    list_filter = ('status', 'created', 'publish', 'author') #? bokowa panel filtru
    search_fields = ('title', 'body') #? Wyszukiwarka
    prepopulated_fields = {'slug':('title',)} #? automatyczne uzupelnenie pola 'slug' w ADD POST
    raw_id_fields = ('author',) #? dodaje widzet dla tego pola ? ulatwia wyszukiwanie w ADD POST
    date_hierarchy = 'publish' #? dodaje date nad tablica
    ordering = ('status', 'publish') #? sortuje 'default'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'email', 'created', 'active')
    list_filter = ('active', 'created', 'update')
    search_fields = ('name', 'email', 'body')
