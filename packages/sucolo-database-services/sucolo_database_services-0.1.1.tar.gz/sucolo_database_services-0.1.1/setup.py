# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sucolo_database_services',
 'sucolo_database_services.elasticsearch_client',
 'sucolo_database_services.redis_client',
 'sucolo_database_services.tests',
 'sucolo_database_services.utils']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=8.17.2,<9.0.0',
 'geopandas>=1.0.1,<2.0.0',
 'h3>=4.2.2,<5.0.0',
 'pandas>=2.2.3,<3.0.0',
 'pydantic>=2.11.3,<3.0.0',
 'redis>=5.2.1,<6.0.0']

setup_kwargs = {
    'name': 'sucolo-database-services',
    'version': '0.1.1',
    'description': "A Python client for Sucolo's database services.",
    'long_description': '# Sucolo Database Services\n\nA Python package providing database services for the Sucolo project, including Elasticsearch and Redis clients with additional utilities for data processing and analysis.\n\n## Features\n\n- Elasticsearch client integration\n- Redis client integration\n- Data processing utilities\n- H3 geospatial indexing support\n- Type-safe data handling with Pydantic\n\n## Requirements\n\n- Python 3.11\n- Poetry for dependency management\n\n## Installation\n\n1. Clone the repository:\n```bash\ngit clone https://github.com/yourusername/sucolo-database_services.git\ncd sucolo-database_services\n```\n\n2. Install dependencies using Poetry:\n```bash\npoetry install\n```\n\n3. Set up your environment variables in `.env` file:\n```\n# Example .env configuration\nELASTICSEARCH_HOST=localhost\nELASTICSEARCH_PORT=9200\nREDIS_HOST=localhost\nREDIS_PORT=6379\n```\n\n## Development\n\n### Code Style\n\nThis project uses several tools to maintain code quality:\n\n- Black for code formatting\n- Flake8 for linting\n- MyPy for type checking\n- isort for import sorting\n\nRun the following command to format and check the code:\n```bash\nmake format\n```\n\n### Testing\n\nRun tests using pytest:\n```bash\nmake test\n```\n\n## Project Structure\n\n```\nsucolo_database_services/\n├── elasticsearch_client/  # Elasticsearch client implementation\n├── redis_client/         # Redis client implementation\n├── utils/                # Utility functions and helpers\n├── tests/                # Test suite\n└── db_service.py         # Main database service implementation\n```\n\n## Dependencies\n\nMain dependencies:\n- elasticsearch\n- redis\n- pandas\n- geopandas\n- h3\n- pydantic\n- python-dotenv\n\n## License\n\n[Add your license information here]\n\n## Contributing\n\n[Add contribution guidelines here]\n',
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
