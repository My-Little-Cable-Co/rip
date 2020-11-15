import json
import os
import subprocess
import sys

from pathlib import Path
from typing import List, Dict

from ripping_guide import RippingGuide
from ripping_guide_creator import RippingGuideCreator


DRIVE_PATH_CANDIDATES = ['/dev/rdisk2', '/dev/disk1', '/dev/disk2', '/dev/sr0', '/dev/sr1', '/dev/rdisk0', '/dev/rdisk1']


class Rip:

    def __init__(self, *args, **kwargs):
        self.multi_feature_disc = False
        self.dvd_info = None

    def requirements_check(self) -> bool:
        requirements_met = True
        try:
            result = subprocess.run(['dvd_info', '--version'], capture_output=True, text=True)
        except FileNotFoundError:
            print("ERROR, dependency not found: This program requires the 'dvd_info' binary to be in the PATH.")
            requirements_met = False
        try:
            result = subprocess.run(['HandBrakeCLI', '--version'], capture_output=True, text=True)
        except FileNotFoundError:
            print("ERROR, dependency not found: This program requires the 'HandBrakeCLI' binary to be in the PATH.")
            requirements_met = False
        return requirements_met

    def handbrake(self, drive_path, title, chapters, filename, preset='Fast 480p30'):
        handbrake_process_arguments = [
            'HandBrakeCLI',
            '--preset', preset,
            '--decomb',
            '--markers',
            '--encoder', 'x264',
            '--title', title,
            '--chapters', chapters,
            '-i', drive_path,
            '-o', filename
        ]
        print(f'\n\nNow Ripping: {filename}\n\n')
        subprocess.run(handbrake_process_arguments, text=True)

    def rip_from(self, ripping_guide, drive_path):
        dvd_rip_dir = f"{Path.home()}/dvd_rips"
        Path(dvd_rip_dir).mkdir(parents=True, exist_ok=True)
        for ripable in ripping_guide.ripables():
            ripable_parent_directories = f"{dvd_rip_dir}/{'/'.join(ripable.file_path.split('/')[0:-1])}"
            Path(ripable_parent_directories).mkdir(parents=True, exist_ok=True)
            self.handbrake(drive_path, ripable.disc_title, ripable.disc_chapters, f"{dvd_rip_dir}/{ripable.file_path}")

        print('\n\nRipping Complete\n\n')

    def ripping_guide_path_from_disc_id(self, disc_id: str) -> str:
        # Intention: to limit the number of files in each directory while
        # maintaining the ability to know a file path given a disc id.
        #
        # input: 'edaf369980557bbb26ccfdddd0e8198b'
        # output: 'ed/af/36/edaf369980557bbb26ccfdddd0e8198b.ripping-guide.json'
        subdirectories = f"{disc_id[0:2]}/{disc_id[2:4]}/{disc_id[4:6]}"
        return f"{subdirectories}/{disc_id}.ripping-guide.json"

    def main(self):
        title = """

    @@@@@@@            @@@           @@@@@@@   
    @@@@@@@@           @@@           @@@@@@@@  
    @@!  @@@           @@!           @@!  @@@  
    !@!  @!@           !@!           !@!  @!@  
    @!@!!@!            !!@           @!@@!@!   
    !!@!@!             !!!           !!@!!!    
    !!: :!!            !!:           !!:       
    :!:  !:!           :!:           :!:       
    ::   :::            ::            ::       
     :   : :           :              :        
                                               
        """
        print(title)

        print('Checking requirements...', end =" ")
        if not self.requirements_check():
            print("\nRequirements not met, exiting.\n")
            sys.exit(1)
        else:
            print("ok.")

        drive_path = None
        disc_id = None
        disc_title = None

        print('Gathering disc information, this could take a moment.')
        for drive_path_candidate in DRIVE_PATH_CANDIDATES:
            print(f'Looking for a disc in {drive_path_candidate}...')
            result = subprocess.run(['dvd_info', '--json', drive_path_candidate], capture_output=True, text=True)
            if result.stdout and not result.stderr:
                drive_path = drive_path_candidate
                dvd_info_output = result.stdout
                dvd_info_output_json = ''.join([line for line in dvd_info_output.splitlines() if not line.startswith('libdvdread: ')])
                self.dvd_info = json.loads(dvd_info_output_json)
                disc_id = self.dvd_info['dvd']['dvdread id']
                disc_title = self.dvd_info['dvd']['title'] or 'Unknown Title'
                break

        if not drive_path:
            print(f'Could not find disc at any of the following locations: {", ".join(DRIVE_PATH_CANDIDATES)}')
            print('Ensure a disc is inserted, or specify the drive path as an argument.')
            print('Example:')
            print('python3 rip/start.py /special/disc/path')
            sys.exit(1)
        
        print(f'Found volume "{disc_title}" with id "{disc_id}" at {drive_path}')

        ripping_guide = None
        ripping_guide_dir = f"{Path.home()}/dvd_ripping_guides"
        Path(ripping_guide_dir).mkdir(parents=True, exist_ok=True)

        expected_path_to_guide = self.ripping_guide_path_from_disc_id(disc_id)

        ripping_guide_file_path = Path(f"{ripping_guide_dir}/{expected_path_to_guide}")
        if ripping_guide_file_path.is_file():
            ripping_guide = RippingGuide.from_path(ripping_guide_file_path)

        if not ripping_guide:
            should_create_ripping_guide = input('\nCreate a ripping guide? [y/n]: ').lower() == 'y'
            if should_create_ripping_guide:
                # create a ripping guide
                ripping_guide = RippingGuideCreator(self.dvd_info).create_ripping_guide()

                ripping_guide_file_parent_directory = str(ripping_guide_file_path.parent)
                Path(ripping_guide_file_parent_directory).mkdir(parents=True, exist_ok=True)
                with open(ripping_guide_file_path, "w") as exported_ripping_guide:
                    exported_ripping_guide.write(ripping_guide.to_json())

        rip_from_guide = False
        if ripping_guide:
            print('Please review the ripping guide:\n')
            for ripable in ripping_guide.ripables():
                print(ripable)

            rip_from_guide = input('\nRip the disc based on this guide? [y/n]').lower() == 'y'

        if rip_from_guide:
            self.rip_from(ripping_guide, drive_path)
