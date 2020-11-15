from typing import Dict, List
from ripping_guide import RippingGuide


class RippingGuideCreator:

    def __init__(self, dvd_info={}, *args, **kwargs):
        self.guide = RippingGuide()
        self.dvd_info = dvd_info

    def print_title_and_chapter_info(self, only_title=None, show_chapters=True):
        for title_index, title in enumerate(self.dvd_info['tracks']):
            if only_title and str(title['track']) != only_title:
                continue
            print(f"Title {title['track']} ({title['length']})")
            if show_chapters:
                for chapter_index, chapter in enumerate(self.dvd_info['tracks'][title_index]['chapters']):
                    print(f"\tChapter {chapter['chapter']} ({chapter['length']})")

    def create_ripping_guide(self) -> RippingGuide:
        # Here is a visual of the structure we are building.
        self.guide.set_disc_id(self.dvd_info['dvd']['dvdread id'])

        def ask_disc_composition() -> str:
            print('Is this disc contain:')
            print('\n1) One or more movies')
            print('2) Episodes from a show')
            print('3) Some mixture of the above\n')
            response = input('-> ')
            if response == '1':
                return 'movie'
            elif response == '2':
                return 'tv'
            elif response == '3':
                return 'mixture'
            else:
                print('\nInvalid response.\n')
                return ask_movie_or_tv()
        
        data_gathering_method = {
            'movie': self.get_feature_data,
            'tv': self.get_episode_data,
            'mixture': self.get_feature_and_episode_data,
        }.get(ask_disc_composition())
        data_gathering_method()

        return self.guide

    def get_feature_and_episode_data(self):
        print("Ok, let's focus on the movie part first.")
        self.get_feature_data()
        print("Now that that's out of the way, lets talk shows.")
        self.get_episode_data()

    def get_episode_data(self):
        def ask_season() -> str:
            return input('Season #: ').strip().zfill(2)

        def ask_episodes() -> List[str]:
            response = input('Episode #s comma separated (ex: "1,2,3,4,5"): ').strip().replace(' ', '')
            episodes = [number.zfill(2) for number in sorted(list(set(response.split(','))))]
            return episodes

        episodes = []

        all_episodes_collected = False
        print("Don't worry if there are multiple seasons on this disc, we'll get them all.")
        while not all_episodes_collected:
            show_title = input("What's the name of the show? ").strip()
            if not self.guide.title:
                self.guide.set_title(show_title)

            season = ask_season()
            episode_numbers = ask_episodes()
            for episode_number in sorted(episode_numbers):
                self.print_title_and_chapter_info(show_chapters=False)
                disc_title = input(f'What title of the disc contains episode {episode_number}? ')
                self.print_title_and_chapter_info(only_title=disc_title)
                disc_chapters = input(f'Which chapters of title {disc_title} make up episode {episode_number}? (example: 1-5) ')
                episode = {
                    'show_title': show_title,
                    'season': season,
                    'episode': episode_number,
                    'filename': f'{show_title}.S{season}.E{episode_number}.m4v',
                    'title': disc_title,
                    'chapters': disc_chapters
                }
                self.guide.add_episode(episode)
            all_episodes_collected = not (input('\nDoes this disc have episodes from another show or season? [y/n]').lower() == 'y')

    def get_feature_data(self):
        features = []
        all_features_collected = False
        while not all_features_collected:
            if not features:
                feature_title = input('What is the title of the main (or only) movie on this disc? ').strip()
                self.guide.set_title(feature_title)
            else:
                feature_title = input('What is the title of the next movie on this disc? ').strip()
            self.print_title_and_chapter_info(show_chapters=False)
            disc_title = input(f'What title of the disc contains the feature? ')
            self.print_title_and_chapter_info(only_title=disc_title)
            disc_chapters = input(f'Which chapters of title {disc_title} make up the feature? (example: 1-5) ')
            feature = {
                'feature_title': feature_title,
                'filename': f'{feature_title}.m4v',
                'title': disc_title,
                'chapters': disc_chapters,
            }

            if self.ask_if_there_are_special_features():
                feature['special_features'] = self.get_special_feature_data()

            self.guide.add_feature(feature)
            all_features_collected = not (input('\nDoes this disc have another feature? [y/n]').lower() == 'y')

    def ask_if_there_are_special_features(self) -> bool:
        print('\nAre there special features?')
        print('1) Yes')
        print('2) No')
        print("3) Yes, but I don't want them.\n")
        response = input('-> ')
        if response == '1':
            return True
        elif response == '2':
            return False
        elif response == '3':
            # TODO: This response should be put into the ripping guide in
            # a way that indicates that the guide may not be complete, or
            # could otherwise be improved upon.
            return False
        else:
            print('\nInvalid response.\n')
            return self.ask_if_there_are_special_features()

    def get_special_feature_data(self) -> List[Dict]:
        def ask_special_feature_title() -> str:
            return input('Special Feature Title: ').strip()

        def ask_special_feature_type() -> str:
            print('\nWhat kind of special feature is this?')
            print('1) Behind the Scenes')
            print('2) Deleted Scene')
            print('3) Featurette')
            print('4) Interview')
            print('5) Scene')
            print('6) Short')
            print('7) Trailer')
            print("8) Other\n")
            response = input('-> ')

            # These are plex-style suffixes
            if response == '1':
                return '-behindthescenes'
            elif response == '2':
                return '-deleted'
            elif response == '3':
                return '-featurette'
            elif response == '4':
                return '-interview'
            elif response == '5':
                return '-scene'
            elif response == '6':
                return '-short'
            elif response == '7':
                return '-trailer'
            elif response == '8':
                return '-other'
            else:
                print('\nInvalid response.\n')
                return ask_special_feature_type()

        special_features = []
        all_special_features_collected = False
        while not all_special_features_collected:
            special_feature_title = ask_special_feature_title()
            special_feature_type = ask_special_feature_type()
            self.print_title_and_chapter_info(show_chapters=False)
            disc_title = input(f'What title of the disc contains the special feature? ')
            self.print_title_and_chapter_info(only_title=disc_title)
            disc_chapters = input(f'Which chapters of title {disc_title} make up the special feature? (example: 1-5) ')
            special_features.append({
                'special_feature_title': special_feature_title,
                'filename': f'{special_feature_title}{special_feature_type}.m4v',
                'title': disc_title,
                'chapters': disc_chapters,
            })
            all_special_features_collected = not (input('\nDoes this disc have another special feature? [y/n]').lower() == 'y')
        return special_features
