import os
import requests
import datetime

def save_response(response, folder, filename):
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w') as file:
        file.write(response)
    print(f"Saved response to {filepath}")

def make_requests(origin, destination):
    today = datetime.datetime.now().strftime('%Y%m%d')
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=1, i",
        "referer": "https://www.condor.com/pl",
        "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    cookies = {
        "gig_bootstrap_4_KlKTMxbRoyQsBxAHdOrgjw": "myaccount_ver4",
        "mt.v": "2.107781936.1706542757451",
        "baqend-speedkit-user-id": "sQwGF9rnBk91LT4KNl0VyQM79",
        "cjUser": "4b2bb494-7de7-46e0-8562-b8b4474e0e66",
        "FPID": "FPID2.2.lkjzdjC%2BpXzbUiKNbA30QU0mPxuZoYXQ2rEkJrsLDQY%3D.1706542758",
        "_fbp": "fb.1.1706542762786.986654829",
        "_cs_c": "0",
        "__rtbh.lid": "%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22nugJJVA1c0TApRL6j1oM%22%7D",
        "emcid": "F-WK70ZnmR9",
        "QSI_SI_2m0pjIPzZymhd6S_intercept": "true",
        "optimizelyEndUserId": "oeu1712907637269r0.3878897448054124",
        "_ga_43TGDLCQ9B": "GS1.1.1712907637.1.1.1712907673.0.0.0",
        "_gcl_au": "1.1.590393541.1714379381",
        "cjConsent": "MXxZfDB8WXww",
        "ga_utm_src": "cj",
        "ga_utm_md": "aff",
        "ga_utm_cn": "perf_campaign-id",
        "_evga_3e4d": "{%22uuid%22:%223d6b760aba83f90f%22}",
        "_sfid_ea41": "{%22anonymousId%22:%223d6b760aba83f90f%22,%22consents%22:[]}",
        "cjevent_dc": "4af85db91cc411ef810802b50a18ba72",
        "_gid": "GA1.2.1777636765.1717150080",
        "FPLC": "4ZfnZ3fsayC3Xbi7dWUb3XsFvwDxTuFS0Yn8Eu53ac9RR5EQt4qgAUk%2Fw9tYKm5wdNrAgLDBoEKaFTiVK9Lnx25U8kU%2Bp7mRWGyghu54nKoJ0LHBWEm0uPBElSSNnQ%3D%3D",
        "_uetsid": "d2047a501f3511efa3293569cefc6170",
        "_uetvid": "e91a47209a4f11ee9192d52cd41f5f77",
        "bstag": "fAWTpr2f2w9sWlR6Iz_u",
        "bstag.pub": "fAWTpr2f2w9sWlR6Iz_u",
        "ga_laMa": "pl",
        "_ga": "GA1.2.513062555.1706542758",
        "kifcc_52045": "1",
        "_cs_id": "7d0d4901-d9fd-a298-d8d5-e7d0dd712aca.1706542764.82.1717221009.1717220707.1.1740706764153.1",
        "_cs_s": "5.0.0.1717222809938",
        "_ga_FPR0JQ8CJX": "GS1.1.1717220707.88.1.1717221010.0.0.1473533926",
        "RT": "^\"z=1&dm=www.condor.com&si=e610247e-997c-41d9-90ad-129bc830fefd&ss=lwvovbxd&sl=1&tt=3am&rl=1^\""
    }
    
    folder_name = f"{origin}_{destination}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Round trip
    url_roundtrip = f"https://www.condor.com/tca/rest/pl/vacancies/lowFareInformation?origin={origin}&destination={destination}&outboundDate={today}&numberOfFlightDays=360&currency=EUR&oneway=false&isOutbound=true"
    response_roundtrip = requests.get(url_roundtrip, headers=headers, cookies=cookies)
    save_response(response_roundtrip.text, folder_name, f"{today}_{origin}_{destination}_roundtrip.json")
    
    # One way
    url_oneway = f"https://www.condor.com/tca/rest/pl/vacancies/lowFareInformation?origin={origin}&destination={destination}&outboundDate={today}&numberOfFlightDays=360&currency=EUR&oneway=true&isOutbound=true"
    response_oneway = requests.get(url_oneway, headers=headers, cookies=cookies)
    save_response(response_oneway.text, folder_name, f"{today}_{origin}_{destination}_oneway.json")
    
    # Reverse one way
    url_reverse_oneway = f"https://www.condor.com/tca/rest/pl/vacancies/lowFareInformation?origin={destination}&destination={origin}&outboundDate={today}&numberOfFlightDays=360&currency=EUR&oneway=true&isOutbound=true"
    response_reverse_oneway = requests.get(url_reverse_oneway, headers=headers, cookies=cookies)
    save_response(response_reverse_oneway.text, folder_name, f"{today}_{destination}_{origin}_oneway.json")

def fetch_flight_data(pairs):
    for origin, destination in pairs:
        print(f"Processing: {origin} to {destination}")
        make_requests(origin, destination)

# Example usage:
pairs = [
            ('WRO', 'PUJ'),
        ('WAW', 'PUJ'),
        ('GDN', 'PUJ'),
        ('KRK', 'PUJ'),
        ('POZ', 'PUJ'),
        ('KTW', 'PUJ'),
        ('FRA', 'PUJ'),
        ('BER', 'PUJ'),
        ('MUC', 'PUJ'),
        ('LUX', 'PUJ'),
        ('PRG', 'PUJ'),
        ('DRS', 'PUJ'),
        ('LEJ', 'PUJ'),
        ('HAM', 'PUJ'),
        ('HAJ', 'PUJ'),
        ('NUE', 'PUJ'),
        ('STR', 'PUJ'),
        ('ZRH', 'PUJ'),
        ('DUS', 'PUJ'),
        ('FMO', 'PUJ'),
        ('VNO', 'PUJ'),
        ('GRZ', 'PUJ'),
        ('INN', 'PUJ'),
        ('SZG', 'PUJ'),
        ('VIE', 'PUJ'),
        ('BUD', 'PUJ'),
        ('BSL', 'PUJ')
] # Add more pairs as needed
fetch_flight_data(pairs)
