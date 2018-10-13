from django.shortcuts import render, redirect
from django.views.generic import TemplateView
#from sentiment.forms import HomeForm
from .models import Grab_Twitter
# Create your views here.
class HomePageView(TemplateView):
    template_name = 'index.html'

#    def get(self, request):
 #       form = HomeForm()
  #      return render(request, self.template_name, {'form': form} )
    
   # def post(self, request):
    #    form = HomeForm(request.POST)
     #   if form.is_valid():
      #      text = form.cleaned_data['First_Election_Candidate']
       #     form.save() 
        #    args = {'form': form, 'text': text}
         #   return render(request, self.template_name, args )

class AboutPageView(TemplateView):
    template_name = "about.html"

def search(request):
    if request.method == "POST":
        First_Election_Candidate = request.POST["First_Election_Candidate"]
        Second_Election_Candidate = request.POST["Second_Election_Candidate"]
        
        search_twitter = Grab_Twitter(First_Election_Candidate)
        return redirect("basic.html")
    else:
        return redirect("/")


