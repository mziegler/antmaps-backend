"""
Django app for reporting data issues
"""


from time import time

from django.shortcuts import render
from django import forms
from django.core.mail import send_mail
from django.views.decorators.cache import never_cache

from django.conf import settings


class ErrorForm(forms.Form):
    """
    Form for report-data-issue page
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
        
        
    

@never_cache
def report(request):
    """
    Data issue report page
    
    This view validates the form, and calls sendErrorReport if the form is valid
    """
    
    errormessage = ''  # error message to display to the user
    
    # did the user submit the form?
    if request.method == 'POST':
        submitted = True
        form = ErrorForm(request.POST)
        
        if form.is_valid():
            try:
                sendErrorReport(form.cleaned_data)
                
            except Exception as e:
                if settings.DEBUG: # show default error page in debug mode
                    raise 
                    
                else: # if we're not in debug mode, (if we're deployed on Apache)
                
                    # if something went wrong trying to report the error, show a friendly error message
                    errormessage = 'Something went wrong on the AntMaps server!  Your report might not have been submitted.'
                    
                    # write the error to the Apache error log
                    import logging; logging.error(str(e))
                
            
    else:
        # show a blank error form if there's no POST
        submitted = False
        form = ErrorForm()
        
        
    return render(request, 'error_report/report.html', {'form':form, 'submitted':submitted, 'errormessage': errormessage})
            
            
            
            

def sendErrorReport(cleaned_data):
    """
    Send an email with the contents of the issue report form
    """
    
    message = """
ANTMAPS DATA ISSUE REPORT
-------------------------

Sender name:  {name}
Sender email: {email}


---------Message---------

{message}
""".format(**cleaned_data)
    
    send_mail(
        subject='AntMaps data issue report ' + str(int(time())), # add timestamp 
        message=message, 
        from_email=settings.EMAIL_HOST_USER, 
        recipient_list=[settings.REPORT_TO_EMAIL_ADDRESS])
