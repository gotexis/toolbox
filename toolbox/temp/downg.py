from google_drive_downloader import GoogleDriveDownloader as gdd

files = {

    'supert': '1-FYLKEG4-1ExU_bxQO3GcMWAhxOrLQqj',
}


def down(name):
    file_id = files[name]
    gdd.download_file_from_google_drive(
        file_id=file_id,
        dest_path=f'F:/game.console/switch/roms.not_installed/{name}.nsp',
        showsize=True
    )


def download_all():
    for file in files.keys():
        down(file)

# download_all()


gdd.download_file_from_google_drive(
    file_id='1-FYLKEG4-1ExU_bxQO3GcMWAhxOrLQqj',
    dest_path=f'F:/game.console/switch/roms.not_installed/supert.nsp',
    showsize=True
)

from django.db.models import ForeignKey