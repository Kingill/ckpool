# CKPool Solo Mining Setup

Welcome to the **CKPool Solo Mining Setup** guide! This document explains how to install and configure **CKPool**, a lightweight Bitcoin mining pool server, to solo mine with a miner like the **Bitaxe** (1.14 TH/s) using a **Bitcoin Core node**. You’ll learn to retrieve the network difficulty (~119T in May 2025) and monitor your mining performance.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running CKPool](#running-ckpool)
- [Monitoring Mining Info](#monitoring-mining-info)
- [Log Management](#log-management)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

## Overview
**CKPool** is a high-performance Bitcoin mining pool server designed for solo or small-scale mining. When paired with a **Bitcoin Core node**, it relays block templates to your miner (e.g., Bitaxe), targeting the network difficulty (~119T). Your Bitaxe’s best share (e.g., 330M) must reach this difficulty to solve a block.

This guide assumes you’re solo mining with a Bitaxe (1.14 TH/s) and a synced Bitcoin node.

## Prerequisites
- **Hardware**:
  - Bitaxe miner (1.14 TH/s, running AxeOS).
  - Linux server (e.g., Ubuntu) for CKPool.
  - Computer running Bitcoin Core (fully synced, ~600 GB storage).
- **Software**:
  - [Bitcoin Core](https://bitcoin.org) (v24.0 or later).
  - Ubuntu or Debian-based OS.
  - Tools: `git`, `bitcoin-cli`, `curl`.
- **Knowledge**:
  - Basic Linux command-line skills.
  - Understanding of Bitcoin mining (difficulty, shares, Stratum protocol).

## Installation
Install CKPool and its dependencies on your Linux server.

1. **Update System**:
   ```bash
   sudo apt update
   sudo apt-get install -y build-essential yasm libzmq3-dev
   ```

2. **Clone CKPool Repository**:
   ```bash
   git clone https://bitbucket.org/ckolivas/ckpool.git
   cd ckpool
   ```

3. **Compile CKPool**:
   ```bash
   ./autogen.sh
   ./configure
   make
   sudo make install
   ```
   - This installs CKPool to `/usr/local/bin/ckpool`.

## Configuration
Set up CKPool to connect your Bitcoin node and Bitaxe.

1. **Create Configuration File**:
   - Create a directory for CKPool:
     ```bash
     mkdir -p ~/ckpool/ckpool-solo
     ```
   - Create `~/ckpool/ckpool-solo/ckpool.conf`:
     ```json
     {
       "btcd": [
         {
           "url": "http://127.0.0.1:8332",
           "auth": "yourusername",
           "pass": "yourpassword"
         }
       ],
       "btcaddress": "your_bitcoin_address",
       "blockpoll": 100,
       "logdir": "/home/ckpool/ckpool-solo/logs",
       "stratumport": 3333
     }
     ```
     - Replace `yourusername` and `yourpassword` with your Bitcoin Core RPC credentials (from `bitcoin.conf`).
     - Replace `your_bitcoin_address` with your Bitcoin wallet address.

2. **Configure Bitcoin Core**:
   - Edit `~/.bitcoin/bitcoin.conf`:
     ```conf
     rpcuser=yourusername
     rpcpassword=yourpassword
     server=1
     rpcallowip=127.0.0.1
     ```
   - Restart Bitcoin Core:
     ```bash
     bitcoin-cli stop
     bitcoind
     ```

3. **Configure Bitaxe**:
   - Access the AxeOS dashboard (`http://[Bitaxe-IP]`).
   - Set pool settings:
     - **Pool URL**: `stratum+tcp://[Server-IP]:3333` (e.g., `stratum+tcp://192.168.1.50:3333`).
     - **Worker**: Your Bitcoin wallet address.
     - **Password**: Any value (e.g., `x`).
   - Save and restart mining.

## Running CKPool
Start CKPool to relay block templates from your node to your Bitaxe.

1. **Run CKPool**:
   ```bash
   /usr/local/bin/ckpool -B -c ~/ckpool/ckpool-solo/ckpool.conf
   ```
   - `-B`: Run in background mode.
   - `-c`: Specify the config file.

2. **Verify Operation**:
   - Check CKPool logs in `~/ckpool/ckpool-solo/logs`.
   - Ensure Bitaxe shows hashrate (~1.14 TH/s) in AxeOS (`http://[Bitaxe-IP]`).

## Monitoring Mining Info
Retrieve the **network difficulty** (~119T) to understand the threshold your Bitaxe must meet to solve a block.

1. **Using bitcoin-cli**:
   ```bash
   bitcoin-cli -rpcuser=yourusername -rpcpassword=yourpassword getmininginfo
   ```
   - Example Output:
     ```json
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
     ```
   - **Difficulty**: `119116256505723.5` (~119.12T) is the target your Bitaxe’s hash must meet to solve a block.

2. **Using Python**:
   ```
   python3 -m venv ~/bitcoin-venv
   source ~/bitcoin-venv/bin/activate
   pip3 install python-dotenv
   pip3 install simplejson
   pip3 install python-bitcoinrpc
   
   /home/bitcoin/difficulty.py  
   ```
   - Output: `Network Difficulty: 119.12T`.
   - Raw mining_info: `{'blocks': 895189, 'currentblockweight': 3995574, 'currentblocktx': 636, 'difficulty': 119116256505723.5, 'networkhashps': 8.722632117999069e+20, 'pooledtx': 789, 'chain': 'main', 'warnings': ''}`.

## Best Share Info
1. **Using Python**:
   ```
   /home/ckpool/extract_bestshare.py.py  
   ```
   - Latest bestshare: `330078121`   

## Log Management
Prevent CKPool logs from growing too large.

1. **Create Purge Script**:
   - Create `~/ckpool/ckpool-solo/purge_ckpool_log.sh`:
     

2. **Schedule Purge**:
   - Edit crontab:
     ```bash
     sudo crontab -e
     ```
   - Add:
     ```
     0 0 * * * /home/ckpool/ckpool-solo/purge_ckpool_log.sh
     ```
   - This deletes logs older than 7 days at midnight daily.

## Troubleshooting
- **Node Not Synced**:
  - Run `bitcoin-cli getblockchaininfo`. Ensure `"initialblockdownload": false`.
- **CKPool Not Starting**:
  - Verify `ckpool.conf` (correct RPC credentials, Bitcoin address).
  - Check logs in `~/ckpool/ckpool-solo/logs`.
- **Bitaxe Not Connecting**:
  - Confirm Wi-Fi stability and correct Stratum URL in AxeOS.
  - Test: `telnet [Server-IP] 3333`.
- **Low Best Share**:
  - Normal for 1.14 TH/s (e.g., 330M). Solving a block (~119T) is rare (~32-year average).
- **High Share Rejections**:
  - Your logs show 0.029% rejection rate (excellent). If higher, check network latency or pool settings.

## Resources
- **CKPool**:
  - [Bitbucket Repository](https://bitbucket.org/ckolivas/ckpool)
  - [CKPool Documentation](https://bitbucket.org/ckolivas/ckpool/src/master/README)
- **Bitaxe**:
  - [Bitaxe.org](https://bitaxe.org)
  - [ESP-Miner GitHub](https://github.com/bitaxeorg/ESP-Miner)
- **Bitcoin Core**:
  - [Bitcoin.org](https://bitcoin.org)
  - [RPC Documentation](https://developer.bitcoin.org/reference/rpc)
- **Mining Data**:
  - [Mempool.space](https://mempool.space)
  - [CoinWarz](https://coinwarz.com)

---

Happy solo mining! For issues, check the [CKPool Bitbucket](https://bitbucket.org/ckolivas/ckpool) or [Bitaxe community](https://bitaxe.org).
