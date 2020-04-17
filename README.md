#### List Of server ####

    192.168.3.31    redis01        a_master:6379    c_slave:6381
    192.168.3.32    redis02        b_master:6380    a_slave:6379
    192.168.3.33    redis03        c_master:6381    b_slave:6380


#### Install Redis ####

sudo yum install make gcc libc6-dev tcl screen telnet zlib zlib-devel readline readline-devel  
wget http://download.redis.io/releases/redis-4.0.4.tar.gz  
tar xvzf redis-4.0.4.tar.gz  
mv redis-4.0.4 redis  
cd redis  
sudo make install  
make test


#### Create config file ####
For all instance of redis change the port, pidfile, cluster-config-file, dir value accordingly  
vi /redis/a_master.conf  
##############################################################  
bind 0.0.0.0  
protected-mode no  
port 6379  
pidfile /var/run/redis_6379.pid  
cluster-enabled yes  
cluster-config-file nodes-6379.conf  
cluster-node-timeout 15000  
#Make sure following properties are added in each conf file  
  appendonly yes  
  save 900 1  
  save 300 10  
  save 60 10000  
  dir /home/vagrant/a_master/  
##############################################################  
start two redis instance in redis01 node:  

screen -U -S a_master

redis-server a_master.conf

Ctrl+a+d

screen -U -S c_slave

redis-server c_slave.conf

Ctrl+a+d

#### Install Ruby ####

wget https://cache.ruby-lang.org/pub/ruby/2.2/ruby-2.2.4.tar.gz  
tar -zxvf ruby-2.2.4.tar.gz  
cd ruby-2.2.4  
./configure  
make  
sudo make install  

#### Install gem ####

wget https://rubygems.org/rubygems/rubygems-2.4.8.tgz --no-check-certificate  
tar -xvzf rubygems-2.4.8.tgz  
cd rubygems-2.4.8  
sudo /usr/local/bin/ruby setup.rb config && sudo /usr/local/bin/ruby setup.rb setup && sudo /usr/local/bin/ruby setup.rb install  

#### Install redis gem ####

wget https://rubygems.org/downloads/redis-4.1.0.gem  
sudo /usr/local/bin/gem install redis-4.1.1.gem  

#### Cluster Setup ####  
#### Add Master ####  
cd redis/src  
./redis-trib.rb create 192.168.3.31:6379 192.168.3.32:6380 192.168.3.33:6381  

#### Add Slave ####  
./redis-trib.rb add-node --slave --master-id 7f46599d998e24b8eb07513eb525b90f9b0488e3 192.168.3.32:6379 192.168.3.31:6379  
./redis-trib.rb add-node --slave --master-id c8bd0b335a3f75619163f42a77b2257a16dca1c1 192.168.3.33:6380 192.168.3.32:6380  
./redis-trib.rb add-node --slave --master-id 89c4b22476c10ba54840fd5e3fe920a5c72fed72 192.168.3.31:6381 192.168.3.33:6381  

#### To backup Redis data ####

cp /home/vagrant/a_master/dump.rdb /home/vagrant/a_master/backup/dump_$(date +\%Y\%m\%d\%H\%M\%S).rdb  
cp /home/vagrant/a_master/appendonly.aof /home/vagrant/a_master/backup/appendonly_$(date +\%Y\%m\%d\%H\%M\%S).aof  
cp /home/vagrant/c_slave/dump.rdb /home/vagrant/c_slave/backup/dump_$(date +\%Y\%m\%d\%H\%M\%S).rdb  
cp /home/vagrant/c_slave/appendonly.aof /home/vagrant/c_slave/backup/appendonly_$(date +\%Y\%m\%d\%H\%M\%S).aof  

cp /home/vagrant/b_master/dump.rdb /home/vagrant/b_master/backup/dump_$(date +\%Y\%m\%d\%H\%M\%S).rdb  
cp /home/vagrant/b_master/appendonly.aof /home/vagrant/b_master/backup/appendonly_$(date +\%Y\%m\%d\%H\%M\%S).aof  
cp /home/vagrant/a_slave/dump.rdb /home/vagrant/a_slave/backup/dump_$(date +\%Y\%m\%d\%H\%M\%S).rdb  
cp /home/vagrant/a_slave/appendonly.aof /home/vagrant/a_slave/backup/appendonly_$(date +\%Y\%m\%d\%H\%M\%S).aof  

cp /home/vagrant/c_master/dump.rdb /home/vagrant/c_master/backup/dump_$(date +\%Y\%m\%d\%H\%M\%S).rdb  
cp /home/vagrant/c_master/appendonly.aof /home/vagrant/c_master/backup/appendonly_$(date +\%Y\%m\%d\%H\%M\%S).aof  
cp /home/vagrant/b_slave/dump.rdb /home/vagrant/b_slave/backup/dump_$(date +\%Y\%m\%d\%H\%M\%S).rdb  
cp /home/vagrant/b_slave/appendonly.aof /home/vagrant/b_slave/backup/appendonly_$(date +\%Y\%m\%d\%H\%M\%S).aof  

#### To Restore #####

1. Stop all redis instance  
2. Rename the existing dump.rdb and appendonly.aof  
3. mv backed up data to data directory.  
4. Start all redis instance.  


#### To insert data ####

sudo pip install redis-py-cluster  

then run below command  

python data.py  

#### To view/delete/save data ####

python get-data.py  



