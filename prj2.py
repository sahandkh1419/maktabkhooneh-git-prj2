from selenium import webdriver
import re
from time import sleep
import xlsxwriter
from tinydb import TinyDB

db = TinyDB('db.json')