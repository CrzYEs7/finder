# Finder: Car Parts
#### Video Demo:  <URL HERE>

### *Inspiration:*
This project was based of a idea of my friend Gonçalo, that works in the same company as me.

We work in a call center and spend a lot of time looking for references for specific products.<br>
To improve our **time efficiency** he created an **Excel file containing a list of references** that everyone in the company can **contribute to**.

So I had the idea for my final project of the **CS50** course to create an internal website for this purpose.

***
**This projects consists primarily of a web page using (*Flask*) framework.**
**(*SQlite*) that stores some information about car parts.**
***

### How it works?
**Utilization loop** :
* Initial page
  - **Register**: Create and account, as it's internal there's no need for e-mail.
  - **Login**
    - **Homepage**: Search a product by **name**, **partial reference**, **tag(s)**, **manufacturer** and **car brand**.
      - Result: User can add/remove itens from favorite, edit some information or do another search.
    - ***Navigating***:
        - **New Part**: Where they add a new product by filling some fields.
        - **Favourite**: List of the current favorited products, user can remove itens from favorite here.
        - **Logout**: End user session.
            - Back to the initial page;
        - **Light/Dark**: Switch between light or dark mode.
  - **Light/Dark**: Switch between light or dark mode.

### Major choices:
+   **Web framework** : **Flask**.
    I already have some familiarity because of **CS50's** problem sets. And it's simple.

+   **Database** : **Sqlite**.
    Simple, fast, light. More than enough for what i need.

+   **Parse the data from the excel** : **Python**, **pandas**.
    Did a bit of data cleaning and wrote a  script to parse it.

***
### **Files**

### **app.py**
This file is the **Flask** application responsible for the backend logic so<br>
**verything that is server sided happens here.**<br>


**Interaction with the database:**
  - Stores new users information encrypted;
  - Validade users login, password and username;
  - Stores new products;
  - Updates products information;
  - Updates users favorited itens;
  - Get the users search results;
