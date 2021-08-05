#!/bin/bash
sudo yum update -y
sudo yum install -y mysql httpd
sudo amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
sudo service httpd start
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz
cd wordpress
cp wp-config-sample.php wp-config.php
sudo cp -r /wordpress/* /var/www/html/
sudo service httpd restart
