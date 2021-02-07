from django.contrib import admin
from api.models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Video._meta.fields]
    list_per_page = 50
    fields = list_display
    readonly_fields = list_display
    search_fields = ['title', 'description']
    actions = None
    list_filter = ('published_at', )
    date_hierarchy = 'published_at'

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id=None, form_url='',
                    extra_context=None):
        template_response = super(VideoAdmin, self).change_view(request, object_id, form_url, extra_context)
        template_response.content = template_response.rendered_content.replace(
            '<div class="submit-row">',
            '<div class="submit-row" style="display: none">')
        return template_response


admin.site.register(Video, VideoAdmin)
