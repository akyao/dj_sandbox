
PROJECT = "dj_sandbox"
APP = "cron_table"

VENV_DIR="/var/venv"
VENV_PATH="/var/venv/env27"

PYTHON = VENV_PATH

execute "yum groupinstall -y 'Development Tools'"

# fuck selinux
execute "selinux is kuso" do
  user "root"
  command "setenforce 0"
  only_if "getenforce | grep Enforcing"
end

file "/etc/selinux/config" do
  action :edit
  user "root"
  block do |content|
    content.gsub!("SELINUX=enforcing", "SELINUX=disabled")
  end
  only_if "test -e /etc/selinux/config"
end

package "bzip2-devel"
package "openssl-devel"
package "ncurses-devel"
package "sqlite-devel"
package "readline-devel"
#package "tk-devel"
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


execute "install python 2.7" do
  command "wget http://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz;
            tar -xzvf Python-2.7.9.tgz;
            cd Python-2.7.9;
            ./configure --enable-shared;
            make;
            sudo make install;
            ln -s /usr/local/lib/libpython2.7.so.1.0 /lib64/"
  not_if "ls /lib64 | grep python2.7"
end

execute "pip" do
  command "wget https://bootstrap.pypa.io/get-pip.py;
            /usr/local/bin/python get-pip.py"
  not_if "pip --version | grep pip"
end

execute "virtualenv" do
  command "/usr/local/bin/pip install virtualenv"
  #user "#{node[:user]}"
  not_if "which virtualenv | grep virtualenv"
end

directory "create virtualenv dir" do
  action :create
  path "#{VENV_DIR}"
  mode "777"
  owner "#{node[:user]}"
  group "#{node[:user]}"
end

execute "setting virtualenv" do
  command "cd #{VENV_DIR} ;/usr/local/bin/virtualenv env27 --python=/usr/local/bin/python2.7"
  user "#{node[:user]}"
  not_if "test -e #{VENV_PATH}"
end

execute "activate venv" do
  command "source #{VENV_PATH}/bin/activate"
end

execute "django install" do
  command "source #{VENV_PATH}/bin/activate &&
            pip install Django==1.8.2"
  user "#{node[:user]}"
  not_if "test -e #{VENV_PATH}/bin/django-admin"
end

execute "wsgi down" do
  command "wget http://modwsgi.googlecode.com/files/mod_wsgi-3.3.tar.gz;
            tar xvfz mod_wsgi-3.3.tar.gz"
  not_if "test -e mod_wsgi-3.3"
end

execute "wsgi install" do
  command "cd mod_wsgi-3.3;
            ./configure --with-apxs=/usr/sbin/apxs --with-python=#{VENV_PATH}/bin/python2.7;
            make;
            sudo make install"
  not_if "test -e /etc/httpd/modules/mod_wsgi.so"
end

execute "wsgi setting1" do
  user "root"
  command "echo '/usr/local/lib' >> /etc/ld.so.conf; ldconfig"
  not_if "grep '/usr/local/lib' /etc/ld.so.conf"
end

package 'http://dev.mysql.com/get/mysql-community-release-el6-5.noarch.rpm' do
  not_if 'rpm -q mysql-community-release-el6-5'
end

package 'mysql-server'
package 'mysql-devel'

execute "install python-mysql" do
  command "source #{VENV_PATH}/bin/activate &&
            pip install MySQL-python"
  not_if "#{VENV_PATH}/bin/pip/ list | grep MySQL-python"
end

template "/etc/httpd/conf.d/wsgi.conf" do
  action :create
  source "wsgi_conf.erb"
  mode   "644"
  owner  "root"
  group  "root"
  variables(proj: PROJECT, app: APP, python: PYTHON)
end


execute "httpd setting" do
  command "mkdir /var/www/html/dummy;
            ln -s /var/www/html/dummy /var/www/html/#{PROJECT}"
  not_if "test -e /var/www/html/#{PROJECT}"
end

service 'mysqld' do
  action [:enable, :start]
end

service 'httpd' do
  user "root"
  action [:enable, :start]
end

directory "create work dir" do
  action :create
  path "/home/#{node[:user]}/work"
  mode "777"
  owner "#{node[:user]}"
  group "#{node[:user]}"
end

require 'securerandom'
file "create secret key file" do
  path "/var/www/html/secret"
  action :create
  content "#{SecureRandom.base64(50)}"
  mode "744"
  owner "#{node[:user]}"
  group "#{node[:user]}"
  not_if "test -e /var/www/html/secret"
end

execute "mysql -uroot -e \"CREATE DATABASE if not exists dj_sandbox CHARACTER SET utf8;\""
execute "mysql -uroot -e \"GRANT ALL ON dj_sandbox.* to dj_sandbox@localhost;\""
execute "mysql -uroot -e \"FLUSH PRIVILEGES;\""
