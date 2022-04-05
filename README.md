<h1>Django Custome User Model</h1>
<p>This is a simple example showing how to create a custom user model for authentication and usermanagment</p>
<br>
<h3>Key Things to note befroe starting</h3>
<ul>
  <li>Add your environment variables in <i>Core/Core/.env</i></li> (especially: SECRET_KEY, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, RECIPIENT_ADDRESS)
  <li>Update <i>Core/Core/settings.py</i> with all your custom initial conditions</li>
  <li>Add any apps you need and whenever you refernce the user inside the view, use the <i>request</i> object</li>
</ul>

run the server like anyother django project
