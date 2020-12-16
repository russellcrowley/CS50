MINIMEALS README

PROJECT SUMMARY: A web app that allows parents to log and review the meals their toddler is eating, after seeing several posts online by parents bemoaning the lack of a program that does this. The resulting project is the start of a response to this problem, with the intention that it provides a quick and easy way for a user to log meals that theirchild is eating, as well as how much they've eaten and their enjoyment. 

TECHNOLOGIES USED
-Flask/Python
-Bootstrap
-HTML
-CSS

MY LEARNING
-Databases - this is my first relational database created from scratch, and uses several different tables to allow a list of dishes and ingredients that can be used by users collectively, with the intention that the database becomes more comprehensive with more users
-Bootstrap - I haven't used this library before
-Passing vraiables to HTML/Jinja - I was particulary stuck on incrporating the results from two separate tables in a loop (meals and dishes on the 'review page;), but found I could achieve the desired effect by zipping the sqlite3.row objects together

NEXT STEPS
There are plenty of further developments and functionality I can add to minimeals, auch as:
-Improved date formatting
-Exploring more streamlined ways to add meals and dishes
-Customisable review filters (e.g. finding ingredientd the child likes to eat)
-Introducing algorithms which can try to identify common ingredients that may be influencing the child's behaviour that the parent may not be aware of 
-A 'contact us' page that allows an email to be set through a form
-An 'about' page
