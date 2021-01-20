import markdown2
import random

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.contrib.auth.decorators import login_required



from . import util
from markdown2 import Markdown 


class newForm(forms.Form):
	title = forms.CharField(label="Wiki title", widget=forms.TextInput(attrs={'class': 'form-control col-md-10 col-lg-10'}))
	content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-10 col-lg-10', 'rows': 12}))
	edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)
	

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
	md= Markdown()
	wiki= util.get_entry(entry)
	
	if wiki is None:
		return render(request, "encyclopedia/noEntry.html", {
			"entryTitle": entry
			})
	else:
		return render(request, "encyclopedia/entry.html", {
			"entry": md.convert(wiki), 
			"entryTitle": entry
			})

def new(request): 
	if request.method == "POST":
		form = newForm(request.POST)

		if form.is_valid():
			
			title = form.cleaned_data["title"]
			content = form.cleaned_data["content"]
			
			if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
				util.save_entry(title,content)
				return HttpResponseRedirect(reverse("entry", kwargs={'entry':title }))
			
			else:
				return render(request, "encyclopedia/new.html", {
					"form": form, 
					"existing": True, 
					"entry": title
					})
		else:
			return render(request, "encyclopedia/new.html", {
				"form": form, 
				"existing": False
				})
	else:
		return render(request, "encyclopedia/new.html", {
			"form": newForm(),
			"existing": False
			})

def edit(request, entry):
	wiki = util.get_entry(entry)
	
	if wiki is None:
		return render(request, "encyclopedia/noEntry.html", {
			"entryTitle": entry
			})
	else:
		form= newForm()
		form.fields["title"].initial = entry 
		form.fields["title"].widget = forms.HiddenInput()
		form.fields["content"].initial = wiki
		form.fields["edit"].initial = True
		return render(request, "encyclopedia/new.html", {
			"form": form, 
			"edit": form.fields["edit"].initial,
			"entryTitle": form.fields["title"].initial
			})


def search(request):
	value = request.GET.get('q', '')

	if(util.get_entry(value) is not None):
		return HttpResponseRedirect(reverse("entry", kwargs={'entry':value }))
	
	else:
		sub=[]
		
		for entry in util.list_entries():
			if value.lower() in entry.lower():
				sub.append(entry)

		return render(request, "encyclopedia/index.html", {
			"entries": sub, 
			"search": True, 
			"value": value
			})

def rdm(request):
    wikis = util.list_entries()
    rdm = random.choice(wikis)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry':rdm}))




