import regex
import requests

URL_TOKEN = "https://api.europace.de/auth/access-token/"
URL_DICT = {"ehyp": "https://api.ehyp.de/case/v2/cases/",
            "europace": "https://baufinanzierung.api.europace.de/kundenangaben/"}

def get_token(con_id: str, con_secret: str):
    header = {"content-type": "application/x-www-form-urlencoded"}

    token_creds = {"client_id": con_id,
                   "client_secret": con_secret,
                   "grant_type": "client_credentials"}

    token_gen = requests.post(url=URL_TOKEN, headers=header, data=token_creds)

    token_json = token_gen.json()

    return token_json['access_token']

def map_to_euro(data_to_map: dict, data_structure: dict):
    # mapping, values 1:1
    data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['personendaten']['person']['vorname'] = data_to_map['applicants'][0]['personalData']['fname']
    data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['personendaten']['person']['nachname'] = data_to_map['applicants'][0]['personalData']['lname']
    data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['personendaten']['geburtsort'] = data_to_map['applicants'][0]['personalDataDetails']['birthCity']
    data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['personendaten']['geburtsdatum'] = data_to_map['applicants'][0]['personalData']['birthdate']
    data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['personendaten']['staatsangehoerigkeit'] = data_to_map['applicants'][0]['personalData']['nationality']
    data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['finanzielles']['steuerId'] = data_to_map['applicants'][0]['personalDataDetails']['taxId']
    data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['wohnsituation']['anschrift']['plz'] = data_to_map['applicants'][0]['personalData']['zip']
    data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['wohnsituation']['anschrift']['ort'] = data_to_map['applicants'][0]['personalData']['city']

    # mapping, values not 1:1
    data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['personendaten']['person']['titel']['dr'] = True if data_to_map['applicants'][0]['personalData']['title'].lower() == ("dr" or "profdr") else False
    data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['personendaten']['person']['titel']['prof'] = True if data_to_map['applicants'][0]['personalData']['title'].lower() == ("prof" or "profdr") else False
    data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['wohnsituation']['anschrift']['strasse'] = data_to_map['applicants'][0]['personalData']['street'].split()[0]
    data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['wohnsituation']['anschrift']['hausnummer'] = data_to_map['applicants'][0]['personalData']['street'].split()[-1] if regex.search(regex.compile('^[0123456789]'), data_to_map['applicants'][0]['personalData']['street'].split()[-1]) else data_to_map['applicants'][0]['personalData']['street'].split()[-2]
    data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['kontakt']['telefonnummer']['vorwahl'] = "/"
    data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['kontakt']['telefonnummer']['nummer'] = data_to_map['applicants'][0]['personalData']['phoneDay']
    data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['personendaten']['person']['anrede'] = "HERR" if data_to_map['applicants'][0]['personalData']['sex'].lower() == "m" else "FRAU"

    match data_to_map['applicants'][0]['personalData']['maritalStatus']:
        case "ledig":
            data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['personendaten']['familienstand']['@type'] = "Ledig".upper()
        case "verheirt":
            data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['personendaten']['familienstand']['@type'] = "Verheiratet".upper()
        case "eingleben":
            data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['personendaten']['familienstand']['@type'] = "Lebenspartnerschaft".upper()
        case "zusammen":
            data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['personendaten']['familienstand']['@type'] = "Lebenspartnerschaft".upper()
        case "verwitwet":
            data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['personendaten']['familienstand']['@type'] = "Verwitwet".upper()
        case "geschieden":
            data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['personendaten']['familienstand']['@type'] = "Geschieden".upper()
        case "getrennt":
            data_structure['kundenangaben']['haushalte'][0]['kunden'][0]['personendaten']['familienstand']['@type'] = "GetrenntLebend".upper()

    return data_structure

