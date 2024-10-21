from setuptools import setup, find_packages

INSTALL_REQUIRES = ["intake >=0.6.6"]

setup(
    name="tethysdash_plugin_cw3e",
    version="0.0.1",
    description="usace visualization plugins for tethysdash",
    url="https://github.com/FIRO-Tethys/tethysdash_plugin_cw3e",
    maintainer="Corey Krewson",
    maintainer_email="ckrewson@aquaveo.com",
    license="BSD",
    py_modules=["tethysdash_plugin_cw3e"],
    packages=find_packages(),
    entry_points={
        "intake.drivers": [
            "cw3e_ar_landfall = cw3e_visualizations.ar_landfall:ARLandfall",
            "cw3e_qpf = cw3e_visualizations.qpf:QPF"
        ]
    },
    package_data={"": ["*.csv", "*.yml", "*.html"]},
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
)
