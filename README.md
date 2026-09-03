Stress and Strain Analysis System

Group Members
  Member	            Primary Responsibility
  
  Erin Wade Acuña	    Task 1 – Basic Calculations
  
  Lance Wesley Santos	Task 2 – Control Structures
  
  Neo Carl Jacinto	  Task 3 – Data Structures
  
  Gabriel Dolar	      Task 4 – Functions
  
  John Oswald Amon	  Task 5 – OOP

Task 6 – Modular Integration was completed collaboratively by all members.

Project Description

The Stress-Strain Analysis System is a modular Python application designed to simulate, analyze, 
and manage material mechanical properties and stress-strain testing procedures. Built collaboratively
across a multi-module architecture, the program models material class hierarchies, organizes mechanical 
properties using modern dataclasses, executes simulated stress-strain test runs, and handles local data
persistence via JSON serialization and CSV reports. It bridges object-oriented design with practical 
standard-library utilities to function as a complete engineering analysis workflow.


Program Features

Modular Architecture: Cleanly separates responsibilities across dedicated modules  
(material.py, properties.py, tests.py, utils.py, database.py, and main.py).

Material Class Hierarchy: Object-oriented modeling that defines distinct 
material types and their inheritance structures.

Structured Property Data: Leverages Python dataclasses to cleanly store 
physical attributes such as Young’s Modulus, yield strength, and ultimate tensile strength.

Simulated Mechanical Testing: Runs automated stress-strain test simulations 
utilizing the random module to generate realistic stress/strain curves.

Timestamp Tracking: Automatically stamps every executed test with 
exact timestamps using the datetime module.

Data Persistence & Export:
  Saves and loads material profiles and settings using json.
  Exports test data arrays into well-formatted .csv files for external graphing or reporting.

Smart File Management: Uses pathlib to safely manage directories and store generated report 
files without throwing path errors across different operating systems.


Installation/Requirements

Python Version: Python 3.8 or higher.

External Dependencies: This project relies entirely on the Python Standard Library and requires no external third-party packages (no pip install required!).
  Standard Libraries Used: json, csv, datetime, pathlib, random.


How to Run the Program

  -Open your terminal or command prompt.
  
  -Navigate to the root folder of the project.
  
  -Execute the application via the main entry point:
      python stress_calculator/main.py
      
  -Observe the console output as the application loads materials 
  from the database, initializes tests, simulates data points, and outputs results.

  -Check the newly generated results/ directory to review your 
  saved .json logs and exported .csv test datasets.
    

  
