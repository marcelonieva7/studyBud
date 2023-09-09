from django.forms import ModelForm, Textarea, HiddenInput

from.models import Room, Message

class RoomForm(ModelForm):
  class Meta:
    model =  Room
    fields = '__all__'

class CommentForm(ModelForm):
  class Meta:
    model = Message
    fields = '__all__'
    widgets = {
      'body': Textarea(attrs={'placeholder': 'Escribe tu comentario....'}),
      'user': HiddenInput(),
      'room': HiddenInput(),
    }
    labels = {
      'body': ''
    }