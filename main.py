# this is very quickly thrown together
# ignore bad coding practices and messy code

import requests
import re

def extract_carried(content: str):
    ec_match = re.search(r'name="carried_ec".*?value="(-?\d+)"', content)
    soc_match = re.search(r'name="carried_soc".*?value="(-?\d+)"', content)

    ec_value = ec_match.group(1) if ec_match else None
    soc_value = soc_match.group(1) if soc_match else None

    return ec_value, soc_value

def post(payload):
    print(payload)
    response = requests.post("https://politicalcompass.org/test/en", data=payload)

    return response
    # print(response.text)
    #
    # carried = extract_carried(response.text)
    #
    # print(carried[0])
    # print(carried[1])
    #
    # return carried

def load_responses():
    with open("responses.txt") as f:
        return [line.strip() for line in f]

# this function/regexes were from ChatGPT
def get_political_compass_axes(text):
    # print(text)

    ec_match = re.search(r"Economic Left/Right:\s*([-+]?\d+(?:\.\d+)?)", text, re.IGNORECASE)

    soc_match = re.search(r"Social Libertarian/Authoritarian:\s*([-+]?\d+(?:\.\d+)?)", text, re.IGNORECASE)

    if not ec_match or not soc_match:
        raise ValueError("Could not find Political Compass scores.")

    return {
        "economic": float(ec_match.group(1)),
        "social": float(soc_match.group(1)),
    }

PAGES = [
    [
        "globalisationinevitable",
        "countryrightorwrong",
        "proudofcountry",
        "racequalities",
        "enemyenemyfriend",
        "militaryactionlaw",
        "fusioninfotainment"
    ],
    [
        "classthannationality",
        "inflationoverunemployment",
        "corporationstrust",
        "fromeachability",
        "freermarketfreerpeople",
        "bottledwater",
        "landcommodity",
        "manipulatemoney",
        "protectionismnecessary",
        "companyshareholders",
        "richtaxed",
        "paymedical",
        "penalisemislead",
        "freepredatormulinational"
    ],
    [
        "abortionillegal",
        "questionauthority",
        "eyeforeye",
        "taxtotheatres",
        "schoolscompulsory",
        "ownkind",
        "spankchildren",
        "naturalsecrets",
        "marijuanalegal",
        "schooljobs",
        "inheritablereproduce",
        "childrendiscipline",
        "savagecivilised",
        "abletowork",
        "represstroubles",
        "immigrantsintegrated",
        "goodforcorporations",
        "broadcastingfunding"
    ],
    [
        "libertyterrorism",
        "onepartystate",
        "serveillancewrongdoers",
        "deathpenalty",
        "societyheirarchy",
        "abstractart",
        "punishmentrehabilitation",
        "wastecriminals",
        "businessart",
        "mothershomemakers",
        "plantresources",
        "peacewithestablishment"
    ],
    [
        "astrology",
        "moralreligious",
        "charitysocialsecurity",
        "naturallyunlucky",
        "schoolreligious"
    ],
    [
        "sexoutsidemarriage",
        "homosexualadoption",
        "pornography",
        "consentingprivate",
        "naturallyhomosexual",
        "opennessaboutsex"
    ]
]

responses = load_responses()

i = 0
carried_ec = ""
carried_soc = ""

for page_num, questions in enumerate(PAGES, start=1):
    payload = {
        "page": str(page_num),
        "carried_ec": carried_ec,
        "carried_soc": carried_soc,
        "populated": "",
    }

    for question in questions:
        payload[question] = responses[i]
        i += 1

    response = post(payload)

    if page_num == len(PAGES):
        axes = get_political_compass_axes(response.text)
        print(f"Axes: {axes}")
    else:
        carried_ec, carried_soc = extract_carried(response.text)
        print(f"Eco: {carried_ec}, Social: {carried_soc}")

    # carried_ec, carried_soc = post(payload)

print("finished")
