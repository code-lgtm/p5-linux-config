# fullstack

FullStack Project using Flask Micro framework  

-------------------------------------------------------------------------------  
Setting up and running server:  
   --- Install software using command  
        sudo apt-get install libpq-dev python-dev  
   --- Do a latest chekout from the repsitory: https://github.com/kumaratinfy/fullstack.git  
   --- From shell navigate inside the fullstack folder  
   --- create a virtual environment using the command:  
           virtualenv venv --always-copy --no-site-packages  
           chmod 777 venv  
   --- Activate virtual environemt using the following command  
           source venv/bin/activate  
   --- Export path to successfully install psycopg2  
           export PATH=/usr/bin:"$PATH"  
   --- Install all dependenices using the following command  
           pip install -r requirements.txt  
   --- Upgrade to the new catalog database (database should be present in postgres)  
           python manage.py db upgrade  
   --- Add sample data using the following commands  
           python manage.py shell (You will be inside the python shell)  
           import catalog.sample_data as sample  
           sample.main() (This will add sample data to the database)  
   --- Run server with the following command  
           python manage.py runserver  
             
-------------------------------------------------------------------------------  
  
Available routes:  
1) http://\<servername\>:\<port no\>/login  
2) http://<servername>:<port no>/register  
3) http://<servername>:<port no>/login  
4) http://<servername>:<port no>  
   http://<servername>:<port no>/dashboard  
5) http://<servername>:<port no>/edit/item/<item id>  
6) http://<servername>:<port no>/add/item/<item id>  
7) http://<servername>:<port no>/delete/item/<item id>  
8) http://<servername>:<port no>/api/v1.0/categories/  
9) http://<servername>:<port no>/api/v1.0/category/<category id>  
  
-------------------------------------------------------------------------------  
  
Available logins:  
1) Email : a@b.com Password: test  
2) Email : b@c.com Password: test  
3) Email : c@d.com Password: test  
4) Email : d@e.com Password: test  
5) Email : e@f.com Password: test  
  
