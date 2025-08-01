from django.http import HttpResponse
from django.contrib.auth import authenticate
from .authentication.models import User

def debug_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        response_html = "<h1>Debug Login</h1>"
        response_html += f"<p>Email: {email}</p>"
        response_html += f"<p>Password: {'*' * len(password)}</p>"
        
        try:
            user = User.objects.get(email=email)
            response_html += f"<p>User found: {user.username}</p>"
            
            if user.check_password(password):
                response_html += "<p>Password check: OK</p>"
                
                authenticated_user = authenticate(request, email=email, password=password)
                if authenticated_user:
                    response_html += "<p>Authentication successful</p>"
                else:
                    response_html += "<p>Authentication failed</p>"
            else:
                response_html += "<p>Password check: FAILED</p>"
                
        except User.DoesNotExist:
            response_html += "<p>User not found</p>"
            
        return HttpResponse(response_html)
    else:
        return HttpResponse("Please use POST method to debug login.")