from django.forms import ModelForm, Textarea

from.models import Room, Message

class RoomForm(ModelForm):
  class Meta:
    model =  Room
    fields = '__all__'

class CommentForm(ModelForm):
  class Meta:
    model = Message
    fields = ['body']
    widgets = {
      'body': Textarea(attrs={'placeholder': 'Escribe tu comentario....'})
    }
    labels = {
      'body': ''
    }