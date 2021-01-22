import sys, os 
import pandas as pd

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_book.settings")
django.setup()
from book.models import Book

def save_book_from_row(book_row):
    book = Book()
    book.id = book_row[0]
    book.title = book_row[1]
    # book.category=book_row[2]
    book.author = book_row[3]
    book.publication =book_row[4]
    book.category = book_row[5]
    book.save()
    

if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print ("Reading from file " , str(sys.argv[1]))
        booksdf = pd.read_csv(sys.argv[1], sep=',', encoding='latin-1')
        print (booksdf)

        booksdf.apply(
            save_book_from_row,
            axis=1
        )

        print ("There are {} books".format(Book.objects.count()))
        
    else:
        print ("Please, provide Book file path")
