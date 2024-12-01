# Smart Class Planning Tool
Class project for CPSC6177 - smart class planning tool

## Group 3
Pedro T, Emmanuel V, Jian Z

## Core Project Specifications

Functional requirements:
1. Course planning: The first goal of the software is to plan out classes among different semesters for a student until his/her graduation. The software takes three inputs and outputs an excel sheet where recommenced classes are listed. The recommended plan should be outputted by the software in the form of an excel document. 
2. Prerequisite checking: Another function of the software is to detect if a student’s plan has prerequisite issues. To do this, you need to construct a web crawler component within your software to grab the prerequisite information from CPSC Course Descriptions because the descriptions include prerequisite information which is sometimes missing in DegreeWorks.

Non-functional requirements:
1. The software should be configurable. Specifically, the inputs must be separated from the software and be parsed by the software.
2. The software should be implemented in Python and can be executed on Windows.

## Purpose

This application provides a student with a viable course plan to complete their studies, taking into account the following data:
* Current progress
* Course prerequisites
* Course schedule for future semesters
* Program requirements

## Required Inputs

1. Current DegreeWorks progress exported as a PDF file
2. URL of the appropriate course descriptions page for your program
3. Current course schedule Excel workbook provided by the department

## Prerequisites

1. Windows 10 or higher
2. DegreeWorks degree requirement file (PDF)
3. 4-Year Course Schedule file (Excel format)
4. Url for Prerequisites (https://catalog.columbusstate.edu/course-descriptions/cpsc/)

## Download

End-users should download the installer from: https://github.com/Pedro-T/ClassPlanningTool/blob/master/class_planning_tool_installer.exe

Source can be cloned via git using the url: https://github.com/Pedro-T/ClassPlanningTool.git

## Build/Configuration/Installation/Deployment

From Source:
1. Clone the repository from https://github.com/Pedro-T/ClassPlanningTool.git
2. Install requirements via pip, using provided requirements.txt
3. To launch from source, run main.py with no additional arguments

Using the Installer:
1. Run the downloaded installer (myInstaller.exe)
2. Follow the on-screen instructions to install the application
3. Once installed, the application will be available to run

## Usage
1. Upload Files:
  Upload the DegreeWorks PDF file for degree requirements
  Upload the 4-Year Course Schedule Excel file
  Enter the URL for course prerequisites
2. Generate Results:
  Click "Submit & Process" to generate your course plan
3. Download Results:
  Click "Download Result in Excel File" to save the generated course plan
  The Excel file will be saved in the Documents folder and can be opened directly
4. Restart Application:
  Use the "Restart" button to reset the tool for a new input set

