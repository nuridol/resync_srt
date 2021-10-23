RE:Sync SRT
===========

![Language](https://shields.io/github/languages/top/nuridol/resync_srt)
![License](https://shields.io/github/license/nuridol/resync_srt)

Note
----

This is the simple script to resynchronize SRT timestamps.

Requirements
------------

- Python 3.7+

Usage
-----

Here is the help message:

```Shell
usage: resync_srt.py [-h] [--debug] [--offset OFFSET] [--rate RATE] file

RE:Sync SRT v1.0

positional arguments:
  file             SRT file

optional arguments:
  -h, --help       show this help message and exit
  --debug          print debug message
  --offset OFFSET  sync offset(ms)
  --rate RATE      sync rate
```

If you want change timestamps by offset(milliseconds), use `--offset` option.

```bash
# push 5 seconds
resync_srt.py --offset 5000 sub.srt

# pull 3 seconds
resync_srt.py --offset -3000 sub.srt
```

If you want change timestamps by multiple with rate, use `--rate` option.

```bash
# change speed by multiplication
resync_srt.py --rate 1.2 sub.srt
```

And you can use both options at once. Now you can get a new file `<original filename>.resync.srt`.

# License

This software is released under the MIT License, see [LICENSE](LICENSE).
