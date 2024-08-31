**QuizMaster**
The project consolidates individual solutions into a unified system that allows administrators to create and manage quizzes with various question types.

**Key Features**
Admin Capabilities: Create, approve, or delete quizzes and individual questions. Administrators can review user quizzes and provide feedback with saved correct answers.
User Interaction: Users cannot view their quiz results until they are approved by an administrator.
Security & Feedback: Includes XSS, CSRF, and SQL Injection protections, with feedback mechanisms based on stored correct answers.

**Network address and login information**

Username and password in the database

In the attached SQL script that generates the database, two users have been added: one with administrator privileges and one regular user.

**Admin:**

E-mail: admin@uit.no

Password: 123456


**Normal User:**

E-mail: bruker@uit.no

password: 123456



**Project Structure**

![image](https://github.com/user-attachments/assets/b02bf238-47f9-4597-b663-21d833dade52)

app.py: Initializes the Flask application, manages user authentication with Flask-Login, and handles routing.
models/: Contains database classes and queries, managing connections and CRUD operations.
static/: Holds JavaScript and CSS files for frontend interactivity and styling.
templates/: Contains HTML templates, with Jinja2 for dynamic content rendering.
utils/: Provides utility functions for form validation and CSRF token checks.
views/: Manages application routing, user interaction, and admin functionalities.

**Improvements & Future Work**
Implement confirmation dialogs for deletions to avoid accidental data loss.
Add pagination to handle large sets of quizzes and improve system performance.

**Contributors**
Madeleine Randine Woodbury (mwo030@uit.no)
Said Nasser Said (ssa171@uit.no)
