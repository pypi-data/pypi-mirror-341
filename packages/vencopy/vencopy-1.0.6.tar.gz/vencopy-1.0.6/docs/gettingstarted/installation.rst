.. venco.py installation documentation file, created on February 11, 2020
    Licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/deed.en

.. _installation:

Installation and Setup
===================================


Requirements and boundary conditions
-------------------------------------

venco.py runs on Unix and Windows-based operating systems. It requires:

- A working installation of Python
- The package, dependency, and environment management tool conda (or mamba)
- Internet access for downloading the required packages

Versioning follows semantic versioning (X.Y.Z) and is managed via git labels.
You can install venco.py in one of two ways:

- As a user (installation from PyPI)
- As a developer (checking out the repository from GitLab)

Depending on your choice, the installation and setup process will differ.


.. image:: ../figures/application_context.drawio.png
	:width: 600
	:align: center


Installation for users
-------------------------------------

As a user, you will apply venco.py for answering analytical questions. Thus,
you're mainly interested in applying venco.py's built-in features and functions.
On this level, you will not change the codebase within the venco.py core class
objects - of course you can write your own data processing routines around those
functions.

If you are using venco.py to answer analytical questions, follow these steps:

1. **Set up a Conda Environment**

Open a conda console and create a new environment::

    conda create -n <your_environment_name> python
    conda activate <your_environment_name>

2. **Install venco.py from PyPI**

Run the following command::

    pip install vencopy

3. **Create a venco.py User Folder**

Navigate to a parent directory where you want to create your venco.py user
folder and run::

    python -m vencopy


You will be prompted for a user folder name. Enter the name and press Enter. The
following folder structure will be created::



    FOLDERNAME
    ├── config
    │   ├── dev_config.yaml
    │   └── user_config.yaml.default
    ├── output
    │   ├── dataparser
    │   │   ├── dataparsers
    │   │   ├── parkinference
    │   │   ├── parseMiD
    │   │   └── parseKiD
    │   ├── gridmodeller
    │   ├── flexestimator
    │   ├── diarybuilder
    │   ├── profileaggregator
    │   └── postprocessor
    ├── tutorials
    │   └── ..
    └── run.py


4. **Configure venco.py**

Duplicate the default configuration file:

- Navigate to the config folder, copy user_config.yaml.default, and rename it to
  user_config.yaml.
- Edit the user_config.yaml:
    Set vencopy_root (user_config["global"]["absolute_path"]["vencopy_root"]) to
    the absolute path of your cloned vencopy repository. Set the path to your
    local MiD STATA folder (ending with /B2/STATA/).


The user_config in the config folder is the main interface between the user and
the code. In order to learn more about them, check out our tutorials. For this
you will not need any additional data as an extract of a suitable database is
provided `here <https://gitlab.com/dlr-ve/esy/vencopy/vencopy/-/blob/joss/tutorials/data_sampling/MiD17.csv?ref_type=heads>`_
This is an anonymised extract of the MiD B2 dataset. 

The dataset "Mobilität in Deutschland" (German for mobility in Germany), can be
requested here from the `clearingboard transport <https://daten.clearingstelle-verkehr.de/order-form.html>`_.
Alternatively, you can
use the tool in conjunction with any other national travel survey data or output
of transport models which contains at least the following variables:

    - Person ID: A unique identifier for each individual or vehicle or
      household.
    - Trip ID: A distinct identifier for each trip.
    - Timestamps: Precise hours of the day indicating the beginning and
      conclusion of a trip.
    - Trip Purpose: The underlying motivation or intention for embarking on a
      particular journey.
    - Distance: The total length in km covered during the trip.

To be able to run the following steps you need to have mobility data at hand. If
you have the "Mobilität in Deutschland" dataset or any other NTSs for which
venco.py has been already adapted you can continue with the following
instructions. Alternatively, you can try out the tutorials (see :ref:`start`).
For guidance on adapting venco.py for a new NTS or other mobility datasets, including writing a custom
parsing class beyond the ones provided, refer to :ref:`adaptability`. This page provides step-by-step
instructions on the steps and the required minimal features to
ensure compatibility with the processing logic of venco.py.

1. **Run venco.py**

Open your user folder in an IDE, configure your interpreter (environment), and
run::

    python run.py


The vencopy.log file will be generated during execution. This file serves as a
diagnostic tool, progress tracker, and audit trail.


Installation for developers
-------------------------------------

This part of the documentation holds a step-by-step installation guide for
venco.py if you want to contribute to the codebase. 


1. **Clone the Repository**

Navigate to a directory where you want to clone venco.py and run::

    git clone https://gitlab.com/dlr-ve/esy/vencopy/vencopy.git


2. **Set Up a Conda Environment**

Navigate to the folder of your cloned venco.py repository and run::

    conda create -n <your_environment_name> python
    conda activate <your_environment_name>
    pip install -e .

3. **Configure venco.py**

See point 4. above.


4. **Run venco.py**

You are now ready to either run the tutorials or to run venco.py if you have mobility data to
use (see :ref:`adaptability`) by typing::

   python run.py


For additional resources, tutorials, and dataset information, check out the
official documentation or the GitLab repository.

