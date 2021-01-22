from book.models import Book
class GetBooks:
    def __init__(self,get_response):
        self.get_response = get_response
        
    
    def __call__(self,request):
        response = self.get_response(request)
        abcd = list(Book.objects.all().values().order_by('-id')[:7])
        request.session['book'] = abcd
        return response