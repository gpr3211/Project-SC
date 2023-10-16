# Project-SC
#### Video Demo:
#### Description: 
<p>Project Scorpio is an exercise based website.It is built using html,python and flask with a local SQL database of exercises.There is some minor JS functionality for greeting users.The website features an Admin dashboard that allows direct queries on the database in the form of adding or removing exercises and users . Admin page has restricted access and is only visible to users with admin priviliges.
</p>



Lets the user generate a sample workout from a database of exercises, save favorite exercises and keep track of record lifts.<br><br>
<h3>Website User Overview </h3><br>

1.Register,Login,Index page.
  - User registers and is saved to a database where his password is hashed.
  - User logs
  - user is greeted with a java alert
  - user given links to the different pages + navbar

2.Generate page,
  - lets the user choose up to 2 muscle groups and 1 equipment 
  - return exercises including instructions with images.In a table with 3 rows. Users can receive up to 10 results depending on their search.


3.Favorite
  - User can select an exercises from our database and add/remove it their favorites.Users current  favorite exercises are displayed below <br>

4.History 
  - User can record his power lift records<br>
<h3>Developer Overview </h3>

1.File structure.
  - templates folder contains our html files. We use layout.html as a base for the rest our pages..
  - static folder contains the styles.css file and the images for the website. We only save the name in our database. Image naming convention for our DB is "foo-bar.jpg"
  - scorpio.db is our SQL database containing tables of users with hashed passwords, exercises table( short description, name, id , image containing 2 steps ), user favorites, branches and equipment. 
  - app.py. Here is most of our python/flask code.
  - helpers.py contains our login required and error display functions
  - requirements.txt lists the required packages to run the website
  - config.py just tells Flask to always run debugger 

2.Maintenance.
  - lets look at app.py
    - "/" route or "templates/index.html" is only accessable after registration and login 
      - we execute a query on the db for the logged in user "session["user_id"] and greet them by username at index.html
    - "/generate" -> "templates/generate.html"
      - if request is GET we query branches and exercises and render generate template
      - if request is POST it means user is trying to generate a workout. First we check if imputs are all in place and if not we return an error
        - If all inputs are correct we query our db for the comments and exercises  and return quoted.html with the generated workout displayed in a table with 3 rows.
    - "/fav" -> "templates/favorites.html" Is where the user can save and remove exercsises 
      - if request method is GET then make queries on the database to show the user a select menu that allows them to choose an exercise and add it to their favoriites
      - if request method is POST  we insert a new entry into the favorites table in our database with the selected exercise's ID and user ID. fav ID is autoincremented in SQL.
      - "/fav_remove" lives on the same page as favorites. It is the function that allows us to display a remove button next to each fav exercise .
    - "admin" -> "templates/admin.html" 






















