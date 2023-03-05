from django.contrib import admin
from fetchyoutubedata.models import YoutubeVideoAPIKey


class YoutubeVideoAPIKeyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in YoutubeVideoAPIKey._meta.fields]
    list_per_page = 50
    fields = list_display
    date_hierarchy = 'modified'
    readonly_fields = ['id', 'created', 'modified']


admin.site.register(YoutubeVideoAPIKey, YoutubeVideoAPIKeyAdmin)
