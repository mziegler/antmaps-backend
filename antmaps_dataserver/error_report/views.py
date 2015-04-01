"""
Django app for reporting data errors
"""



from django.shortcuts import render
from django import forms



class ErrorForm(forms.Form):
    """
    Form for report-data-error page
    """

    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    humantest = forms.CharField()
    
    
    def clean_humantest(self):
        """
        Check to see that the user entered "ants" in the security field
        """
        val = self.cleaned_data['humantest']
        
        if not val.strip().lower() in ['ant', 'ants', 'an ant', 'a ant']:
            raise forms.ValidationError('Incorrect answer!  (Hint: please type "ant" into this box.)')
        return val
        
        
    

def report(request):
    """
    Data error report page
    """
    
    # did the user submit the form?
    if request.method == 'POST':
        submitted = True
        form = ErrorForm(request.POST)
        
        if form.is_valid():
            sendErrorReport(form.cleaned_data)
            
    else:
        submitted = False
        form = ErrorForm()
        
    return render(request, 'error_report/report.html', {'form':form, 'submitted':submitted})
            
            
            

def sendErrorReport(cleaned_data):
    """
    TODO: Do something with the validated form data (send an email?)
    """
    print(cleaned_data)
