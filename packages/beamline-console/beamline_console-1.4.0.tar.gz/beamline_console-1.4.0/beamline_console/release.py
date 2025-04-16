__all__ = ("Release",)

__docformat__ = "restructuredtext"


class Release:
    """Summarize release information as class attributes.
    """

    name = 'beamline_console'
    version_info = (1, 4, 0)
    version = '.'.join(map(str, version_info[:3]))
    release = ''.join(map(str, version_info[3:]))
    separator = '.' if 'dev' in release or 'post' in release else ''
    version_long = version + separator + release

    version_number = int(version.replace('.', ''))
    long_description = description = 'GUI for experimental control'

    license = 'GPL3'
    authors = (('Yury Matveev', 'yury.matveev@desy.de'),)
    author_lines = "\n".join([f"{name}: {email}" for name, email in authors])
    url = 'https://gitlab.desy.de/yury.matveev/beamline_console'
    download_url = 'https://gitlab.desy.de/yury.matveev/beamline_console.git'
    platform = ['Linux', 'Windows']
