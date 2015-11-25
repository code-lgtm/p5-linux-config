# fullstack

Setting up server:
   --- Install software using command
        sudo apt-get install libpq-dev python-dev
   --- Do a latest chekout from the reposiroty: https://github.com/kgaurav7/codellect.git
   --- From shell navigate inside the codellect folder
   --- create a virtual environment using the command: 
           virtualenv venv --always-copy --no-site-packages
           chmod 777 virtualenv
   --- Activate virtual environemt using the following command
           source venv/bin/activate
   --- Export path to successfully install psycopg2
           export PATH=/usr/bin:"$PATH"
   --- Install all dependenices using the following command (Try with sudo if you get permissions errors)
           pip install -r requirements.txt
   --- Upgrade to the new database (database should be present in postgres)
           python manage.py db upgrade
   --- Add sample data using the following commands
           python manage.py shell (You will be inside the python shell)
           import app.sample_data as sample
           sample.main() (This will add sample data to the database)
   --- Run server with the following command
           python manage.py runserver
          
--------------------------------------------------------------------------------------------------------------------------
Additional Required Packages:
1) pip install enum34

