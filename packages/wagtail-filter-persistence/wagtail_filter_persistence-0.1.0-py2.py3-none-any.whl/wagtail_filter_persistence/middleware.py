from django.utils.deprecation import MiddlewareMixin
from urllib.parse import urlparse, parse_qs, urlencode
from django.http import HttpResponseRedirect

class WagtailFilterPersistenceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if this is a Wagtail admin request
        if not request.path.startswith('/admin/'):
            return None
            
        # Store filter params when viewing a listing
        if 'modeladmin' in request.path and not request.path.endswith('/create/') and not '/edit/' in request.path:
            query_params = parse_qs(request.META.get('QUERY_STRING', ''))
            if query_params:
                request.session['wagtail_filters_' + request.path] = query_params
                
        # Check if returning to a listing page (typically via breadcrumb)
        referer = request.META.get('HTTP_REFERER', '')
        parsed_referer = urlparse(referer)
        referer_path = parsed_referer.path
        
        # If we're on a listing page with no query params but have stored filters
        if (not request.META.get('QUERY_STRING') and 
            'modeladmin' in request.path and 
            'wagtail_filters_' + request.path in request.session):
            
            stored_params = request.session.get('wagtail_filters_' + request.path)
            if stored_params:
                # Redirect to the same URL but with the stored parameters
                query_string = urlencode(stored_params, doseq=True)
                redirect_url = request.path + '?' + query_string
                return HttpResponseRedirect(redirect_url)
                
        return None