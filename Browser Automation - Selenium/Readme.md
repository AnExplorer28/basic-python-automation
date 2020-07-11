# GPS file converter API

## Introduction
An web browser API is developed using ***selenium*** library which automates the following task:
- Navigates to the desired website
- Loads file on the website
- Converts the file
- Downloads the file
- Post processing to desired columns and format

***Pandas*** is used for Post Processing the file contents.

## Requirements:

Update to python latest version(preferably 3.6+)
```
pip install selenium
pip install pandas
pip install argparse
```
Update firefox to latest version.

Download suitable [Firefox driver](https://github.com/mozilla/geckodriver/releases) (under asset section check for your os and 32/64 bit):

## Input:

Script takes 2 paths as input which needs to be passed:

- Path where GPS files to be converted are located
  - input_dir = '\GPS Files'

- Path to firefox driver which was downloaded
  - driver_path = "\geckodriver-v0.26.0-win64\geckodriver"

## Example call:

> Please clone the repository to your local before making the example call

`git clone https://github.com/AnExplorer28/basic-python-automation`

Open a terminal window and navigate to folder where **GPS_converter.py** is located

`$ python GPS_converter.py --input_dir "D:\GPS Files" --driver_path "Downloads\geckodriver-v0.26.0-win64"`

You can also get help by running:

`python GPS_converter.py -h`

## Output:

It gives 2 files as output for each input file:

- **ABCD-1234.txt** - raw txt file downloaded from GPS visualizer.
- **ABCD-1234.csv** - csv file after removing time, sat and hdop columns.