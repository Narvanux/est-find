# est-find

### Installation

```shell
git clone https://github.com/Narvanux/est-find.git
cd est-find
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```



You can also add an execute script to ~/.local/bin/

```shell
cd ~/.local/bin/
touch est-find
chmod +x est-find
```

**est-find** has following content:

```shell
#!/bin/bash
path="(path)"
source "${path}/venv/bin/activate"
python3 "${path}/main.py" "$@"
deactivate
```

P.S. \$path has project directory. Ex: "\$HOME/Projects/est-find"):

### Usage

```shell
python3 main.py -h
```

| Argument       | Explanation                                                          |
|:-------------- | -------------------------------------------------------------------- |
| `-h`           | displays help message                                                |
| `-s SEARCH`    | search for similar words (str)                                       |
| `-w WORD`      | get response for a specific word (str)                               |
| `-t LANG`      | translate meaning panels in specified language (str: ru, et, fr, uk) |
| `-l LIMIT`     | limit amount of meaning panels shown in response (int)               |
| `-v VARIATION` | select variation of the word with a similar spelling (int)           |
| `-sn`          | show synonims of the word in panels                                  |
| `-d`           | show definition of the word in Estonian                              |
| `-e`           | show examples of the word usage                                      |
| `-f`           | show forms of the word                                               |
| `-u`           | upgrade cookies, which are used to access website API                |
