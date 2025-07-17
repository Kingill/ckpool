```markdown
# CKPool

CKPool is a high-performance Bitcoin mining pool server and proxy software. It supports solo mining, proxy, passthrough, and redirector modes, with flexible configuration options and minimal dependencies.

## Building

### Dependencies
CKPool requires:
- Basic build tools
- `yasm`
- Optional: `libzmq3-dev` for ZMQ notification support (CKPool only)

### Build Instructions

#### With ZMQ (preferred for CKPool, not required for CKProxy):
```bash
sudo apt-get install build-essential yasm libzmq3-dev
./configure
make
```

#### Basic Build (without ZMQ):
```bash
sudo apt-get install build-essential yasm
./configure
make
```

#### Building from Git:
Requires additional tools: `autoconf`, `automake`, and `pkgconf`.
```bash
sudo apt-get install build-essential yasm autoconf automake libtool libzmq3-dev pkgconf
./autogen.sh
./configure
make
```

### Output
Binaries are generated in the `src/` subdirectory:
- `ckpool`: Main pool backend
- `ckproxy`: Proxy mode link
- `ckpmsg`: Messaging utility for CKPool
- `notifier`: Block change notification for bitcoind

### Installation
Installation is optional; CKPool can run directly from the build directory. To install:
```bash
sudo make install
```

## Running

CKPool supports several command-line options:

| Option | Description |
|--------|-------------|
| `-B`, `--btcsolo` | Start in BTCSOLO mode for solo mining; usernames must be valid Bitcoin addresses. |
| `-c CONFIG`, `--config CONFIG` | Specify custom configuration file (defaults: `ckpool.conf`, `ckproxy.conf`, `ckpassthrough.conf`, `ckredirector.conf`). |
| `-g GROUP`, `--group GROUP` | Run as specified group ID. |
| `-H`, `--handover` | Take over client socket from a running CKPool instance with the same name. |
| `-h`, `--help` | Display help message. |
| `-k`, `--killold` | Shut down existing CKPool instance with the same name. |
| `-L`, `--log-shares` | Log per-share data by block height and workbase. |
| `-l LOGLEVEL`, `--loglevel LOGLEVEL` | Set log level (default: 5, max debug: 7). |
| `-N`, `--node` | Start in passthrough node mode with local bitcoind. |
| `-n NAME`, `--name NAME` | Set process name for multiple instances (defaults: `ckpool`, `ckproxy`, `ckpassthrough`, `ckredirector`, `cknode`). |
| `-P`, `--passthrough` | Start in passthrough proxy mode, streaming to an upstream pool. |
| `-p`, `--proxy` | Start in proxy mode, presenting shares as a single user to an upstream CKPool. |
| `-R`, `--redirector` | Start in redirector mode, filtering inactive users and redirecting to configured pools. |
| `-s SOCKDIR`, `--sockdir SOCKDIR` | Set directory for communication sockets (default: `/tmp`). |
| `-u`, `--userproxy` | Proxy mode with per-user upstream connections using provided credentials. |

`ckpmsg` and `notifier` support `-n`, `-p`, and `-s` options.

## Configuration

CKPool uses a JSON-encoded configuration file (`ckpool.conf` or `ckproxy.conf` by default). Sample configurations are included in the source.

### Key Configuration Options
| Option | Description |
|--------|-------------|
| `btcd` | Array of bitcoind(s) with `url`, `auth`, `pass`, and optional `notify` (for notifier). Defaults to `localhost:8332`, `user`, `pass`. |
| `proxy` | Array of upstream pool(s) for proxy/passthrough mode (mandatory). |
| `btcaddress` | Bitcoin address for block rewards (ignored in BTCSOLO mode). |
| `btcsig` | Optional coinbase signature. |
| `blockpoll` | Block check frequency (ms, default: 100). Used if `notify` is unset. |
| `donation` | Optional developer donation percentage (default: 0). |
| `nodeserver` | IPs/ports for mining node communications. |
| `nonce1length` | Extranonce1 length (2–8, default: 4). |
| `nonce2length` | Extranonce2 length (2–8, default: 8). |
| `update_interval` | Stratum update frequency (seconds, default: 30). |
| `version_mask` | Bits clients can alter in version number (hex, default: `1fffe000`). |
| `serverurl` | IPs/ports to bind (default: all interfaces, port 3333 for pool, 3334 for proxy). |
| `redirecturl` | URLs for redirector mode. |
| `mindiff` | Minimum vardiff (default: 1). |
| `startdiff` | Starting vardiff (default: 42). |
| `maxdiff` | Optional maximum vardiff (0 = no limit). |
| `logdir` | Directory for logs (default: `logs`). |
| `maxclients` | Optional client limit. |
| `zmqblock` | ZMQ blockhash notification interface (default: `tcp://127.0.0.1:28332`). |

### Notes
- At least one bitcoind is required in CKPool mode with `server`, `rpcuser`, and `rpcpassword` set.
- Comments can be added after valid JSON in the configuration file.

## License
[Add license details here, e.g., GPL-3.0 or other, if applicable.]

## Support
For issues or contributions, visit [repository URL, e.g., GitHub link] or contact the developer.
```

This README provides a clear, concise overview of CKPool, its build process, runtime options, and configuration details, formatted for easy reading on platforms like GitHub. Replace placeholders (e.g., license, repository URL) with specific details if available. Let me know if you need further customization or additional sections!
