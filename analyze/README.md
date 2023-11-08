1. run process
```
python process.py -d data_dir -o output_dir
```
eg.
```
python process.py -d /home/yunchi/data/xinda -o /home/yunchi/data/xinda_analyze
```
- `-d`: data directory, optional if correct path is set in `config.py`.
- `-o`: output directory, optional if correct path is set in `config.py`.
- `-p`: optional, parser name,  can be `runtime`, `info`, `raw` etc. or combination of them with "`,`". Default to trigger all parsers.
