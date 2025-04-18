import textdistance

collegeIdDict = {
    "American River College": 48,
    "Antelope Valley College": 49,
    "Bakersfield College": 217,
    "Barstow Community College": 218,
    "Berkeley City College": 83,
    "Butte College": 219,
    "Cabrillo College": 84,
    "Cañada College": 473,
    "Cerritos College": 480,
    "Cerro Coso Community College": 481,
    "Chabot College": 482,
    "Chaffey College": 483,
    "Citrus College": 489,
    "City College of San Francisco": 490,
    "Clovis Community College": 12437,
    "Coalinga College": 12372,
    "Coastline Community College": 103,
    "College of Alameda": 86,
    "College of Marin": 593,
    "College of San Mateo": 697,
    "College of the Canyons": 474,
    "College of the Desert": 512,
    "College of the Redwoods": 673,
    "College of the Sequoias": 705,
    "College of the Siskiyous": 711,
    "Columbia College": 499,
    "Compton College": 12634,
    "Contra Costa College": 104,
    "Copper Mountain College": 4802,
    "Cosumnes River College": 88,
    "Crafton Hills College": 504,
    "Cuesta College": 506,
    "Cuyamaca College": 507,
    "Cypress College": 508,
    "De Anza College": 50,
    "Diablo Valley College": 89,
    "East Los Angeles College": 55,
    "El Camino College": 220,
    "Evergreen Valley College": 526,
    "Feather River College": 529,
    "Folsom Lake College": 90,
    "Foothill College": 51,
    "Fresno City College": 536,
    "Fullerton College": 539,
    "Gavilan College": 541,
    "Glendale Community College": 543,
    "Golden West College": 91,
    "Grossmont College": 548,
    "Hartnell College": 551,
    "Imperial Valley College": 557,
    "Irvine Valley College": 563,
    "Lake Tahoe Community College": 571,
    "Laney College": 92,
    "Las Positas College": 4531,
    "Lassen Community College": 573,
    "Lemoore College": 12373,
    "Long Beach City College": 579,
    "Los Angeles City College": 56,
    "Los Angeles Harbor College": 57,
    "Los Angeles Mission College": 58,
    "Los Angeles Pierce College": 59,
    "Los Angeles Southwest College": 60,
    "Los Angeles Trade Technical College": 61,
    "Los Angeles Valley College": 62,
    "Los Medanos College": 93,
    "Madera Community College": 12641,
    "Mendocino College": 596,
    "Merced College": 599,
    "Merritt College": 94,
    "MiraCosta College": 601,
    "Mission College": 603,
    "Modesto Junior College": 606,
    "Monterey Peninsula College": 607,
    "Moorpark College": 611,
    "Moreno Valley College": 5751,
    "Mt. San Antonio College": 12370,
    "Mt. San Jacinto College": 615,
    "Napa Valley College": 618,
    "Norco College": 7842,
    "Ohlone College": 642,
    "Orange Coast College": 95,
    "Oxnard College": 645,
    "Palomar College": 656,
    "Palo Verde College": 655,
    "Pasadena City College": 658,
    "Porterville College": 666,
    "Reedley College": 567,
    "Rio Hondo College": 96,
    "Riverside City College": 676,
    "Sacramento City College": 97,
    "Saddleback College": 98,
    "San Bernardino Valley College": 99,
    "San Diego City College": 683,
    "San Diego Mesa College": 684,
    "San Diego Miramar College": 685,
    "San Joaquin Delta College": 692,
    "San Jose City College": 696,
    "Santa Ana College": 670,
    "Santa Barbara City College": 100,
    "Santa Monica College": 101,
    "Santa Rosa Junior College": 701,
    "Santiago Canyon College": 4811,
    "Shasta College": 707,
    "Sierra College": 102,
    "Skyline College": 713,
    "Solano Community College": 715,
    "Southwestern College": 720,
    "Taft College": 727,
    "Ventura College": 738,
    "Victor Valley College": 740,
    "West Los Angeles College": 63,
    "West Valley College": 745,
    "Woodland Community College": 8023,
    "Yuba College": 757
}

def _getGreatestMatching(queryCollegeName:str):
    """
    Using a provided college name, returns the corresponding CVC college ID.
    Jaro is a distance metric that considers the number of matching characters and the number of transpositions.
    Jaro-Winkler is a variation of Jaro that gives more weight to matching characters at the beginning of the strings.
    Jaro-Winkler will be used if no exact matching in queryCollegeName is found in the collegeIdDict.

    Parameters:
    queryCollegeName (str): The college name whose ID to find.

    Returns:
    int: The corresponding CVC college ID of the user inputted college name.
    """
    bestMatchID = collegeIdDict['Yuba College']
    bestMatchScore = 0
    bestMatchName = "Yuba College"
    collegeNameList = list(collegeIdDict.keys())
    if queryCollegeName in collegeNameList:
        return collegeIdDict[queryCollegeName]
    queryCompareName = queryCollegeName.lower().replace(" ","")
    for name in collegeNameList:
        compareName = name.lower().replace(" ","")
        score = textdistance.jaro_winkler(compareName,queryCompareName)
        if bestMatchScore < score:
            bestMatchScore = score
            bestMatchID = collegeIdDict[name]
            bestMatchName = name
            # print(bestMatchName)
    # print(bestMatchName)
    return bestMatchID
