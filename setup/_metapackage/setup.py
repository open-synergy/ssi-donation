import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-donation",
    description="Meta package for open-synergy-ssi-donation Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_donation',
        'odoo14-addon-test_ssi_donation',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
