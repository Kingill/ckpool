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


How to get mining info

bitcoin-cli -rpcuser= -rpcpassword= getmininginfo
{
  "blocks": 895177,
  "currentblockweight": 3995928,
  "currentblocktx": 3734,
  "difficulty": 119116256505723.5,
  "networkhashps": 8.894282723879657e+20,
  "pooledtx": 5826,
  "chain": "main",
  "warnings": ""
}


difficulty": 119116256505723 (119.1163T, or ~119T).

The node provides block templates with the 119T difficulty target. Your Bitaxe’s bestshare (330M) is tracked in AxeOS, but only a hash ≥119T solves a block.
Your logs (diff: 0.0, bestshare: 330078121) suggest solo mining, where the node assigns the network difficulty, and shares are accepted at a low threshold (~1000) for monitoring.

```
