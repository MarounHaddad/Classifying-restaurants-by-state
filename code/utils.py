from scipy.stats import pearsonr
import time
import math
from datetime import datetime, timedelta
import json
import pandas as pd

datapath = "../../data/qcrestaurants/"

def save_all_restaurants_to_kml(business_rest, file_name):
    """"
    This function saves the longitude and latitude
    of all restaurants in kml format to be viewed on google earth
    red: closed
    green: open
    """
    kml = ""
    for index, business in business_rest[business_rest.is_open == 1].iterrows():
        kml += "<Placemark>\n" + \
               "<styleUrl> #green</styleUrl>\n" + \
               "<Point>\n" + \
               "<coordinates> " + str(business.longitude) + ", " + str(business.latitude) + ", 0 </coordinates>\n" + \
               "</Point>\n" + \
               "</Placemark>\n"
        # "<name> " + str(business['name']).replace("&","&amp;") + " </name>\n"+ \
    for index, business in business_rest[business_rest.is_open == 0].iterrows():
        kml += "<Placemark>\n" + \
               "<styleUrl> #red</styleUrl>\n" + \
               "<Point>\n" + \
               "<coordinates> " + str(business.longitude) + ", " + str(business.latitude) + ", 0 </coordinates>\n" + \
               "</Point>\n" + \
               "</Placemark>\n"
        # "<name> " + str(business['name']).replace("&","&amp;") + " </name>\n" + \
    text_file = open("../../data/preprocess/" + file_name + ".txt", "wt")
    n = text_file.write(kml)
    text_file.close()
    print("\nsuccessfully saved all restaurants to kml format\n")


def save_closed_restaurants_to_kml(business_rest, file_name):
    """"
    This function saves the longitude and latitude
    of closed restaurants in kml format to be viewed on google earth
    """
    kml = ""
    for index, business in business_rest[business_rest.is_open == 0].iterrows():
        kml += "<Placemark>\n" + \
               "<styleUrl> #red</styleUrl>\n" + \
               "<Point>\n" + \
               "<coordinates> " + str(business.longitude) + ", " + str(business.latitude) + ", 0 </coordinates>\n" + \
               "</Point>\n" + \
               "</Placemark>\n"
        # "<name> " + str(business['name']).replace("&","&amp;") + " </name>\n" + \
    text_file = open("../../data/preprocess/" + file_name + ".txt", "wt")
    n = text_file.write(kml)
    text_file.close()
    print("\nsuccessfully saved closed restaurants to kml format\n")


def pearson_correlation(x, y):
    """
    calculates the pearson correlation between two attributes
    :param x: first attribute
    :param y: second attribute
    :return:
    """
    corr, _ = pearsonr(x, y)
    return corr


def calc_total_open_hours(row):
    """
    calculate total open hours per business record
    :param row: business record
    :return: total_hours
    """
    days = row.hours
    total_hours = 0
    if type(days) is not dict:
        return 0
    for day in days:
        hours = days[day].split("-")
        FMT = '%H:%M'
        hours_day = datetime.strptime(hours[1], FMT) - datetime.strptime(hours[0], FMT)
        total_hours += hours_day.seconds / 3600
    return total_hours


def is_open_week_day(row, week_day):
    """
    returns true (1) if the business is open on a certain week_day
    :param row: business record
    :param week_day: weekday name
    :return: bool (open 1 closed 0)
    """
    days = row.hours
    if type(days) is not dict:
        return 0
    if week_day in days:
        return 1
    else:
        return 0


def get_attribute(row, attribute, default_value):
    """
    This function returns the attribute value of the record
    in dictionary attributes of the Dataframe business
    :param row: business record
    :param attribute: name of the attribute to extract
    :param default_value: the value to return if the attribute is not in dictionary
    :return: attribute_value
    """
    attributes = row.attributes
    if type(attributes) is not dict:
        return default_value

    attribute_value = default_value
    if attribute in attributes:
        attribute_value = attributes[attribute]
        if attribute_value == 'True':
            attribute_value = 1
        if attribute_value == 'False':
            attribute_value = 0
        if attribute_value == 'None':
            attribute_value = 0
    return attribute_value


def init_ds(json):
    """
    this function transform json into a dictionary
    :param json: jason data
    :return: dictionary, keys
    """
    ds = {}
    keys = json.keys()
    for k in keys:
        ds[k] = []
    return ds, keys


def read_json(file):
    """
    this function reads a json file and returns it as a dataframe
    :param file: json file path
    :return: dataframe
    """
    dataset = {}
    keys = []
    with open(file, errors='ignore') as file_lines:
        for count, line in enumerate(file_lines):
            data = json.loads(line.strip())
            if count == 0:
                dataset, keys = init_ds(data)
            for k in keys:
                dataset[k].append(data[k])

        return pd.DataFrame(dataset)