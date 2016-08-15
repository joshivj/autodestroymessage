import json
import datetime

from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
# Create your views here.

#internal imports
from .queries import create_random_key,create_hashkey,encrypt,decrypt,get_client_ip
from .models import SecureNotes

class NoteCreateView(View):
    """
    View to handle get and post of secure note creation page
    """
    template_html = 'secretenote.html'

    def get(self,request, *args, **kwargs):
        """
        To render the template
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return render_to_response(self.template_html,RequestContext(request))

    def post(self,request, *args, **kwargs):
        """
        Handles the secret note creation
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ajax_template_html = 'securenotelink.html'
        text_data = self.request.POST.get('note')
        #get randon string to be used as slug
        random_key = create_random_key()

        #hash this random key
        hashed_key = create_hashkey(random_key)

        #Now encrypt the note using the recently hashed key
        encrypted_text = encrypt(text_data,random_key)

        #save this encrypted text/ciphertext and hashed key in DB
        SecureNotes.objects.create(
            key=hashed_key,notes=encrypted_text
        )

        #return the new template containing link using which user can retrieve the Note, only one time retrival
        template_context = {
            'link':request.META.get('HTTP_HOST') + reverse('secure_note_preview',kwargs={
                'noteID':random_key
            })
        }
        response = render_to_string(ajax_template_html, template_context)

        return HttpResponse(json.dumps({'status':True,
                                       'response': response
                                        }))


class PreviewNoteView(View):
    """
    This class handles the decryption of note using the noteID which was send to user when he created it
    """

    template_html = 'secretenotepreview.html'

    def get(self,request, *args, **kwargs):
        """
        To render the template
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        #when user enter the url for the first time, show a message do you want to see it as it will get self destroyed after that
        noteid = kwargs.get('noteID')
        if self.request.GET.get('show_me'):
            # use the noteID in url and create hashkey of noteid then use this hashednoteID to get record from db and descrypt message

            hashednoteID = create_hashkey(noteid)

            #now use this hashednoteID to fetch record from DB
            if SecureNotes.objects.filter(key=hashednoteID).exists():
                noteObj = SecureNotes.objects.get(key=hashednoteID)
                if noteObj.is_active:
                    descrypted_text = decrypt(noteObj.notes,noteid)

                    # as the user will view this message, make is_Active false and delete the message from record and
                    # add modifiedtime stamp
                    noteObj.is_active = False
                    noteObj.reader_ipaddress = get_client_ip(request)
                    noteObj.notes = ''
                    noteObj.save()
                    # render template containing decrypted text
                    return render_to_response(self.template_html,RequestContext(request,
                                                                            {
                                                                                'recordexists':True,
                                                                                'status':True,
                                                                                'message':descrypted_text,
                                                                                'additional_msg':'This message will self destroy,Please save the note'
                                                                            }))

                else:
                    # render template showing the time at which message was read

                    message = 'Note has been self destructed, It was read at ' + noteObj.read_date.strftime("%Y-%m-%d %H:%M")
                    if noteObj.reader_ipaddress:
                        message = message + ' from IP:-' + noteObj.reader_ipaddress
                    return render_to_response(self.template_html,RequestContext(request,
                                                                            {
                                                                                'recordexists':False,
                                                                                'status':True,
                                                                                'message':message
                                                                            }))
            else:
                # return new template containing information such that your secret record does not exists
                return render_to_response(self.template_html,RequestContext(request,
                                                                            {
                                                                                'status':False,
                                                                                'message':'Note Does not exists'
                                                                            }))
        else:
            return render_to_response(self.template_html,RequestContext(request,
                                                                        {
                                                                                'status':False,
                                                                                'message':'Do you want to view the Note, if will self destroy after you read it',
                                                                                'only_preview':True,
                                                                                'noteid':noteid
                                                                            }))





