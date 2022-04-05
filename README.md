<h1>Django Custome User Model</h1>
<p>This is a simple example showing how to create a custom user model for authentication and usermanagment</p>
<br>
<h3>Key Things to note befroe starting</h3>
<ul>
  <li><b>Finish setting up the <i>customUserModel</i> inside <i>Core/user/models.py</i> before you run <i>python manage.py makemigrations</i>for the frist time. If you don't, you'll have issues updating the database file. (If you already initiated the database with the builtin user model, you need to manually delete all tables connected to the user model as well as all migration files and then create a new super user)</b></li>
  <li>Add your environment variables in <i>Core/Core/.env</i></li> (especially: SECRET_KEY, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, RECIPIENT_ADDRESS)
  <li>Update <i>Core/Core/settings.py</i> with all your custom initial conditions</li>
  <li>Add any apps you need and whenever you refernce the user inside the view, use the <i>request</i> object</li>
</ul>

Once you finish setting up, 

run the server like anyother django project
