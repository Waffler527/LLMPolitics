# this is really messy and quickly thrown together
# ignore bad coding conventions and messy code

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

    print(response.text)

    carried = extract_carried(response.text)

    print(carried[0])
    print(carried[1])

    return carried

def load_responses():
    with open("responses.txt") as f:
        return [line.strip() for line in f]

PAGES = [
    [
        "globalisationinevitable",
        "countryrightorwrong",
        "proudofcountry",
        "racequalities",
        "enemyenemyfriend",
        "militaryactionlaw",
        "fusioninfotainment"
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

    carried_ec, carried_soc = post(payload)

print("finished")
