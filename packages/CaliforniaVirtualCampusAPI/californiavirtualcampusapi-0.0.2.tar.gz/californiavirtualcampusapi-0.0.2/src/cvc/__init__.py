"""
California Virtual Campus API

A simple API for the California Virtual Campus platform.

:copyright: (c) 2025 Robert Meli
:license: Apache 2.0, see LICENSE for more details.
"""

from .helperFunctions import _getCourseContentByID, _getCourseIDsByLandingPage, _getCourseIDsBySearch

__all__ = ["getCourseContentByID", "getCourseContentByScraping", "getCourseIDsByScraping", "getCourseIDsBySearch"]

def getCourseContentByID(id:int):
    """
    Using a provided course ID, returns a course object with info scrapped from the CVC course webpage.

    Parameters:
    id (int): The CVC ID of the desired course

    Raises:
    ValueError: Inputted ID, id, is invalid.

    Returns:
    course: A course object filled with the desired course info.
    """
    return _getCourseContentByID(id)

def getCourseContentByScraping(collegeName:str, C_ID:str, courseSymbol:str, courseName:str):
    """
    Using a provided the provided college name, 
    searches for all the CVC IDs of the classes in the college which would be returned in a query with the above parameters.
    Returns a list of each of their corresponding course objects.
    This method uses Selenium to perform the search query.

    Parameters:
    collegeName (str):  Name of the college whose classes you will search.
    C_ID (str):         The C-ID of the class you want to find.
    courseSymbol (str): The course symbol of the class you want to find.
    courseName (str):   The name of the course you want to find.

    Returns:
    courses: A list of course objects.
    """
    courseIDs = _getCourseIDsByLandingPage(collegeName, C_ID, courseSymbol, courseName)
    courses = []
    for id in courseIDs:
        courses.append(_getCourseContentByID(id))
    return courses

def getCourseIDsByScraping(collegeName:str, C_ID:str, courseSymbol:str, courseName:str):
    """
    Using a provided the provided college name, 
    searches for all the CVC IDs of the classes in the college which would be returned in a query with the above parameters.
    Returns a list of the found IDs.
    This method uses Selenium to perform the search query.

    Parameters:
    collegeName (str):  Name of the college whose classes you will search.
    C_ID (str):         The C-ID of the class you want to find.
    courseSymbol (str): The course symbol of the class you want to find.
    courseName (str):   The name of the course you want to find.

    Returns:
    A list of CVC IDs.
    """
    return _getCourseIDsByLandingPage(collegeName, C_ID, courseSymbol, courseName)

def getCourseIDsBySearch(collegeName:str, C_ID:str, courseSymbol:str, courseName:str):
    """
    Using a provided the provided college name, 
    searches for all the CVC IDs of the classes in the college which would be returned in a query with the above parameters.
    Returns a list of the found IDs.
    
    Parameters:
    collegeName (str):  Name of the college whose classes you will search.
    C_ID (str):         The C-ID of the class you want to find.
    courseSymbol (str): The course symbol of the class you want to find.
    courseName (str):   The name of the course you want to find.

    Returns:
    A list of CVC IDs.
    """
    return _getCourseIDsBySearch(collegeName, C_ID, courseSymbol, courseName)