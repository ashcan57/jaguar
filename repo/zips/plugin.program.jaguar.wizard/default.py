import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
import urllib.request
import os
import zipfile

BUILD_URL = "https://www.dropbox.com/scl/fi/glc4wagx7mmdvso88jmiu/encore.zip?rlkey=836o6k19xlppx2ab9ek0zvcbt&st=u7bsm4iz&dl=1"
BUILD_NAME = "Encore"
USERDATA = xbmcvfs.translatePath("special://home/")
TEMP_ZIP = xbmcvfs.translatePath("special://temp/encore.zip")

def install_build():
    dialog = xbmcgui.Dialog()
    confirm = dialog.yesno("Jaguar Wizard", f"Install the {BUILD_NAME} Build?\n\nThis will overwrite your current Kodi setup.", nolabel="Cancel", yeslabel="Install")
    if not confirm:
        return
    progress = xbmcgui.DialogProgress()
    progress.create("Jaguar Wizard", "Starting download...")
    try:
        def report(block_num, block_size, total_size):
            if progress.iscanceled():
                raise Exception("Cancelled")
            if total_size > 0:
                downloaded = block_num * block_size
                percent = min(int(downloaded * 100 / total_size), 99)
                mb_done = downloaded / (1024 * 1024)
                mb_total = total_size / (1024 * 1024)
                progress.update(percent, f"Downloading {BUILD_NAME} Build...\n{mb_done:.1f} MB of {mb_total:.1f} MB  ({percent}%)")
        urllib.request.urlretrieve(BUILD_URL, TEMP_ZIP, reporthook=report)
        if progress.iscanceled():
            progress.close()
            return
        progress.update(0, "Preparing to install...")
        xbmc.sleep(300)
        with zipfile.ZipFile(TEMP_ZIP, 'r') as z:
            entries = z.infolist()
            total = len(entries)
            for i, entry in enumerate(entries):
                if progress.iscanceled():
                    raise Exception("Cancelled")
                percent = int((i + 1) * 100 / total)
                name = entry.filename if len(entry.filename) <= 50 else "..." + entry.filename[-47:]
                progress.update(percent, f"Installing {BUILD_NAME} Build...\nFile {i + 1} of {total}  ({percent}%)\n{name}")
                z.extract(entry, USERDATA)
        if os.path.exists(TEMP_ZIP):
            os.remove(TEMP_ZIP)
        progress.update(100, "Installation complete!")
        xbmc.sleep(800)
        progress.close()
        restart = dialog.yesno("Jaguar Wizard", f"{BUILD_NAME} Build installed successfully!\n\nRestart Kodi now?", nolabel="Later", yeslabel="Restart Now")
        if restart:
            xbmc.executebuiltin("RestartApp")
    except Exception as e:
        progress.close()
        if os.path.exists(TEMP_ZIP):
            os.remove(TEMP_ZIP)
        if "Cancelled" not in str(e):
            dialog.ok("Jaguar Wizard", f"Installation failed:\n{str(e)}")

if __name__ == "__main__":
    install_build()