def map_to_ehyp(data_to_map: dict, data_structure: dict):
    # mapping, values 1:1
    data_structure['applicants'][0]['personalData']['fname'] = data_to_map['haushalte'][0]['kunden'][0]['personendaten']['person']['vorname']
    data_structure['applicants'][0]['personalData']['lname'] = data_to_map['haushalte'][0]['kunden'][0]['personendaten']['person']['nachname']
    data_structure['applicants'][0]['personalData']['zip'] = data_to_map['haushalte'][0]['kunden'][0]['wohnsituation']['anschrift']['plz']
    data_structure['applicants'][0]['personalData']['city'] = data_to_map['haushalte'][0]['kunden'][0]['wohnsituation']['anschrift']['ort']
    data_structure['applicants'][0]['personalData']['birthdate'] = data_to_map['haushalte'][0]['kunden'][0]['personendaten']['geburtsdatum']
    data_structure['applicants'][0]['personalData']['nationality'] = data_to_map['haushalte'][0]['kunden'][0]['personendaten']['staatsangehoerigkeit']

    if "personalDataDetails" in data_structure['applicants'][0]:
        if "birthCity" in data_structure['applicants'][0]['personalDataDetails']:
            data_structure['applicants'][0]['personalDataDetails']['birthCity'] = data_to_map['haushalte'][0]['kunden'][0]['personendaten']['geburtsort']
        if "taxId" in data_structure['applicants'][0]['personalDataDetails']:
            data_structure['applicants'][0]['personalDataDetails']['taxId'] = data_to_map['haushalte'][0]['kunden'][0]['finanzielles']['steuerId']

    # mapping, value not 1:1
    data_structure['applicants'][0]['personalData']['street'] = data_to_map['haushalte'][0]['kunden'][0]['wohnsituation']['anschrift']['strasse'] + " " + data_to_map['haushalte'][0]['kunden'][0]['wohnsituation']['anschrift']['hausnummer']
    data_structure['applicants'][0]['personalData']['phoneDay'] = data_to_map['haushalte'][0]['kunden'][0]['kontakt']['telefonnummer']['vorwahl'] + " " + data_to_map['haushalte'][0]['kunden'][0]['kontakt']['telefonnummer']['nummer']
    data_structure['applicants'][0]['personalData']['sex'] = "M" if data_to_map['haushalte'][0]['kunden'][0]['personendaten']['person']['anrede'].lower() == "herr" else "F" 
    # country is not needed in this direction

    if "titel" in data_to_map['haushalte'][0]['kunden'][0]['personendaten']['person']:
        if "dr" in data_to_map['haushalte'][0]['kunden'][0]['personendaten']['person']['titel'] and "prof" in data_to_map['haushalte'][0]['kunden'][0]['personendaten']['person']['titel'] and data_to_map['haushalte'][0]['kunden'][0]['personendaten']['person']['titel']['dr'] == True and data_to_map['haushalte'][0]['kunden'][0]['personendaten']['person']['titel']['prof'] == True:
            data_structure['applicants'][0]['personalData']['title'] = "ProfDr"
        elif "dr" in data_to_map['haushalte'][0]['kunden'][0]['personendaten']['person']['titel'] and data_to_map['haushalte'][0]['kunden'][0]['personendaten']['person']['titel']['dr'] == True:
            data_structure['applicants'][0]['personalData']['title'] = "Dr"
        elif "prof" in data_to_map['haushalte'][0]['kunden'][0]['personendaten']['person']['titel'] and data_to_map['haushalte'][0]['kunden'][0]['personendaten']['person']['titel']['prof'] == True:
            data_structure['applicants'][0]['personalData']['title'] = "Prof"

    match data_to_map['haushalte'][0]['kunden'][0]['personendaten']['familienstand']['@type']:
        case "Ledig":
            data_structure['applicants'][0]['personalData']['maritalStatus'] = "ledig"
        case "Verheiratet":
            data_structure['applicants'][0]['personalData']['maritalStatus'] = "verheirt"
        case "Lebenspartnerschaft":
            data_structure['applicants'][0]['personalData']['maritalStatus'] = "eingleben"
        case "Verwitwet":
            data_structure['applicants'][0]['personalData']['maritalStatus'] = "verwitwet"
        case "Geschieden":
            data_structure['applicants'][0]['personalData']['maritalStatus'] = "geschieden"
        case "GetrenntLebend":
            data_structure['applicants'][0]['personalData']['maritalStatus'] = "getrennt"

    return data_structure

def get_customer(ops_no: str, acc_token: str, provider: str):
    header = {"content-type": "application/json; charset=UTF-8",
              "Authorization": f"Bearer {acc_token}"}

    url = URL_DICT['ehyp'] if provider == "ehyp" else URL_DICT['europace']

    return requests.get(url=f"{url}{ops_no}", headers=header).json()

def post_customer(data: dict, acc_token: str, provider: str):
    header = {"content-type": "application/json; charset=UTF-8",
              "Authorization": f"Bearer {acc_token}"}

    url = URL_DICT['europace'] if provider == "ehyp" else URL_DICT['ehyp']

    return requests.post(url=f"{url}", headers=header, json=data)