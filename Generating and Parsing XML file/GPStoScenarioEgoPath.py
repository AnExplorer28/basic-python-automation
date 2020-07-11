import pyproj
import pandas as pd
from lxml import etree as ET

##Extract Projection String from Opendrive xml file

parser = ET.XMLParser(remove_blank_text=True)

xodr_tree = ET.parse('../Sample.xodr', parser) #Input Path to Opendrive File

root = xodr_tree.getroot()

geoReference = root.find('header/geoReference')

proj_string = geoReference.text.strip() #Extracting Projection String from the Geo reference header in Opendrive File

##Converting GPS to local co-ordinates

input_file = pd.read_csv('../GPSdata.csv') #Reading GPS co-ordinates Time series data

input_lat = list(input_file.loc[:,'latitude'])
input_long = list(input_file.loc[:,'longitude'])

p = pyproj.Proj(proj_string) #Defining projection string for conversion

xs, ys = p(input_long, input_lat, inverse=False) #Converting GPS co-ordinates to Local

#print(xs, ys)

##Creating VTD Scenario xml file

tree = ET.parse('../Template.xml', parser) #Reading Template File with predefined Tags

root = tree.getroot()

PathShape = root.find('MovingObjectsControl/PathShape') #Finding Pathshape Tag in Template file

for x,y in zip(xs,ys): #Adding Waypoints from converted GPS data to Pathshape
    Waypoint = ET.SubElement(PathShape, 'Waypoint')
    Waypoint.attrib['X'] = '{:.16e}'.format(x)
    Waypoint.attrib['Y'] = '{:.16e}'.format(y)
    Waypoint.attrib['Options']= "0x00000000"
    Waypoint.attrib['Z'] = "0.0000000000000000e+00"
    Waypoint.attrib['Weight'] = "1.0000000000000000e+00"
    Waypoint.attrib['Yaw'] = "0.0000000000000000e+00"
    Waypoint.attrib['Pitch'] = "0.0000000000000000e+00"
    Waypoint.attrib['Roll'] = "0.0000000000000000e+00"

ET.indent(root, space="    ")

##Output the file edited with Pathshape data

tree.write('Template_Output.xml', pretty_print=True, encoding='utf-8', xml_declaration=True)