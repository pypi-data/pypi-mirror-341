import os
import subprocess
from datetime import datetime, timedelta
from getpass import getpass

LA1 = {
    'NLDAS': 25.025,
    'GLDAS': -999,
}
LO1 = {
    'NLDAS': -124.9375,
    'GLDAS': -999,
}
DI = {
    'NLDAS': 0.125,
    'GLDAS': -999,
}
DJ = {
    'NLDAS': 0.125,
    'GLDAS': -999,
}

IND_J = lambda ldas, lat: int(round((lat - LA1[ldas]) / DJ[ldas]))
IND_I = lambda ldas, lon: int(round((lon - LO1[ldas]) / DI[ldas]))

T0 = {
    'NLDAS': datetime(1979, 1, 1, 13),
    'GLDAS': datetime(2000, 1, 1, 0),
}
DT = {
    'NLDAS': 3600,
    'GLDAS': 10800,
}
IND_T = lambda ldas, t: int((t - T0).total_seconds() / 3600)

URS = 'urs.earthdata.nasa.gov'    # Earthdata URL to call for authentication

def get_weather_file(ldas, lat, lon, start_year, end_year):
    prompts = ['Enter NASA Earthdata Login Username \n(or create an account at urs.earthdata.nasa.gov): ',
            'Enter NASA Earthdata Login Password: ']

    with open(os.path.expanduser("~") + os.sep + '.netrc', 'w') as file:
        file.write('machine {} login {} password {}'.format(URS, getpass(prompt=prompts[0]), getpass(prompt=prompts[1])))
        file.close()

    #USER_NAME = 'yzs123'
    #PASSWORD = 'm+H_rrxJF2m-jKC'

    for year in range(start_year, end_year):
        url = f'https://hydro1.gesdisc.eosdis.nasa.gov:443/dods/NLDAS_FORA0125_H.002.ascii?tmp2m[{max(0, IND_T(datetime(1979, 1, 1)))}:{IND_T(datetime(2024, 7, 14))}][{IND_J(LATITUDE)}][{IND_I(LONGITUDE)}]'
        #url = f'https://hydro1.gesdisc.eosdis.nasa.gov:443/dods/NLDAS_FORA0125_H.002.ascii?tmp2m[{1}:{100}][{1}][{1}]'
        commands = [
            'wget',
            '--load-cookies',
            '.urs_cookies',
            '--save-cookies',
            '.urs_cookies',
            '--keep-session-cookies',
            '{url}',
            '-O',
            'nldas.txt',
        ]

        subprocess.run(commands)
