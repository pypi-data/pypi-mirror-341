# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sucolo_database_services-stubs']

package_data = \
{'': ['*'],
 'sucolo_database_services-stubs': ['elasticsearch_client/*',
                                    'redis_client/*',
                                    'utils/*']}

install_requires = \
['sucolo-database-services>=0.1.3']

setup_kwargs = {
    'name': 'sucolo-database-services-stubs',
    'version': '0.1.3',
    'description': 'Type stubs for sucolo-database-services',
    'long_description': '# Type stubs for sucolo-database-services\n\nThis package provides type stubs for [sucolo-database-services](https://github.com/Stashq/sucolo-database_services).\n\n## Installation\n\n```bash\npip install types-sucolo-database-services\n```\n\n## Usage\n\nThe stubs will be automatically used by type checkers like mypy when you have both the main package and the stubs installed.\n\n## Versioning\n\nThe version of this package matches the version of the main package it provides stubs for.\n\n## License\n\nMIT License - see the LICENSE file for details \n',
    'author': 'Stanislaw Straburzynski',
    'author_email': 'sstraburzynski@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Stashq/sucolo-database_services',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.14',
}


setup(**setup_kwargs)
