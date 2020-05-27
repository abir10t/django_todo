from django.forms import ModelForm #TodoForm needs inheret, so we import it
from .models import Todo
class TodoForm(ModelForm):
    class Meta: #specify what class it is,what model,fields we want ,so we need to use meta class
      model =Todo #specifying the model ,and we need to import from .models import Todo
      fields=['title','memo','important'] #specify what we want
