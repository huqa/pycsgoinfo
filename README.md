# pycsgoinfo - demoinfogo-linux data parser

pycsgoinfo builds a coherent data resource from demoinfogo demo data.
The resource includes basic info about the match. 

### Requirements & installation

This project requires a compiled version of [demoinfogo](https://github.com/csgo-data/demoinfogo-linux) placed in the pycsgoinfo/lib-directory.

It's recommended to modify demoinfogo if you plan on calling it from an external program (https://github.com/huqa/pycsgoinfo/issues/1).


Run pycsgoinfo from the command line using
```
python pycsgoinfo-runner.py mydemo.dem
```

pycsgoinfo uses sqlite as the default data resource and creates a simple database named pycsgoinfo.db after parsing.

### Version
0.2.1

