# ckpool

```
Installation
sudo apt update
sudo apt-get install build-essential yasm libzmq3-dev


git clone https://bitbucket.org/ckolivas/ckpool/src/master/
cd master

=> Compiler 
./autogen.sh
./configure
make
sudo make install

/usr/local/bin/ckpool -B -c ~/ckpool/ckpool-solo/ckpool.conf


Purge
sudo crontab -e
0 0 * * * /home/ckpool/ckpool-solo/purge_ckpool_log.sh
```
