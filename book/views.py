from django.shortcuts import get_object_or_404, render
from .models import Review, Book
from .form import ReviewForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User

from django.contrib.auth import logout
from django.shortcuts import redirect

from django.views import generic
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

# require ML libraries
import pandas as pd
import numpy as np
import scipy as sp
from sklearn.neighbors import NearestNeighbors

import operator

# To get latest reviews given by users
def review_list(request):
    latest_review_list = Review.objects.all().order_by('-id')[:10]
    context = {'latest_review_list': latest_review_list}
    return render(request, 'review_list.html', context)

# To get all the reviews of individual books
def review_detail(request , pk):
    review = get_object_or_404(Review, id=pk)
    return render(request, 'review_detail.html',{'review': review})
    
# To get latest 20 books from database
# currently not used in the project
def book_list(request):
    book_list = Book.objects.order_by('-title')[:20]
    context = {'book_list':book_list}
    return render(request, 'book_list.html', context)

# To get details of the book (author, publication, average rating, etc)
def book_detail(request , pk):
    book = get_object_or_404(Book,id= pk)
    form = ReviewForm()
    return render(request, 'book_detail.html', {'book':book})

# To add users review (feedback)
def add_review(request, pk):
    # To check if book is available in the database
    book = get_object_or_404(Book, id=pk)

    us = get_object_or_404(User, id=request.user.id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.book = book
        review.user_id = us
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.save()
        return HttpResponseRedirect(reverse('book_detail', args=(book.id,)))
    return render(request,'book_detail.html', {'book':book, 'form':form})


def logout_view(request):
    logout(request)
    return redirect('/')

# To register new user
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

# collaborative filtering
# To get recommendation based on users past history
def get_suggestions(request):

    # Check if user is logged in, if not the redirect to login page
    if request.user.is_authenticated:
        num_reviews = Review.objects.count()
        all_user_names = list(map(lambda x: x.id, User.objects.only("id")))
        all_user_names = sorted(all_user_names)
        all_book_ids = set(map(lambda x: x.book.id, Review.objects.only("book")))
        num_users = all_user_names[-1]
        sizeofusers = len(list(all_user_names))-1
        bookRatings_m = sp.sparse.dok_matrix((num_users+1, max(all_book_ids)+1),dtype=float) #defining matrix dimensions (MxN)
        for i in range(num_users): #each user corrsponds to a ro, in the order of all_user_names
            if i > sizeofusers:
                break
            user_reviews = Review.objects.filter(user_id=all_user_names[i])
            for user_review in user_reviews:
                bookRatings_m[all_user_names[i], user_review.book.id] = user_review.rating
        
        bookRatings = bookRatings_m.transpose()
        
        coo = bookRatings.tocoo(copy=False)
        
        # pivoting dataframe
        df = pd.DataFrame({'books':coo.row, 'users':coo.col, 'rating': coo.data}
                        )[['books','users','rating']].sort_values(['books','users']
                        ).reset_index(drop=True)
        
        # get logged in users id
        Userpk = request.user.id

        # check if user has given any ratings before, if not then display most popular books in else part
        if Userpk in df.users.values:

            # filling empty values as zero as data is in sparse matrix form and creating pivot table
            bo = df.pivot_table(index=['users'], columns=['books'], values='rating',fill_value=0)
            
            # Defining parameters of KNN model
            model_knn = NearestNeighbors(algorithm='brute', metric='cosine')

            # creating model
            model_knn.fit(bo.values)

            # getting nearest(similar) neighbours(users) to logged in user.
            distances, indices = model_knn.kneighbors(bo.loc[Userpk, :].values.reshape(1,-1), n_neighbors=10, return_distance=True)
            
            best = []
            bo = bo.transpose()
            
            # converting to 1D array
            indicesflatten = indices.flatten()


            # for i in indices.flatten():
            #     if i > 609:
            #         indicesflatten.append(all_user_names[i]) 
            #     else:
            #         indicesflatten.append(all_user_names[i])


            # best books according to similar users
            for i in indicesflatten:
                if (i != Userpk):
                    max_score = bo.loc[:, i].max()
                    best.append(bo[bo.loc[:,i] == max_score].index.tolist())

            #books read by user       
            user_read_book = bo[bo.loc[:, Userpk]>0 ].index.tolist() 

            # remove books read by user from best books
            for i in range(len(best)):
                for j in best[i]:
                    if (j in user_read_book):
                        best[i].remove(j)

            # no. of times books recommended
            most_common={}
            for i in range(len(best)):
                for j in best[i]:
                    if j in most_common:
                        most_common[j]+=1
                    else:
                        most_common[j]=1


            sorted_list = sorted(most_common.items(), key =operator.itemgetter(1), reverse= True)
            rec = []
            for i in sorted_list:
                rec.append(i[0])

            # Getting book object fro database using book id
            context  = list(map(lambda x: Book.objects.get(id=rec[x]),range(0,len(rec))))
            return render(request, 'get_suggestions.html',{'context' :context})

    #------------------for new users (popular books shown)--------------------
        else:
            bookStats = df.groupby('books').agg({'rating':[np.size, np.mean]})
            popularBooks = bookStats['rating']['size']>10
            bookStats = bookStats[popularBooks].sort_values([('rating', 'mean')],ascending=False)[:10]
            booklist = bookStats.index.tolist()
            context  = list(map(lambda x: Book.objects.get(id=booklist[x]),range(0,len(booklist))))
            
            return render(request, 'get_suggestions.html',{'context' :context})
    return HttpResponseRedirect(reverse('login'))


# content based filtering(based on search)
def get_suggestions2(request):

    # extracting users selected(searched) book category from front end
    checkedlist = request.GET.getlist('bookselected')

    # to see if user has selected any category
    if len(checkedlist):
        lists = []
        dicts = {}

        # creating list of dictionary from book model, key = category, value = book id
        for i in Book.objects.all():
            dicts['category'] = i.category
            dicts['bid'] = i.id
            lists.append(dicts.copy())

        # making a list of categories of book from database sepearted by '|'
        df = pd.DataFrame(lists)
        df = pd.concat([df,df['category'].str.get_dummies(sep = '|')],axis=1)
        columns = list(df.head(0))
        cleanedColumn = columns[2:]
        
        N = 5
        if 3 <= len(checkedlist) <=6:
            N=7
        elif len(checkedlist)>6:
            N=9

        # creating an array(list) of 1 and 0
        # if user has selected the book then put 1 in list else 0
        # array would look something like this [1,0,0,0,0,0,1,0,1,0]
        selected = []
        for i in cleanedColumn:
            if i in checkedlist:
                selected.append(1)
            else:
                selected.append(0)

        # passi paramteres and creating mathematical model
        X= df.iloc[:, 2:]
        nbrs = NearestNeighbors(n_neighbors=N).fit(X)
        booksrec = nbrs.kneighbors([selected])

        # 1D list
        booklists = []
        for i in list(booksrec)[1][0]:
            booklists.append(i+1)
        
        # retrieving books data(object) using book id from database
        context  = list(map(lambda x: Book.objects.get(id=booklists[x]),range(0,len(booklists))))
        
        return render(request, 'get_suggestions2.html',{'context':context})
    

    # if user has not selected any category then show recommendation based on collaborative filtering
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('get_suggestions'))


    return HttpResponseRedirect(reverse('login'))


#-------------------------------------------
# get recently added books to database
def latestbooks():
    return Book.objects.all().order_by('-id')[:10]

# get all books present in the database
def allBooks(request):
    allbooks = Book.objects.all()
    # allbooks = Book.objects.all().order_by('-id')[:10]
    return render(request, 'allbooks.html',{'context' :allbooks})


#display all types(categories) of books available in the database to user to select for content based filtering(search)
def select(request):
    lists = []
    dicts = {}
    for i in Book.objects.all():
        
        dicts['category'] = i.category
        dicts['bid'] = i.id
        lists.append(dicts.copy())

    df = pd.DataFrame(lists)
    df = pd.concat([df,df['category'].str.get_dummies(sep = '|')],axis=1)
    columns = list(df.head(0))
    cleanedColumn = columns[2:]
    return render(request, 'select.html',{'context': cleanedColumn})