"""
Django app for reporting data errors
"""



from django.shortcuts import render
from django import forms
from django.core.mail import send_mail

from django.conf import settings


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
    
    errormessage = ''  # error message to display to the user
    
    # did the user submit the form?
    if request.method == 'POST':
        submitted = True
        form = ErrorForm(request.POST)
        
        if form.is_valid():
            try:
                sendErrorReport(form.cleaned_data)
                
            except:
                if settings.DEBUG: # show error page in debug mode
                    raise 
                else:
                    # if something went wrong trying to report the error, show an error message
                    errormessage = 'Something went wrong on the AntMaps server!  Your error report might not have been submitted.'
                
            
    else:
        submitted = False
        form = ErrorForm()
        
    return render(request, 'error_report/report.html', {'form':form, 'submitted':submitted, 'errormessage': errormessage})
            
            
            

def sendErrorReport(cleaned_data):
    """
    Send an email with the contents of the error report
    """
    
    message = """
ANTMAPS DATA ERROR REPORT
-------------------------

Sender name:  {name}
Sender email: {email}


---------Message---------

{message}
""".format(**cleaned_data)
    
    send_mail(
        subject='AntMaps data error report', 
        message=message, 
        from_email=settings.EMAIL_HOST_USER, 
        recipient_list=[settings.REPORT_TO_EMAIL_ADDRESS])
