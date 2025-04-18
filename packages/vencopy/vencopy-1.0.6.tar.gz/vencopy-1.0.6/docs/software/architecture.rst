..  venco.py introdcution file created on September 15, 2020
    Licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/deed.en

.. _architecture:

Architecture Documentation
===================================

General structure of the framework
---------------------------------------------------

The figure below shows the detailed venco.py components in a developer diagram. The main components - implemented as 
Python classes - DataParser, DiaryBuilder, GridModeller, FlexEstimator, ProfileAggregator and PostProcessor can be 
clearly distinguished. A brief description of the classes is presented below. For a more
detailed algebraic description of the tool please refer to the :ref:`publications` section.


.. image:: ../figures/vencopy_structure_detailed.drawio.png
	:width: 600
	:align: center


Quality values
---------------------------------------------------

For development, we follow a specific prioritisation of quality values to choose from different options to implement
a solution to a problem. These priorities are listed in the table below. 

.. list-table:: Quality values
   :widths: 35, 65
   :header-rows: 1

   * - Value priority
     - Description
   * - 1. Learnability
     - The highest priority of venco.py is to provide an easy-to-apply tool for scientists (not primarily developers) to
       estimate electric vehicle fleets' load shifting potential. Hence, easy to understand approaches, code structures
       and explicit formulations are favoured.
   * - 2. Readability
     - The readability of the code, especially the linear flow structure of the main venco.py file should be preserved.
       Source code and equations should be easy to read and understand. Splitting of statements is favoured over 
       convoluted one-liners. Significant learnability improvements (e.g. through an additional library), may motivate a
       deviation from this principle.
   * - 3. Reproducibility
     - The model has to be deterministic and reproducible both on the scientific and on the technical level. Hence, all
       example and test artifacts have to be part of the git repository. Source code revisions should be used to 
       reference reproducible states of the source code.
   * - 4. Reliability
     - The software has to operate without crashes and should terminate early, if scientific requirements are not met.
       Testing and asserting expectations in code is encouraged.
   * - 5. Performance
     - Performance is not the highest priority, since venco.py is not a real-time application. However, basic performance
       considerations like efficient formulation and application of libraries and algorithms should be considered.



Organizational information
---------------------------------------------------

.. list-table:: requirements
   :widths: 35, 65
   :header-rows: 1

   * - Requirement
     - Context
   * - Software Engineering Team
     - Niklas Wulff, Fabia Miorelli, Benjamin Fuchs
   * - Stakeholders
     - Hans Christian Gils, Department of Energy Systems Analysis at Institute of Networked Energy Systems, DLR
   * - Timeline
     - We are not a software development company, so release planning and implementation always depends on our currently
       running research projects. For planned releases, see :ref:`releaseTimeline`.
   * - Open source ready
     - Features, dependencies and components which are contraindicative or at odds with an open source publication 
       should not be used.
   * - Development tools
     - Source code and all artefacts are located in the DLR GitLab repository for venco.py including the software 
       documentation. For development, we use VSCode, git and mambaforge are used. For graphical depictions of software
       components and similar documentation draw.io and InkScape are used.





