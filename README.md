CKPool
CKPool is a high-performance Bitcoin mining pool server and proxy software. It supports solo mining, proxy, passthrough, and redirector modes, with flexible configuration options and minimal dependencies.
Building
Dependencies
CKPool requires:

Basic build tools
yasm
Optional: libzmq3-dev for ZMQ notification support (CKPool only)

Build Instructions
With ZMQ (preferred for CKPool, not required for CKProxy):
sudo apt-get install build-essential yasm libzmq3-dev
./configure
make

Basic Build (without ZMQ):
sudo apt-get install build-essential yasm
./configure
make

Building from Git:
Requires additional tools: autoconf, automake, and pkgconf.
sudo apt-get install build-essential yasm autoconf automake libtool libzmq3-dev pkgconf
./autogen.sh
./configure
make

Output
Binaries are generated in the src/ subdirectory:

ckpool: Main pool backend
ckproxy: Proxy mode link
ckpmsg: Messaging utility for CKPool
notifier: Block change notification for bitcoind

Installation
Installation is optional; CKPool can run directly from the build directory. To install:
sudo make install

Running
CKPool supports several command-line options:



Option
Description



-B, --btcsolo
Start in BTCSOLO mode for solo mining; usernames must be valid Bitcoin addresses.


-c CONFIG, --config CONFIG
Specify custom configuration file (defaults: ckpool.conf, ckproxy.conf, ckpassthrough.conf, ckredirector.conf).


-g GROUP, --group GROUP
Run as specified group ID.


-H, --handover
Take over client socket from a running CKPool instance with the same name.


-h, --help
Display help message.


-k, --killold
Shut down existing CKPool instance with the same name.


-L, --log-shares
Log per-share data by block height and workbase.


-l LOGLEVEL, --loglevel LOGLEVEL
Set log level (default: 5, max debug: 7).


-N, --node
Start in passthrough node mode with local bitcoind.


-n NAME, --name NAME
Set process name for multiple instances (defaults: ckpool, ckproxy, ckpassthrough, ckredirector, cknode).


-P, --passthrough
Start in passthrough proxy mode, streaming to an upstream pool.


-p, --proxy
Start in proxy mode, presenting shares as a single user to an upstream CKPool.


-R, --redirector
Start in redirector mode, filtering inactive users and redirecting to configured pools.


-s SOCKDIR, --sockdir SOCKDIR
Set directory for communication sockets (default: /tmp).


-u, --userproxy
Proxy mode with per-user upstream connections using provided credentials.


ckpmsg and notifier support -n, -p, and -s options.
Configuration
CKPool uses a JSON-encoded configuration file (ckpool.conf or ckproxy.conf by default). Sample configurations are included in the source.
Key Configuration Options



Option
Description



btcd
Array of bitcoind(s) with url, auth, pass, and optional notify (for notifier). Defaults to `localhost:

