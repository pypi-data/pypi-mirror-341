from setuptools import setup, find_packages


VERSION = '0.0.11'
DESCRIPTION = 'Youtube Autónomo AI utils are here.'
LONG_DESCRIPTION = 'These are the AI utils we need in the Youtube Autónomo project to work in a better way.'

setup(
    name = "yta_ai_utils", 
    version = VERSION,
    author = "Daniel Alcalá",
    author_email = "<danielalcalavalera@gmail.com>",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = [
        'yta-general-utils',
        'google-generativeai',
        'transformers',
        'ollama',
        'openai',
        'requests',
        # Please, remove this 'tqdm' library as it is only for showing progress bars
        'tqdm',
        # Please, remove this 'whisper_timestamped' library as its functionality is not necessary here
        'whisper_timestamped',
        'python-dotenv',
        # This 're_gpt' library could be refactored or removed maybe
        're_gpt',
        # This 'ai21' library could be removed I think...
        'ai21'
    ],
    
    keywords = [
        'youtube autonomo ai utils'
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)