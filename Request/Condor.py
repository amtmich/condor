import requests
from datetime import datetime
from File.FileManager import FileManager

class Condor:
    def __init__(self, origin, destination, oneway=False, outboundDate=None, numberOfFlightDays=120):
        self.origin = origin
        self.destination = destination
        self.oneway = oneway
        self.outboundDate = outboundDate if outboundDate else datetime.today().strftime('%Y%m%d')
        self.numberOfFlightDays = numberOfFlightDays
        self.base_url = "https://www.condor.com/tca/rest/pl/vacancies/lowFareInformation"
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "cookie": (
                "gig_bootstrap_4_KlKTMxbRoyQsBxAHdOrgjw=myaccount_ver4; "
                "mt.v=2.107781936.1706542757451; baqend-speedkit-user-id=sQwGF9rnBk91LT4KNl0VyQM79; "
                "cjUser=4b2bb494-7de7-46e0-8562-b8b4474e0e66; FPID=FPID2.2.lkjzdjC%2BpXzbUiKNbA30QU0mPxuZoYXQ2rEkJrsLDQY%3D.1706542758; "
                "_fbp=fb.1.1706542762786.986654829; _cs_c=0; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22nugJJVA1c0TApRL6j1oM%22%7D; "
                "emcid=F-WK70ZnmR9; QSI_SI_2m0pjIPzZymhd6S_intercept=true; optimizelyEndUserId=oeu1712907637269r0.3878897448054124; "
                "_ga_43TGDLCQ9B=GS1.1.1712907637.1.1.1712907673.0.0.0; _gcl_au=1.1.590393541.1714379381; cjConsent=MXxZfDB8WXww; "
                "ga_utm_src=cj; ga_utm_md=aff; ga_utm_cn=perf_campaign-id; _evga_3e4d={%22uuid%22:%223d6b760aba83f90f%22}; "
                "_sfid_ea41={%22anonymousId%22:%223d6b760aba83f90f%22,%22consents%22:[]}; _gid=GA1.2.347664274.1716881162; "
                "FPLC=6LXWVvsjNIR7QRDuGSLkYucORuKFDQzasMhd1cl5cedb%2B7CYBBFhhKLO4sNgNi%2BAjs1ZLu9ztaKhYVDq7L9UIcer9M9DEj2l2IkWNt7wOUOsRfYOSJrzSJTthuAn3g%3D%3D; "
                "cjevent_dc=4af85db91cc411ef810802b50a18ba72; _uetsid=ae3200901cc311efb545d9146d51ec1a; _uetvid=e91a47209a4f11ee9192d52cd41f5f77; "
                "RT=\"z=1&dm=www.condor.com&si=e610247e-997c-41d9-90ad-129bc830fefd&ss=lwqmpfoq&sl=0&tt=0\"; bstag=sDw-xbGEyZTRjLcTDpWy; "
                "bstag.pub=sDw-xbGEyZTRjLcTDpWy; ga_laMa=pl; _ga=GA1.2.513062555.1706542758; kifcc_52045=1; _dc_gtm_UA-40916028-3=1; "
                "_dc_gtm_UA-40916028-9=1; _gali=originAirport; _cs_id=7d0d4901-d9fd-a298-d8d5-e7d0dd712aca.1706542764.79.1716914957.1716914741.1.1740706764153.1; "
                "_cs_s=11.0.0.1716916757175; _ga_FPR0JQ8CJX=GS1.1.1716914741.85.1.1716914957.0.0.222065817"
            ),
            "priority": "u=1, i",
            "referer": "https://www.condor.com/pl",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }

    def get_name(self):
        return f"{self.origin}_{self.destination}_{'oneway' if self.oneway else 'return'}"

    def format_url(self):
        return (
            f"{self.base_url}?origin={self.origin}&destination={self.destination}&outboundDate={self.outboundDate}&"
            f"numberOfFlightDays={self.numberOfFlightDays}&currency=EUR&oneway={'true' if self.oneway else 'false'}&isOutbound=true"
        )

    def execute_request(self):
        url = self.format_url()
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()
    
    def create_file_manager(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y-%m-%d")
        file_name = f"{formatted_date}.json"
        file_manager = FileManager(self.get_name(), file_name)
        return file_manager
    

# Example usage:
#flight_info = Condor(origin='DRS', destination='PUJ', oneway=False)
#print(flight_info.get_name())
#response = flight_info.execute_request()
#print(response)
