from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import re

# === Create a new flask cache object
cache = Cache()

# === Create a new flask SQL ORM object
db = SQLAlchemy()


def non_empty_string(s, field):
    # === Method that raises an error on empty string
    if not s:
        raise ValueError(
            f"{field} must not be empty!")
    else:
        return s


def limited_string(s, field, max_length=25):
    # === Method that raises an error on string thats longer than max_length
    if len(s) > max_length:
        raise ValueError(
            f"{field} must have a maximum of {max_length} characters!")
    else:
        return s


def clean_string(s, field):
    # === Method that raises an error on string that contains the word curse
    ans = re.search(r"\bcurse\b", s, re.IGNORECASE)
    if ans:
        raise ValueError(
            f"{field} must not contain curse words!")
    else:
        return s


def validated_input(field, validations, args):
    # === Method that returns a method to validate a string by argumented validations
    def validate(s):
        for v in validations:
            if v == 'clean':
                clean_string(s, field)
            if v == 'limit':
                limited_string(s, field, args['max_length'])
            if v == 'non_empty':
                non_empty_string(s, field)
        return s
    return validate
