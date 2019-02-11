import requests
import time
import configparser


class NoLightsFound(Exception):
    pass


class Hue:

    def _get_all_lights(self):
        r = requests.get(f'{self.base_url}/lights')
        if r.status_code != 200:
            raise NoLightsFound('Cannot find any light!')

        response = r.json()

        if response[0] and 'error' in response[0]:
            raise NoLightsFound(f'Cannot reach lights: {response[0]["error"]["description"]}')
        return response

    def _toggle_light(self, ligth_id, state):
        if state not in [True, False]:
            raise ValueError(f'Cannot set light {ligth_id} state to {state}')

        body = {'on': state}
        response = requests.put(f'{self.base_url}/lights/{ligth_id}/state', json=body).json()

        if response[0] and 'error' in response[0]:
            raise ValueError(f'Error changing status for light {ligth_id}: {response[0]["error"]["description"]}')
        return response

    def __init__(self, ip, user):
        self.base_url = f'http://{ip}/api/{user}'
        self.lights = self._get_all_lights()

    def toggle_all_lights(self, interval):
        for state in [True, False, True]:
            for ligth_id in self.lights.keys():
                self._toggle_light(ligth_id, state)

            time.sleep(interval)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('../config.ini')

    hue = Hue(config['ALL']['bridge_ip_address'], config['ALL']['hue_user'])
    hue.toggle_all_lights(0.2)

