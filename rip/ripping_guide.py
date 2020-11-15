import json

from pathlib import Path
from typing import Dict, List, Optional
from jsonschema.validators import validator_for

from ripping_guide_schema import RIPPING_GUIDE_SCHEMA


class Ripable:
    def __init__(self, name, disc_title, disc_chapters, file_path):
        self.name = name
        self.disc_title = disc_title
        self.disc_chapters = disc_chapters
        self.file_path = file_path

    def __str__(self) -> str:
        return f'{self.name}: Title {self.disc_title}, Chapter(s) {self.disc_chapters}, saving to "{self.file_path}".'

class RippingGuide:

    def __init__(self, ripping_guide_dict={}, *args, **kwargs):
        self._ripping_guide_dict = ripping_guide_dict

    def set_disc_id(self, disc_id):
        self._ripping_guide_dict['disc_id'] = str(disc_id)

    def set_title(self, title):
        self._ripping_guide_dict['title'] = str(title)

    @staticmethod
    def from_json(json_string) -> Optional['RippingGuide']:
        # ensure the string is parsable JSON
        try:
            ripping_guide_dict = json.loads(json_string)
        except json.decoder.JSONDecodeError:
            print('ERROR: File contents were not valid JSON.')
            return None

        # ensure the JSON conforms to the Ripping Guide Schema
        validator_class = validator_for(RIPPING_GUIDE_SCHEMA)
        validator = validator_class(RIPPING_GUIDE_SCHEMA)
        if not validator.is_valid(instance=ripping_guide_dict):
            print(ripping_guide_dict)
            print('ERROR: JSON did not adhere to Ripping Guide schema.')
            return None

        return RippingGuide(ripping_guide_dict=ripping_guide_dict)

    @staticmethod
    def retrieve_from_internet(disc_id) -> Optional['RippingGuide']:
        raise NotImplementedError('This method is TBD')
        # ripping_guide_response = requests.get(f'https://example.com/{disc_id}')
        # if ripping_guide_response.status_code == 200:
        #     RippingGuide.from_json(ripping_guide_response.json())

    @staticmethod
    def from_path(file_path) -> Optional['RippingGuide']:
        file_candidate = Path(file_path)
        if not file_candidate.is_file():
            return None
        return RippingGuide.from_json(file_candidate.read_text())

    def to_json(self) -> str:
        return json.dumps(self._ripping_guide_dict, indent=2)

    @property
    def title(self) -> Optional[str]:
        return self._ripping_guide_dict.get('title')

    @property
    def features(self) -> List[Dict]:
        return self._ripping_guide_dict.get('features', [])

    @property
    def episodes(self) -> List[Dict]:
        return self._ripping_guide_dict.get('episodes', [])

    def add_feature(self, feature: Dict):
        if 'features' not in self._ripping_guide_dict:
            self._ripping_guide_dict['features'] = []
        self._ripping_guide_dict['features'].append(feature)

    def add_episode(self, episode: Dict):
        if 'episodes' not in self._ripping_guide_dict:
            self._ripping_guide_dict['episodes'] = []
        self._ripping_guide_dict['episodes'].append(episode)

    def ripables(self) -> List[Ripable]:
        things_to_rip = []
        for feature in self.features:
            feature_ripable = Ripable(
                name=feature['feature_title'],
                disc_title=feature['title'],
                disc_chapters=feature['chapters'],
                file_path=f"{feature['feature_title']}/{feature['filename']}"
            )
            things_to_rip.append(feature_ripable)
            for special_feature in feature.get('special_features', []):
                special_feature_ripable = Ripable(
                    name=special_feature['special_feature_title'],
                    disc_title=special_feature['title'],
                    disc_chapters=special_feature['chapters'],
                    file_path=f"{feature['feature_title']}/{special_feature['filename']}"
                )
                things_to_rip.append(special_feature_ripable)
        for episode in self.episodes:
            episode_ripable = Ripable(
                name=' '.join(episode['filename'].split('.')[0:-1]),
                disc_title=episode['title'],
                disc_chapters=episode['chapters'],
                file_path=f"{episode['show_title']}/Season {episode['season']}/{episode['filename']}"
            )
            things_to_rip.append(episode_ripable)
        return things_to_rip
