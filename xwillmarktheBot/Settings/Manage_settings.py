from shutil import copyfile


def create_settings():
    copyfile(r'xwillmarktheBot/Settings/Settings_template.py', r'Settings.py')


def copy_settings():
    copyfile('Settings.py', r'xwillmarktheBot/Settings/Settings.py')