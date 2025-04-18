---
title: 'venco.py: A Python model to represent the charging flexibility and vehicle-to-grid potential of electric vehicles in energy system models'
tags:
  - electric vehicles modelling
  - demand-side flexibility
  - charging strategies
  - energy systems analysis 

authors:
  - name: Fabia Miorelli^[corresponding author]
    orcid: 0000-0001-5095-5401
    affiliation: 1
  - name: Niklas Wulff
    orcid: 0000-0002-4659-6984
    affiliation: 1
  - name: Benjamin Fuchs
    orcid: 0000-0002-7820-851X
    affiliation: 1
  - name: Hans Christian Gils
    orcid: 0000-0001-6745-6609
    affiliation: 1
  - name: Patrick Jochem
    orcid: 0000-0002-7486-4958
    affiliation: 1

affiliations:
 - name: German Aerospace Center (DLR), Institute of Networked Energy Systems, Curiestr. 4, 70563 Stuttgart, Germany
   index: 1


date: 29 February 2024
bibliography: paper.bib

---

# Summary

The bottom-up simulation model venco.py provides boundary conditions for load
shifting and vehicle-to-grid (V2G) potential of electric vehicles (EV) based on
mobility demand data and techno-economic assumptions. The tool enables the
modelling of the energy demand and flexibility potential of EV fleets within the
context of energy systems analysis. It supports the modelling of EV charging for
both controlled, i.e. load shifting and V2G, and uncontrolled charging
strategies. The model allows the configuration of assumptions regarding the
charging infrastructure, the technical characteristics of the vehicle fleet, and
the plugging behaviour, enabling the analysis of a wide variety of scenarios.
The main modelling outputs include battery drain profiles, charging and
discharging capacity profiles, minimum and maximum battery energy levels, and
uncontrolled charging profiles both at single vehicle and at fleet level. The
first four outputs can serve as constraining boundaries in other models, helping
to determine optimal charging strategies for the vehicles and representing EV
demand endogenously. In contrast, the uncontrolled charging profile simulates a
scenario where charging is uncontrolled and vehicles begin charging as soon as a
charging opportunity becomes available. The model's versatile and generic output
profiles can help address a wide range of research questions across multiple
modelling domains, including energy system optimisation models [@Wetzel.2024;
@Howells.2011; @Brown.2018] and agent-based electricity market models
[@Schimeczek.2023].

# Statement of need

Estimating the electricity demand, load shifting potential, or V2G capacity of
EV fleets is valuable across a wide range of research fields and industry
applications. Whether it is to analyse future grid ancillary service demands,
evaluate the profitability of aggregators managing EV fleets, calculate the
additional electricity demand from increased EV adoption, or assess the
demand-side flexibility EVs could offer to the energy system, these insights
play a critical role.

Within the field of energy systems analysis, two primary approaches to modelling
EVs can be identified: data-driven approaches and bottom-up simulations.
Data-driven approaches rely on empirically measured data, such as onboard
state-of-charge measurements or data collected at charging stations, which are
then scaled to represent a fleet in line with the modelling scope [@Martz.2022].
In contrast, bottom-up simulation models derive the flexibility and load
profiles of EV fleets by making assumptions about the charging controllability
and the technical parameters of vehicles [@GaeteMorales.2021]. These models
typically use mobility pattern data as their foundation, sourced either from
National Travel Surveys (NTSs) or transport research modelling results. Several
tools to calculate EV fleet profiles have been recently published, including
emobpy [@GaeteMorales.2021], RAMP-mobility [@Mangipinto.2022], OMOD
[@Strobel.2023], SimBEV [@simbev.2023], and MobiFlex [@Martz.2022]. Similarly,
venco.py was developed to provide demand and flexibility potential assessments
for future EV fleets.

While venco.py primarily focuses on plug-in battery electric vehicles, it
introduces several key novelties compared to existing models. First, it has the
capability to model different vehicle and transport segments, including
passenger and commercial transport, expanding its application scope. Second, it
uniquely captures plugging behaviours, which are often overlooked in other
models, and can simulate both explicit and implicit charging strategies,
incorporating exogenous and endogenous approaches. In the case of implicit
charging strategies, the model generates boundary profiles that can be used as
inputs in other models, without directly modelling the resulting load. Explicit
charging strategies, on the other hand, involve selecting a specific strategy
within the model itself, which is then simulated to produce the charging load as
an output. Third, it features ready-to-use interfaces for integrating data from
multiple existing NTSs across European countries. Another unique feature of
venco.py is its ability to perform analyses at a finer granularity, such as for
specific vehicle segments (e.g., small, medium, and large passenger cars, or
vans and heavy-duty trucks for commercial transport), socio-economic groups, or
at spatial resolutions beyond the national level. Since NTSs encompass a broad
range of data beyond mobility patterns, the tool enables the generation of EV
profiles that can be linked to specific groups of EV users.

