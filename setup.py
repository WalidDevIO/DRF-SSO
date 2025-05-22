from setuptools import setup, find_packages

setup(
    name='drf-sso',
    version='0.0.1-beta',
    description='Module Django DRF pour une authentification SSO via CAS, OIDC, SAML, etc.',
    author='EL OUAZIZI Walid',
    author_email='walid.elouazizi29@gmail.com',
    url='https://github.com/WalidDevIO/drf-sso',
    packages=find_packages(exclude=['test', 'samples']),
    include_package_data=False,
    install_requires=[
        'requests',
        'pyjwt',
        'django',
        'lxml',
        'signxml',
        'dotenv',
        'djangorestframework',
        'djangorestframework_simplejwt'
    ],
    extras_require={
        'test': [
            'fastapi',
            'uvicorn'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',  # exemple
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
