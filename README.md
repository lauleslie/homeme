# Web2py
CMPS 183 Web Applications (Hypermedia and the Web)

Assignment

You need to create a site composed of two pages. 

Home Page

The home page behaves differently, according to whether the user is logged in or not. 
Please look at the checklists application we are developing in class for an example of how to achieve this. 

Not logged in

If the user is not logged in, at the top there should be a button to login (this is done for you in the starter code). 
Below, the home page should display the list of the 20 most recent posts, with the most recent on top.  You can find the instructions for doing so in the database abstraction layer chapter of the web2py book.  For each post, you should display:
The post content
The author of the post (using first_name last_name).  Note: see the function get_user_name_from_email in the starter code for how to get the user name given the email.  There are better ways of doing this (using joins), but this will suffice for now.
The date when the post was created
The date when the post was edited, if different from the date when the post was created
See the drawing below for an example.  Notes: 
You don't need to make your page look identical to this; this is a schematic representation only.
The dates will display in UTC. This is intended.  I will teach you later how to convert these to the user local time zone.
Feel free to display the time in the best possible way, e.g., "12 minutes ago", "4 hours ago", "Yesterday 3pm", ... there are python libraries for converting from a datetime into a "humane" time representation.  I leave this as an exercise. 
Example of not logged in home page


Logged in

If the user is logged in, the page should display at the top a button to add a new post (the button is there for you in the starter code). 
Below, as before, there should be the list of the 20 most recent posts, with the most recent on top. 
For each post, you should display:

The post content
The author of the post (using first_name last_name)
The date when the post was made
The date when the post was edited, if different from the date when the post was created
If the post was made by the author, a button to edit/delete the post.
See example below.  Again, you don't need to make it look identical to this.

Example of logged in home page


Note that in this example, the logged in user (Luca de Alfaro) can edit only the posts that he created, so the "Edit" icon is present only for those posts. 
Note also how the edited date is displayed only when different from the creation date. 

Page to Add/Edit/Delete Posts

This page should be accessed by a URL of type: edit/<post_id> , such that if the post_id is specified, the page will allow the user to edit or delete the post, and if the post_id is not specified, the page will allow the user to add a new post.  You can create these URLs as follows:
To create a post: URL('default', 'edit')
To edit a post with id post_id: URL('default', 'edit', args=[post_id])
See here for more documentation on the URL helper. When the user accesses that page, the controller code should check the following: 
The user is logged in.
If a post is specified, the post exists.
If a post is specified, the post was created by the user who is logged in.
The page should display a form that enables the user to create / edit / delete the post; you can use SQLFORM for this.  Once the post has been added / edited / deleted, you can redirect the user back to the home page.  Bonus points: add a CANCEL button that enables the user to go back to the index without performing any edit. 

Starter Code

You can find starter code in the hw2 branch of our starter app.  The code defines the database table for you, and it contains (empty) shells for the controllers.  I did a bit of styling of the list of posts for you.  Look in particular at models/tables.py, controllers/default.py and views/default/index.html, as well as static/sass/_main.scss. 
