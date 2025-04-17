
from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="orange3-autogluon-timeseries",
    version="1.0.6",
    description="AutoGluon Time Series forecasting widget for Orange3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Иван Кордяк",
    author_email="KordyakIM@gmail.com",
    url="https://github.com/KordyakIM/autogluon-timeseries-widget",
    license="MIT",
    # Важно: используем find_namespace_packages
    packages=find_namespace_packages(include=["orangecontrib*"]),
    package_data={
        "orangecontrib.autogluon_timeseries.widgets": ["icons/*.png"],
    },
    entry_points={
        "orange.widgets": (
            "Time Series = orangecontrib.autogluon_timeseries.widgets",
        ),
        "orange.canvas.help": (
            "html-index = orangecontrib.autogluon_timeseries.widgets:WIDGET_HELP_PATH",
        )
    },
    namespace_packages=['orangecontrib'],  # Это особенно важно
    install_requires=[
        "Orange3>=3.38.1",
        "autogluon.timeseries>=1.2",
        "pandas>=2.2,<2.3",
        "numpy>=1.25",
        "PyQt5>=5.15",
        "matplotlib>=3.5"
    ],
    classifiers=[
    	"License :: OSI Approved :: MIT License",
    	"Programming Language :: Python :: 3.9",
    	"Operating System :: OS Independent",
    	"Development Status :: 4 - Beta",
    	"Intended Audience :: Science/Research",
    	"Intended Audience :: Education",
    	"Topic :: Scientific/Engineering :: Artificial Intelligence",
    	"Topic :: Scientific/Engineering :: Information Analysis",
    	"Topic :: Scientific/Engineering :: Visualization",
    	"Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords=["orange3 add-on", "time series", "forecasting", "autogluon"],
    python_requires=">=3.9",
)