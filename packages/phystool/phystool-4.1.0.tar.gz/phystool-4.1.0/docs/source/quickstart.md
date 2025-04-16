# Quickstart

## Installation

Pour installer {{phystool}} dans un environnement virtuel, il suffit de passer
par `pip`:

    pip install phystool


### Requirements

+ Python 3.12
+ git
+ [ripgrep](https://github.com/BurntSushi/ripgrep): Utilisé pour chercher des
  chaines de caractères dans les fichiers {{tex}}.
+ [bat](https://github.com/sharkdp/bat): Utilisé pour afficher le contenu des
  fichier {{tex}} dans le terminal et pour afficher les modifications suivies par
  {{git}}.
+ [delta](https://github.com/dandavison/delta>): Utilisé pour afficher les
  modifications suivies par {{git}}.


## Premier démarrage

Lors du démarrage {{phystool}} charge le fichier de configuration
`~/.phystool/phystool.conf`. Si celui-ci n'existe pas, il est automatiquement
crée et son contenu est par défaut:

```{literalinclude} ../../src/phystool/static/phystool.conf
```
