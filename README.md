# Postfeed

## Description

Postfeed is a website that is a personal blog with the ability to publish posts from the admin account and comment on them to all registered users.
## Technical features

The project is written in Python, implemented using the Django framework. Class representations are used. A custom mixin has been implemented to simplify the insertion of data into the context. A custom template tag has been implemented to simplify the display of frequently repeated data on the page. It is possible to add categories for articles and view the list of articles of the selected category. It is possible to search through articles by the occurrence of a given line in the title or in the content of the article. The list of articles on the main page uses pagination. An account system has been implemented with the ability to register, log in and log out of an account. Registered users have a profile where you can view a list of comments sent from this account. The profiles of other users are not available for viewing. Access to the page for creating articles is restricted for users who do not have administrator rights. The form for sending comments is not visible to unregistered users.
The project consists of one application, which has three models for articles, categories of articles and comments on them. There are forms for creating articles, comments and searching for articles.
## Issues and expected updates

The ability to process a form for publishing articles does not work if categories are specified in it. The complexity of the problem is that the creation of an article entry in the database must be preceded by the creation of a category entry. It is also not possible to transfer the selected categories to the view.
More information about the user will appear in the profile.
