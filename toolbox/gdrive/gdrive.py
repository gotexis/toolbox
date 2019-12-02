from google_drive_downloader import GoogleDriveDownloader as gdd

from projects import dragon_quest

for line in dragon_quest:
    gdd.download_file_from_google_drive(file_id=line[0],
                                        dest_path=f'./{line[1]}',
                                        showsize=True)

