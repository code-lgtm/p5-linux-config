# fullstack

<b>FullStack Project using Flask Micro framework</b>  
  
-------------------------------------------------------------------------------------------------------  
<b>Server Details:</b>  
Public IP: 52.35.118.167  
Application URL: http://ec2­52­35­118­167.us­west­2.compute.amazonaws.com/   
SSH Port : 2200  
  
-------------------------------------------------------------------------------------------------------  
<b>Setting up server:</b>  
   ---  Following softwares have been installed using command sudp apt-get install <package name>   
        -- libpq-dev    
	-- python-dev  
	-- fail2ban  
	-- apache2  
	-- finger  
	-- glances  
	-- git  
	-- libapache2-mod-wsgi    
	-- postgresql  
	-- postgresql-contrib  
	-- python-pip  
	-- python-virtualenv  
	-- python2.7  
	-- sendmail  
	-- ufw  
	-- unattended-upgrades  
    
  --- Created a new user grader with sudo privileges  
  --- Disabled root ssh login by setting following parameter in the file /etc/ssh/sshd_config  
          PermitRootLogin no  
  --- Changed ssh port to 2200 by changing following parameter in the file /etc/ssh/sshd_config  
          Port 2200  
  --- Configured Uncomplicated Firewall (UFW) to only allow incoming connections from  
         -- SSH (port 2200)    
	 -- http(port 80)  
	 -- NTP(port 123)  
-----------------------------------------------------------------------------------------------------------  
<b>Setting up Apache Server:</b>  
   --- Do a latest chekout from the following repsitory in the home directory /home/grader   
           https://github.com/kumaratinfy/p5-linux-config.git  
   --- From shell navigate inside the folder  
       -- /home/grader/p5-linux-config  
   --- Swicth to root user using the following command sudo -s  
   --- create a virtual environment using the command:  
           virtualenv venv --always-copy --no-site-packages  
   --- Activate virtual environemt using the following command  
           source venv/bin/activate  
   --- Install all dependenices using the following command  
           pip install -r requirements.txt  
   --- Exit to grader user by typing the following command  
       -- exit  
   --- Copy following files and directories recursively in the folder /var/www/fullstack  
       -- catalog  
       -- instance  
       -- migrations  
       -- tests  
       -- catalog.wsgi  
       -- config.py  
       -- manage.py  
       -- requirements.txt  
   --- Move the following folder from /home/grader/p5-linux-config to /var/www/fullstack  
       -- venv  
   --- Copy the following file from /home/grader/pf-linus-config to /etc/apache2/sites-available  
       -- catalog.conf     
  
   --- Upgrade to the new catalog database (database should be present in postgres)  
           python manage.py db upgrade  
   --- Add sample data using the following commands  
           python manage.py shell (You will be inside the python shell)  
           import catalog.sample_data as sample  
           sample.main() (This will add sample data to the database)  
   --- Run server with the following command  
           python manage.py runserver  
             
---------------------------------------------------------------------------------------------------------------  
<b>Setting up Postgres:</b>
  --- Go to psql shell using the following command  
      -- sudo -u postgres psql  
      -- Create a new database catalog  
  --- Create catalog database schema with default data using the following command inside the folder /var/www/fullstack  
      -- sudo -u postgres python manage.py deploy  
  --- Create a new database user 'catalog' using the following command inside psql shell    
      -- sudo -u postgres psql  
      -- CREATE USER catalog WITH PASSWORD <password>;   
  --- GRANT privileges in catalog database using the  following command  
      -- sudo -u postgres psql  
      -- GRANT SELECT, INSERT, UPDATE, DELETE  ON <tablename> TO catalog;  
      -- GRANT SELECT, INSERT  ON <indexes> TO catalog;  
   --- Update connection string in file /var/www/fullstack/instance/application.cfg as follows   
      -- SQLALCHEMY_DATABASE_URI = 'postgresql://catalog:<password>@localhost:5432/catalog'   
      
---------------------------------------------------------------------------------------------------------------  
<b>Running Apache</b>
  ---  Run the following commands to run web site under apache2  
      -- sudo a2dissite 000-default  
      -- sudo a2ensite catalog  
      -- sudo service apache2 reload  
      -- sudo service apache2 restart  
---------------------------------------------------------------------------------------------------------------  
<b>Available routes:</b>  
1) http://\<servername\>:\<port no\>/login  
2) http://\<servername\>:\<port no\>/register  
3) http://\<servername\>:\<port no\>/login  
4) http://\<servername\>:\<port no\>  
   http://\<servername\>:\<port no\>/dashboard  
5) http://\<servername\>:<port no>/edit/item/\<item id\>  
6) http://\<servername\>:\<port no\>/add/item/\<item id\>  
7) http://\<servername\>:\<port no\>/delete/item/\<item id\>  
8) http://\<servername\>:\<port no\>/api/v1.0/categories/  
9) http://\<servername\>:\<port no\>/api/v1.0/category/\<category id\>  
  
---------------------------------------------------------------------------------------------------------------    
<b>Available logins:</b>    
1) Email : a@b.com Password: test  
2) Email : b@c.com Password: test  
3) Email : c@d.com Password: test  
4) Email : d@e.com Password: test  
5) Email : e@f.com Password: test  
  
-----------------------------------------------------------------------------------------------------------------    
<b> Miscellaneous:</b>  
 --- Set up Fail2Ban for disabling a host for 6 consecutive unsuccessful ssh login's.   
     Following changes were made in the file /etc/failban/jail.local  
     -- bantime=1800  
     -- destemail=<My email address>  
     -- mta=sendmail  
     -- action = %(action_mwl)s  
     Enabled following jails for monitoring of apache logs  
     -- apache-overflows  
     -- apache-noscript  
     -- apache-badbots  
     -- apache-nohome  
     -- apache  
  
 --- Installed glances for monitoring application availability status  
 --- Installed and configured unattended-upgrades for automated security patches installation  
  
-----------------------------------------------------------------------------------------------------------------    

