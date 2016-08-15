from django.conf.urls import patterns, include, url
from django.contrib import admin

#internal
from note.views import NoteCreateView,PreviewNoteView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',
            NoteCreateView.as_view(), name='secure_note_base'),
    url(r'^secure/(?P<noteID>[\w-]+)',
            PreviewNoteView.as_view(), name='secure_note_preview'),
)
