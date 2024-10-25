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

## Setup

TBD

## Usage

TBD
