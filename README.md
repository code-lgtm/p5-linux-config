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
   &nbsp;&nbsp; -- libpq-dev    
   &nbsp;&nbsp;	-- python-dev  
   &nbsp;&nbsp;	-- fail2ban  
   &nbsp;&nbsp;	-- apache2  
   &nbsp;&nbsp;	-- finger  
   &nbsp;&nbsp;	-- glances  
   &nbsp;&nbsp;	-- git  
   &nbsp;&nbsp;	-- libapache2-mod-wsgi    
   &nbsp;&nbsp;	-- postgresql  
   &nbsp;&nbsp;	-- postgresql-contrib  
   &nbsp;&nbsp;	-- python-pip  
   &nbsp;&nbsp;	-- python-virtualenv  
   &nbsp;&nbsp;	-- python2.7  
   &nbsp;&nbsp;	-- sendmail  
   &nbsp;&nbsp;	-- ufw  
   &nbsp;&nbsp;	-- unattended-upgrades  
    
  --- Created a new user grader with sudo privileges  
  --- Disabled root ssh login by setting following parameter in the file /etc/ssh/sshd_config  
          &nbsp;&nbsp;&nbsp;&nbsp;PermitRootLogin no  
  --- Changed ssh port to 2200 by changing following parameter in the file /etc/ssh/sshd_config  
          &nbsp;&nbsp;&nbsp;&nbsp;Port 2200  
  --- Configured Uncomplicated Firewall (UFW) to only allow incoming connections from  
         &nbsp;&nbsp;&nbsp;&nbsp;-- SSH (port 2200)    
	 &nbsp;&nbsp;&nbsp;&nbsp;-- http(port 80)  
	 &nbsp;&nbsp;&nbsp;&nbsp;-- NTP(port 123)  
-----------------------------------------------------------------------------------------------------------  
<b>Setting up Apache Server:</b>  
   &nbsp;&nbsp;--- Do a latest chekout from the following repsitory in the home directory /home/grader   
           &nbsp;&nbsp;&nbsp;&nbsp;https://github.com/kumaratinfy/p5-linux-config.git  
   &nbsp;&nbsp;--- From shell navigate inside the folder  
       &nbsp;&nbsp;&nbsp;&nbsp;-- /home/grader/p5-linux-config  
   &nbsp;&nbsp;--- Swicth to root user using the following command sudo -s  
   &nbsp;&nbsp;--- create a virtual environment using the command:  
           &nbsp;&nbsp;&nbsp;&nbsp;virtualenv venv --always-copy --no-site-packages  
   &nbsp;&nbsp;--- Activate virtual environemt using the following command  
           &nbsp;&nbsp;&nbsp;&nbsp;source venv/bin/activate  
   &nbsp;&nbsp;--- Install all dependenices using the following command  
           &nbsp;&nbsp;&nbsp;&nbsp;pip install -r requirements.txt  
   &nbsp;&nbsp;--- Exit to grader user by typing the following command  
       &nbsp;&nbsp;&nbsp;&nbsp;-- exit  
   &nbsp;&nbsp;--- Copy following files and directories recursively in the folder /var/www/fullstack  
       &nbsp;&nbsp;&nbsp;&nbsp;-- catalog  
       &nbsp;&nbsp;&nbsp;&nbsp;-- instance  
       &nbsp;&nbsp;&nbsp;&nbsp;-- migrations  
       &nbsp;&nbsp;&nbsp;&nbsp;-- tests  
       &nbsp;&nbsp;&nbsp;&nbsp;-- catalog.wsgi  
       &nbsp;&nbsp;&nbsp;&nbsp;-- config.py  
       &nbsp;&nbsp;&nbsp;&nbsp;-- manage.py  
       &nbsp;&nbsp;&nbsp;&nbsp;-- requirements.txt  
   &nbsp;&nbsp;--- Move the following folder from /home/grader/p5-linux-config to /var/www/fullstack  
       &nbsp;&nbsp;&nbsp;&nbsp; -- venv  
   &nbsp;&nbsp;--- Copy the following file from /home/grader/pf-linus-config to /etc/apache2/sites-available  
       &nbsp;&nbsp;&nbsp;&nbsp; -- catalog.conf       
