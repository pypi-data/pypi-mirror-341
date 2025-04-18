.. venco.py documentation master file, created by
   sphinx-quickstart on Tue Feb  4 09:27:27 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



Welcome to venco.py's documentation!
============================================

.. image:: https://img.shields.io/pypi/v/vencopy
   :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/vencopy
   :alt: PyPI - Python Version

.. image:: https://img.shields.io/pypi/l/vencopy
   :alt: PyPI - License

.. image:: https://badges.gitter.im/vencopy/community.svg
    :target: https://gitter.im/vencopy/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
    :alt: Chat on Gitter

A data processing tool offering hourly demand and flexibility profiles for future electric vehicle fleets in an aggregated manner.
venco.py is developed at the `Department of Energy Systems Analysis <https://www.dlr.de/ve/en/desktopdefault.aspx/tabid-15971/25909_read-66550/>`_ at the `German Aerospace Center (DLR) <https://www.dlr.de/EN/Home/home_node.html>`_.


.. image:: /figures/vencopy_logo_repo.png
	:width: 300
	:align: center


.. raw:: html

   <br>


In a nutshell, with venco.py you can:

- :ref:`simulate different charging strategies (uncontrolled, controlled charging , V2G) for EV fleets <flexestimators>`
- :ref:`model different grid infrastructure options (home charging, work charging, ..) <gridmodellers>`
- :ref:`analyse charging behaviour based on socio-economic data and trip purpose <dataparsers>`



Useful Information about venco.py
--------------------------------------
- :ref:`Find a general description of venco.py and its capabilities here <intro>`
- :ref:`Find the different installation instructions here <installation>`
- :ref:`Find some frequently asked questions here <faq>`
- :ref:`Find information on planned future features <releasetimeline>`
- :ref:`Find information on how to contribute <contributing>`



About
------------------
- Authors: Niklas Wulff, Fabia Miorelli
- Contact: vencopy@dlr.de


Links
-------------------
- `Source code <https://gitlab.com/dlr-ve/esy/vencopy/vencopy>`_
- `PyPI release <https://pypi.org/project/vencopy>`_
- `License <https://opensource.org/licenses/BSD-3-Clause>`_


Acknowledgements
-------------------
The development of venco.py was funded through several third-party funded
projects supported by the German Federal Ministry of Economics and Climate
Protection (BMWK) including BEniVer ("Begleitforschung Energiewende im Verkehr",
FKZ 03EIV116F), SEDOS ("Die Bedeutung der Sektorintegration im Rahmen der
Energiewende in Deutschland - Modellierung mit einem nationalen Open Source
ReferenzEnergieSystem", FKZ 03EI1040D), and En4U ("Entwicklungspfade eines
dezentralen Energiesystems im Zusammenspiel der Entscheidungen privater und
kommerzieller Energieakteure unter Unsicherheit", FKZ 3026201). Additional
funding was provided by the German Aerospace Center (DLR) through the internal
projects UrMoDigital ("Wirkungen der Digitalisierung auf städtische
Verkehrssysteme") and EVer ("Energie und Verkehr"), the European Union through
the DriVe2X project ("Delivering Renewal and Innovation to mass Vehicle
Electrification enabled by V2X technologies", Horizon Europe 101056934), and the
Helmholtz Association's Energy System Design research program.


.. toctree::
   :caption: Getting Started
   :hidden:
   :maxdepth: 1

   gettingstarted/intro
   gettingstarted/installation
   gettingstarted/start

.. toctree::
   :caption: Software
   :hidden:
   :maxdepth: 2

   software/architecture
   software/core
   software/functions
   software/inputoutput
   software/codestyle

.. toctree::
   :caption: Research
   :hidden:
   :maxdepth: 1

   research/projects
   research/publications

.. toctree::
   :caption: Contribution
   :hidden:
   :maxdepth: 1

   contribution/releasetimeline
   contribution/contributing
