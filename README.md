# ppstruct

`ppstruct` is a recursive kernel structure pretty-printer for the Linux `crash` utility, built on [`pykdump`](https://sourceforge.net/projects/pykdump/).

Instead of dumping raw C struct fields, `ppstruct` provides per-structure formatters that decode flags, enums, timestamps, bitmasks, lists/xarrays, and follow nested pointers recursively with cycle/duplicate pruning.

## Requirements

- Linux `crash` utility
- `pykdump` extension (`mpykdump.so`)

## Installation & Setup

1. Clone this repository:
   ```bash
   git clone <repo-url> ppstruct
   ```
2. Add the repository directory to `PYKDUMPPATH` before starting `crash`:
   ```bash
   export PYKDUMPPATH=/path/to/ppstruct:/path/to/pykdump
   ```
3. Load `mpykdump.so` in `crash`:
   ```text
   crash> extend /path/to/mpykdump.so
   ```

## Usage

Run `ppstruct` via `epython` inside `crash`:

```text
crash> epython ppstruct [options] <struct_type> <addr> [<addr> ...]
```

Once invoked, `ppstruct` also registers itself as a `crash` command (`ppstruct ...`).

### Options

| Option | Description |
| --- | --- |
| `-r`, `--recurse` | Increase recursion depth by 1 (default depth: `3`; may be specified multiple times) |
| `-n`, `--noprune` | Disable duplicate `(struct_type, address)` pruning |
| `-c`, `--counts` | Include structure use counts *(not implemented yet)* |
| `-l`, `--locks` | Include locks, mutexes, semaphores, etc. *(not implemented yet)* |
| `-s`, `--stats` | Include statistics *(not implemented yet)* |
| `-h`, `--help` | Show help message |

### Examples

```text
crash> epython ppstruct super_block 0xffff8b69407f0000
crash> epython ppstruct -r -r inode 0xffff8b69425ee2a0
crash> epython ppstruct -n dentry 0xffff8b69447dd000
```

## Supported Structures

Formatters are discovered dynamically by `ppstruct_core.py` across top-level modules and subpackages (`fs/`, `net/`, `misc/`, `ppstruct_types/`):

- **Core / Block / Device:** `address_space`, `backing_dev_info`, `bdi_writeback`, `block_device`, `buffer_head`, `device`, `device_driver`, `gendisk`, `loop_device`, `module`, `mount`, `nls_table`, `page`, `request_queue`, `timespec`, `timespec64`, `vfsmount`
- **VFS / Filesystems:** `dentry`, `file`, `file_lock`, `file_system_type`, `inode`, `mount`, `mnt_namespace`, `nameidata`, `path`, `super_block` (with `s_fs_info` dispatch), plus **ext4** (`ext4_inode_info`, `ext4_sb_info`, `ext4_super_block`), **XFS** (`xfs_buf`, `xfs_buftarg`, `xfs_ifork`, `xfs_imap`, `xfs_inode`, `xfs_mount`), **NFS / SunRPC** (`nfs4_session`, `nfs_client`, `nfs_fh`, `nfs_inode`, `nfs_server`, `rpc_clnt`, `rpc_task`, `rpc_timeout`, `rpc_xprt`), and **CIFS/SMB** (`cifs_sb_info`, `cifs_tcon`, `smb3_fs_context`, `tcon_link`)
- **Networking:** `net`, `sk_buff`, `sock`, `socket`
- **Misc:** `wait` (`wait_queue_head` / `wait_queue_entry`)

## Architecture

- [`ppstruct.py`](ppstruct.py) — CLI entry point and `crash` command registration
- [`ppstruct_core.py`](ppstruct_core.py) — recursive dispatch engine (`pp_struct`), dynamic module lookup, and `(type, addr)` pruning
- [`pp_utils.py`](pp_utils.py) — shared helpers for formatting flags, enums, timestamps, units, and integer/address parsing
- [`fs_lib.py`](fs_lib.py) — convenience re-exports for interactive and script use
- Type modules (`<struct_type>.py` or `<subdir>/<struct_type>.py`) — each defines `pp_struct_<struct_type>(addr, ...)`