---------------------------------------------------------------------------------------------------------------  
<b>Setting up Postgres:</b>
  &nbsp;&nbsp;--- Go to psql shell using the following command  
      &nbsp;&nbsp;&nbsp;&nbsp;-- sudo -u postgres psql  
      &nbsp;&nbsp;&nbsp;&nbsp;-- Create a new database catalog  
  &nbsp;&nbsp;--- Create catalog database schema with default data using the following command inside the folder /var/www/fullstack  
      &nbsp;&nbsp;&nbsp;&nbsp;-- sudo -u postgres python manage.py deploy  
  &nbsp;&nbsp;--- Create a new database user 'catalog' using the following command inside psql shell    
      &nbsp;&nbsp;&nbsp;&nbsp;-- sudo -u postgres psql  
      &nbsp;&nbsp;&nbsp;&nbsp;-- CREATE USER catalog WITH PASSWORD <password>;   
  &nbsp;&nbsp;--- GRANT privileges in catalog database using the  following command  
      &nbsp;&nbsp;&nbsp;&nbsp;-- sudo -u postgres psql  
      &nbsp;&nbsp;&nbsp;&nbsp;-- GRANT SELECT, INSERT, UPDATE, DELETE  ON <tablename> TO catalog;  
      &nbsp;&nbsp;&nbsp;&nbsp;-- GRANT SELECT, INSERT  ON <indexes> TO catalog;  
   &nbsp;&nbsp;--- Update connection string in file /var/www/fullstack/instance/application.cfg as follows   
      &nbsp;&nbsp;&nbsp;&nbsp;-- SQLALCHEMY_DATABASE_URI = 'postgresql://catalog:<password>@localhost:5432/catalog'   
      
---------------------------------------------------------------------------------------------------------------  
<b>Running Apache</b>
  &nbsp;&nbsp;---  Run the following commands to run web site under apache2  
      &nbsp;&nbsp;&nbsp;&nbsp;-- sudo a2dissite 000-default  
      &nbsp;&nbsp;&nbsp;&nbsp;-- sudo a2ensite catalog  
      &nbsp;&nbsp;&nbsp;&nbsp;-- sudo service apache2 reload  
      &nbsp;&nbsp;&nbsp;&nbsp;-- sudo service apache2 restart  
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
 &nbsp;&nbsp;--- Set up Fail2Ban for disabling a host for 6 consecutive unsuccessful ssh login's.   
     &nbsp;&nbsp;&nbsp;&nbsp;Following changes were made in the file /etc/failban/jail.local  
     &nbsp;&nbsp;&nbsp;&nbsp;-- bantime=1800  
     &nbsp;&nbsp;&nbsp;&nbsp;-- destemail=<My email address>  
     &nbsp;&nbsp;&nbsp;&nbsp;-- mta=sendmail  
     &nbsp;&nbsp;&nbsp;&nbsp;-- action = %(action_mwl)s  
     &nbsp;&nbsp;&nbsp;&nbsp;Enabled following jails for monitoring of apache logs  
     &nbsp;&nbsp;&nbsp;&nbsp;-- apache-overflows  
     &nbsp;&nbsp;&nbsp;&nbsp;-- apache-noscript  
     &nbsp;&nbsp;&nbsp;&nbsp;-- apache-badbots  
     &nbsp;&nbsp;&nbsp;&nbsp;-- apache-nohome  
     &nbsp;&nbsp;&nbsp;&nbsp;-- apache  
  
 &nbsp;&nbsp;--- Installed glances for monitoring application availability status  
 &nbsp;&nbsp;--- Installed and configured unattended-upgrades for automated security patches installation  
  
-----------------------------------------------------------------------------------------------------------------    