The venco.py model is fully developed in Python and is openly available on
GitLab at
[https://gitlab.com/dlr-ve/esy/vencopy/vencopy](https://gitlab.com/dlr-ve/esy/vencopy/vencopy).


# Modelling approach

The venco.py model is designed to model heterogeneous vehicle fleets in a
user-friendly and flexible manner. While the model has been applied to several
National Travel Surveys (NTSs), including the German NTS for passenger
("Mobilität in Deutschland") [@infasDLRIVTundinfas360.2018] and commercial
transport ("Mobilitätsstudie Kraftfahrzeugverkehr in Deutschland")
[@WVIIVTDLRandKBA.2010], the English NTS ("National Travel Survey: England
2019") [@DepartmentforTransport.2019], the Dutch NTS ("Documentatie onderzoek
Onderweg in Nederland 2019 (ODiN2019)") [@CentraalBureauvoordeStatistiek.2020],
and the French NTS ("La mobilité locale et longue distance des Français -
Enquête nationale sur la mobilité des personnes en 2019")
[@Leservicedesdonneesetetudesstatistiques.2023], it is adaptable to any input
data representing the mobility patterns of a fleet within the specified
modelling scope, thanks to its flexible parsing approach. The model additionally
features user-defined temporal and geographical resolutions, and it supports
modelling at both the individual vehicle and fleet level.

The model is based on the main building blocks illustrated in Fig.
\ref{structure}, which correspond to the underlying class structure of the tool.
Starting with a parsing interface for mobility datasets, the data undergoes
cleaning and plausibility filtering, followed by consolidation to model internal
variables. The individual trips on the survey day are then consolidated into
person-specific travel diaries, which include multiple trips carried out by each
vehicle throughout the day. Next, the charging infrastructure allocation takes
place, using a charging infrastructure model that assumes charging stations are
available when vehicles are parked. Since the model's analytical focus is at the
regional level, the charging infrastructure availability is allocated either
based on binary mappings related to the trip's purpose or according to
probability distributions for charging availability. This approach allows for
the distinction of different charging availability scenarios. Subsequently,
demand and flexibility estimation is performed, based on techno-economic input
assumptions primarily related to vehicle battery capacity and power consumption.
After an iterative process, this produces the minimum and maximum battery
constraints. The daily activities are then discretised from a table format into
a time series format. The final step in the framework involves aggregating the
individual vehicle profiles to the fleet level and creating annual profiles from
the daily and weekly samples. Additionally, there is an option to normalise the
profiles or scale them to a desired fleet size.

The model output is accompanied by automatic metadata generation that complies
with the metadata requirements of the Open Energy Platform (OEP)
[@Booshehri.2021; @Hulk.2024], ensuring alignment with the FAIR (Findable,
Accessible, Interoperable, Reusable) principles [@Wilkinson.2016].


![Structure of venco.py. \label{structure}](figures/vencopy_structure_joss.pdf)


# Projects and publications

Earlier versions of venco.py have been applied in various projects to address
diverse research objectives. For example, in the EVer project [@ever.2018], the
model was used to compare different modelling approaches for demand-side
flexibility assets within the energy system optimisation model REMix
[@Wetzel.2024]. A more detailed assessment of the transport sector was conducted
in the BEniVer [@beniver.2018] and UrMoDigital [@urmo.2019] projects, which
analysed the roles of synthetic fuels, EVs, and innovative vehicle concepts,
respectively. Additionally, venco.py was employed in the framework of the SEDOS
project [@sedos.2022], which aimed to develop an open-source national reference
energy system dataset and create a reference model for three open-source
frameworks (oemof [@Krien.2020], TIMES [@times.2022], and FINE [@Gro.2023]),
with a specific focus on the German energy system. In the En4U project
[@en4u.2021], the model was used to generate representative load profiles based
on the mobility patterns of different household clusters and residential
time-varying tariffs. Moreover, in the EU DriVe2X project, venco.py is being
employed to evaluate the impact of large-scale deployment of V2X technologies on
the energy system as a whole [@drive2x.2023].


# Acknowledgements

The development of venco.py was funded through several third-party funded
projects supported by the German Federal Ministry of Economics and Climate
Protection (BMWK) including BEniVer ("Begleitforschung Energiewende im Verkehr" - 
"Accompanying research on the energy transition in transportation", grant
number 03EIV116F), SEDOS ("Die Bedeutung der Sektorintegration im Rahmen der
Energiewende in Deutschland - Modellierung mit einem nationalen Open Source
ReferenzEnergieSystem" - "The importance of sector integration in the context of
the energy transition in Germany - Modelling with a national open source
reference energy system", grant number 03EI1040D), and En4U
("Entwicklungspfade eines dezentralen Energiesystems im Zusammenspiel der
Entscheidungen privater und kommerzieller Energieakteure unter Unsicherheit" -
"Development pathways of a decentralized energy system in the interplay of
decisions made by private and commercial energy actors under uncertainty",
grant number 03EI1029A). Additional funding was provided by the German
Aerospace Center (DLR) through the internal projects UrMoDigital ("Wirkungen der
Digitalisierung auf städtische Verkehrssysteme" - "Effects of digitalisation on
urban transport systems") and EVer ("Energie und Verkehr" - "Energy and
Transport"), the European Union through the DriVe2X project ("Delivering Renewal
and Innovation to mass Vehicle Electrification enabled by V2X technologies",
Horizon Europe 101056934), and the Helmholtz Association's Energy System Design
research program.


# References