"""Regular expressions for data analysis"""
import re

pseudo_template = re.compile(r'(?<=://)[\w.]*(?=/|\b)')  # part with all domains from 0 level
pseudo_template_cleaner = re.compile(r'(?<=\.)\w*(?=\.)|^\w*(?=\.)')  # domains from 1 level and higher elementwise
valid_address_template = re.compile(r'https?://.*$')  # start with 'https://' or 'http://'
home_page_template = re.compile(r'https?://[\w.]*(?=/|\b)')  # part between 'https://' and first '/'
