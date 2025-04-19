import os
import FreeSimpleGUI as sg
from loguru import logger
import configparser
from pathlib import Path
import subprocess

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        return config['DEFAULT']['MergecapPath']
    except KeyError:
        sg.popup_error('MergecapPath not found in config.ini. Please configure it.')
        return ''

def main():
    sg.theme('SystemDefault')
    mergecap_path = load_config()
    layout = [
        [sg.Text('Mergecap.exe Path:', expand_x=True), ],
        [sg.Input(mergecap_path, key='-MERGECAP-', size=(60,1), disabled=True, expand_x=True), sg.Button('Change Mergecap')],
        [sg.Text('Select PCAP Folder', expand_x=True)],
        [sg.Input(expand_x=True), sg.FolderBrowse(key='-FOLDER-')],
        [sg.Text('Output File', expand_x=True)],
        [sg.Input(expand_x=True), sg.FileSaveAs(key='-OUTPUT-')],
        [sg.Button('Merge'), sg.Button('Exit')],
        [sg.Text('Generated Command:', expand_x=True)],
        [sg.Multiline('', size=(100, 30), key='-CMD-', disabled=True, expand_x=True)]
    ]

    window = sg.Window('PCAP Merger', layout)

    def to_win_path(p):
        return str(Path(p).as_posix())
    def quote_path(p):
        return f'"{to_win_path(p)}"'
    
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        if event == 'Change Mergecap':
            new_path = sg.popup_get_file('Select mergecap.exe', file_types=(('mergecap.exe', '*.exe'),), no_window=True)
            if new_path:
                # Always store the quoted path in config.ini and update the GUI
                quoted_new_path = f'"{Path(new_path).as_posix()}"'
                config = configparser.ConfigParser()
                config.read('config.ini')
                config['DEFAULT']['MergecapPath'] = quoted_new_path
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                window['-MERGECAP-'].update(quoted_new_path)
        if event == 'Merge':
            input_folder = values['-FOLDER-']
            output_file = values['-OUTPUT-']
            mergecap_path = values['-MERGECAP-']
            if not input_folder or not output_file:
                sg.popup_error('Please specify both input folder and output file')
                continue

            # Normalize input folder path
            input_folder_path = Path(input_folder)
            input_files = [str(f) for f in input_folder_path.iterdir() if f.suffix in ('.cap', '.pcap') and f.is_file()]
            if not input_files:
                sg.popup_error('No PCAP files found in the selected folder')
                continue


            if output_file.startswith('"') and output_file.endswith('"'):
                output_file_path = output_file
            else:
                output_file_path = quote_path(output_file)
            input_files_paths = [quote_path(f) for f in input_files]
            command = f'{mergecap_path} -w {output_file_path} ' + ' '.join(input_files_paths) 
            window['-CMD-'].update(command)
            # Single quotation marks won't do in that case. You have to add quotation marks around each path and also enclose the whole command in quotation marks
            subprocess.Popen(f'start cmd /k "echo {command} & {command} & pause"', shell=True)


    window.close()

if __name__ == '__main__':
    main()