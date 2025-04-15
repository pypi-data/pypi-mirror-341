# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['sqlab',
 'sqlab.dbms',
 'sqlab.dbms.duckdb',
 'sqlab.dbms.mysql',
 'sqlab.dbms.postgresql',
 'sqlab.dbms.sqlite']

package_data = \
{'': ['*']}

install_requires = \
['cmd2>=2.4.3,<3.0.0',
 'jupysql>=0.10.12,<0.11.0',
 'mysql-connector-python>=8.2.0,<9.0.0',
 'psycopg2>=2.9.9,<3.0.0',
 'sqlalchemy>=2.0.27,<3.0.0',
 'sqlparse>=0.4.4,<0.5.0']

entry_points = \
{'console_scripts': ['sqlab = sqlab.__main__:main']}

setup_kwargs = {
    'name': 'sqlab',
    'version': '0.6.6',
    'description': 'SQL Adventure Builder: a command line tool for creating standalone SQL activities.',
    'long_description': "# SQLab\n\n![SQL adventure builder logo](assets/logo/color.svg)\n\nAn SQLab adventure is a text-based game where the player evolves through a series of isolated or interconnected puzzles by crafting SQL queries.\n\nIt consists in a standalone database encompassing the core dataset, a handful of stored procedures, and a table of encrypted messages (such as narrative elements, puzzle statements, answers, explanations, etc.).\n\nThere is no requirement to wrap a dedicated application around this database to “run” the game. It can be played on any generic GUI such as [DBeaver](https://dbeaver.io), [phpMyAdmin](https://www.phpmyadmin.net), [pgAdmin](https://www.pgadmin.org), or directly in a command-line interface.\n\nEach question comes with a unique formula, for example, `salt_042(sum(hash) OVER ())`. Appended to the `SELECT` clause, this formula calculates a decryption token, which may unlock the next episode or, if the query is incorrect, a tailored hint (assuming the game's creator has provided one).\n\nIn an educational context, this setup enables the students to learn and practice SQL without constant oversight. The instructor might stave off boredom by logging their queries and injecting new hints as needed, improving the game for all involved.\n\n## Examples on GitHub\n\n| Game | Pitch | Versions | DBMS | Included |\n| --- | --- | --- | --- | --- |\n| [SQLab Island](https://github.com/laowantong/sqlab_island) | An adaptation of [SQL Island](https://sql-island.informatik.uni-kl.de) by Johannes Schildgen | English | MySQL, PostgreSQL, SQLite | Sources + SQLab database |\n| [SQLab Sessform](https://github.com/laowantong/sqlab_sessform) | A set of independent exercises + _Mortelles Sessions_, a police investigation on a training company | French | MySQL, PostgresQL | SQLab database |\n| [SQLab Corbeau](https://github.com/laowantong/sqlab_corbeau) | An original adaptation of the movie [_Le Corbeau_](https://fr.wikipedia.org/wiki/Le_Corbeau_(film,_1943)) by Henri-Georges Clouzot (1943) | French | MySQL | Sources + SQLab database |\n| SQLab Club | An adaptation of [PostgreSQL Exercises](https://pgexercises.com) by Alisdair Owens | English | PostgreSQL | Sources + SQLab database (coming later) |\n\n## How can I create my own SQLab adventure?\n\nThe `sqlab` command-line tool is not required to play, but is necessary to create a new adventure.\n\n```\npip install sqlab\n```\n\nThe documentation is not yet available. In the meantime, you may explore the repository of [SQLab Island](https://github.com/laowantong/sqlab_island). The provided dataset and Jupyter notebooks serve as source material for the generation of the SQLab database.\n",
    'author': 'Aristide Grange',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/laowantong/sqlab/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
