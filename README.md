# book-recommendation-system

<h2>Requirement:</h2>

Software requirements:
<p>
If the system doesn't work as expected try installing the exact version of the software/libraries.
</p><br>
<ul>
<li>python 3 (3.6.5)</li>
<li>django (2, 0, 4, 'final', 0)</li>
<li>pandas (0.24.1)</li>
<li>numpy (1.15.0)</li>
<li>scipy (1.1.0)</li>
<li>scikit-learn (0.20.3)</li>
</ul>

<h2>Installations</h2>
<p>

pip install django


Install python, django and other libraries(use google if necessary)
download and extract the repository to your desired location, <strong>go to the root folder of the project and open terminal and run the following commands</strong> and run the following commands.
For Windows use python and for Linux use python3 in commands.

</p>

<h3>To setup database</h3>
<code>python manage.py makemigrations</code><br>
<code>python manage.py migrate</code>

<h3>Create superuser</h3>
<code>python manage.py createsuperuser</code><br>
Add the details asked

<h3>Load data(user, books, ratings)</h3>
<code>python load_books.py data/books.csv</code><br>
<code>python load_users.py data/users.csv</code><br>
<code>python load_rating.py data/ratings.csv</code><br>

<h3>Run server</h3>
<code>python manage.py runserver</code><br>
<p>
open google chrome or any browser, go to <code>localhost:8000</ode>
</p>

<h3>Additional Info</h3>
To open admin panel
go to <code>localhost:8000/admin</code><br>
Enter username and password of superuser to log in.
