![tdc Logo](/src/tdc.png)


# Twitter data collection
This project is a aplication that allows you to read information on Twitter in real time. 
From a #hashtag, you can see all the users who have written a tweet with that hashtag and see the relationships between those different users.

* __Final degree project__
This project is part to the final degree project of software Engineering in University Rey Juan Carlos of Madrid.

* __Author:__
  * **Eloy Alfageme Galeano** [@ealfageme] (https://github.com/ealfageme)  
  Contact: e.alfageme@alumnos.urjc.es
  Contact: eloyaliseda@gmail.com

* __Prerequisites:__
  * Python 2.7.14 or higher
  * Neo4j 3.2.2 or higher
  
 * __Tecnhologies:__
  * Django Framework
  * Neo4j
  * Tweepy Library
  * HTML5/CSS3/JS
  * D3JS
## How I run the project
 * Downoload the project using 
   ```
   git clone 
   ```
 * Launch the database using
 ```
 ./bin/neo4j start
 ```
 to stop:
 ```
 ./bin/neo4j stop
 ```
 * Launch the app:
 ```
  python manage.py runserver
 ```
 ## Example of use
 ![home](/src/index.png)
 ![graph](/src/grafo1.png)
