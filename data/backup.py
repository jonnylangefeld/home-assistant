from mega import Mega # pip3 install mega.py
import json, subprocess, glob, os
from datetime import datetime

backups_dir = "/config/backups/"
history_limit = 3
with open('/config/backup-secrets.json', 'r') as f:
    secrets = json.load(f)

mega = Mega()
m = mega.login("jonnylangefeld@gmail.com", secrets['mega_password'])

def latest_backup():
    all_backups = glob.glob(backups_dir + "*.tar")
    all_backups = sorted(all_backups, key=os.path.getmtime)
    if not all_backups:
        print("there is no home-assistant backup")
        exit(1)
    latest_backup = all_backups[-1]
    name = "{}.tar".format(datetime.fromtimestamp(os.path.getmtime(latest_backup)).strftime("%Y-%m-%d-%H-%M-%S"))
    dst = os.path.join(os.path.dirname(latest_backup), name)
    os.rename(latest_backup, dst)
    return dst

def encrypt(backup):
    print("encrypting...")
    name = backup+".gpg"
    gpg = subprocess.run(
        ["gpg", "-o", name, "-c", "--batch", "--passphrase", secrets['encryption_key'], backup]
    )

    print(gpg)
    if gpg.returncode:
        exit(gpg.returncode)
    return name

def upload(backup):
    backup_folder = m.find("home-assistant-backups")
    print(backup)
    file_name = os.path.basename(backup)
    file = m.find(file_name)
    if file:
        print("deleting exsiting file {}...".format(file_name))
        m.delete(file[0])
    print("uploading...")
    file = m.upload(backup, backup_folder[0])
    print("backup uploaded to {}".format(m.get_upload_link(file)))

def prune(backup):
    encrypted_backups = glob.glob(backups_dir + "*.tar.gpg")
    for file in encrypted_backups:
        os.remove(file)

    backups = glob.glob(backups_dir + "*.tar")
    backups = sorted(backups, key=os.path.getmtime)
    if len(backups) > history_limit:
        for f in backups[:len(backups)-history_limit]:
            file_name = os.path.basename(f)+".gpg"
            file = m.find(file_name)
            if file:
                print("deleting old upstream file {}...".format(file_name))
                m.delete(file[0])
            os.remove(f)


if __name__ == "__main__":
    latest_backup = latest_backup()
    encrypted = encrypt(latest_backup)
    upload(encrypted)
    prune(latest_backup)
