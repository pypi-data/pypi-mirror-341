.. venco.py getting started documentation file, created on February 11, 2020
    Licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/deed.en

.. _start:

Getting Started and Tutorials
===================================

Tutorials overview
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


To get started with venco.py, a set of tutorials are provided for the user to
learn about the different classes and how each of them can be customised. The
tutorials are interactive python files and can be found
in the gitlab repository.

- Tutorial 1: Showcasing run.py
- Tutorial 2: Entering mobility data: The DataParser class structure
- Tutorial 3: The GridModeller class
- Tutorial 4: The FlexEstimator class
- Tutorial 5: The DiaryBuilder and TimeDiscretizer classes (currently this 
  tutorial is empty, it will be complemented following upcoming developments)

Tutorials setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To start carrying out the tutorials, you need to follow the developer installation.
After that, open the folder with vencopy and navigate to the tutorials folder and the tutorial you want to run.

Now to be able to run the tutorials, first activate your vencopy environment.

.. code-block:: python

  conda activate <your environment name>
    
Now you can run the tutorial files as a module or in debug mode depending on your preferred IDE.


Adaptability for new databases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For guidance on adapting venco.py for a new NTS or other mobility datasets, including writing a custom
parsing class beyond the ones provided, refer to :ref:`adaptability`. This page provides step-by-step
instructions on the steps and the required minimal features to
ensure compatibility with the processing logic of venco.py.


.. 
  If you want to run the tutorial in an environment which already exists, you can
  first activate your desired environment and then install the necessary packages. 

..
  .. code-block:: python

..
    conda install jupyterlab 

..
  You might need to add the ipykernel to the environment to be able to run the 
  jupyter notebooks with the tutorials. To do this type 

..
  .. code-block:: python

..
    python -m ipykernel install --user --name=<your environment name> 
    
  Now that the requirements are satisfied, you can either open the jupyter 
  notebooks with the tutorials in an IDE that supports notebooks (e.g. VSCode) or
  open them in browser from the Anaconda Powershell Prompt

..
  .. code-block:: python

..
    jupyter lab --notebook-dir='<your local path to te repository>' --browser=firefox
    
  Note: you might need to restart the jupyter notebooks kernel between the 
  tutorials if you carry out multiple ones.
