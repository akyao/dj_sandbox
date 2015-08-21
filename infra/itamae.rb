
PROJECT = "project"
APP = "app"
PYTHON = "/home/vagrant/venv/env27"

execute "yum groupinstall -y 'Development Tools'"

package "bzip2-devel"
package "openssl-devel"
package "ncurses-devel"
package "sqlite-devel"
package "readline-devel"
package "tk-devel"
package "gdbm-devel"
package "db4-devel"
package "libpcap-devel"
package "xz-devel"

package "libjpeg-devel"
package "zlib-devel"
package "git"
package "httpd"
package "httpd-devel"
package "python-devel"


execute "install python 2.7.6" do
  command "wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz;tar -xzvf Python-2.7.6.tgz;cd Python-2.7.6;./configure --enable-shared;make;make install;ln -s /usr/local/lib/libpython2.7.so.1.0 /lib64/"
  not_if "ls /lib64 | grep python2.7"
end

execute "pip" do
  command "wget https://bootstrap.pypa.io/get-pip.py;/usr/local/bin/python get-pip.py"
  not_if "pip --version | grep pip"
end

execute "pwd"
execute "whoami"

execute "virtualenv" do
  command "/usr/local/bin/pip install virtualenv"
  not_if "which virtualenv | grep virtualenv"
end

execute "setting virtualenv" do
  command "mkdir venv; cd venv; /usr/local/bin/virtualenv env27 --python=/usr/local/bin/python2.7"
  not_if "test -e venv/env27"
end

execute "activate venv" do
  command "cd venv/env27; source bin/activate"
end

execute "wsgi down" do
  command "wget http://modwsgi.googlecode.com/files/mod_wsgi-3.3.tar.gz; tar xvfz mod_wsgi-3.3.tar.gz"
  not_if "test -e mod_wsgi-3.3"
end

execute "wsgi install" do
  command "cd mod_wsgi-3.3; sudo ./configure --with-apxs=/usr/sbin/apxs --with-python=/usr/local/bin/python2.7; sudo make; sudo make install"
  not_if "test -e /etc/httpd/modules/mod_wsgi.so"
end

execute "wsgi setting1" do
  command "echo '/usr/local/lib' >> /etc/ld.so.conf"
  not_if "grep '/usr/local/lib' /etc/ld.so.conf"
end

template "/etc/httpd/conf.d/wsgi.conf" do
  action :create
  source "wsgi_conf.erb"
  mode   "644"
  owner  "root"
  group  "root"
  variables(proj: PROJECT, app: APP, python: PYTHON)
end

execute "django install" do
  command "/usr/local/bin/pip install Django==1.8.2"
  not_if "test -e /usr/bin/django-admin"
end

execute "httpd setting" do
  command "sudo mkdir /var/www/html/dummy;sudo ln -s /var/www/html/dummy /var/www/html/#{PROJECT}"
  not_if "test -e /var/www/html/#{PROJECT}"
end

package 'http://dev.mysql.com/get/mysql-community-release-el6-5.noarch.rpm' do
  not_if 'rpm -q mysql-community-release-el6-5'
end

package 'mysql-community-server'
package 'mysql-community-devel'

service 'mysqld' do
  action [:enable, :start]
end

# user
# execute "mysql -uroot -e \"DELETE FROM mysql.user WHERE User='';\""
# execute "mysql -uroot -e \"DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');\""
# execute "mysql -uroot -e \"DROP DATABASE test;\"; echo"
# execute "mysql -uroot -e \"DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%'\""
# execute "mysql -uroot -e \"FLUSH PRIVILEGES;\""

execute "mysql -uroot -e \"CREATE DATABASE if not exists sandbox CHARACTER SET utf8;\""
execute "mysql -uroot -e \"GRANT ALL ON sandbox.* to sandbox@localhost;\""
execute "mysql -uroot -e \"FLUSH PRIVILEGES;\""
