# Sensor data to Scenario generation

## Introduction

A Scenario xml file is generated for input to software using Sensor data from the vehicle. Following is the brief process:
- Reading projection data
- Reading GPS data
- Converting GPS co-ordinates to local using projection
- Passing converted data to Template Scenario file to add Pathshape.

## Libraries used
- ***lxml*** is used for XML parsing
- ***pyproj*** is used for projections
- ***pandas*** is used for data pre/post processing