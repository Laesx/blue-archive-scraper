import os

import requests
import UnityPy

# conf
option = {
    # will skip resources that already downloaded.
    "skipExistingDownloadedResource": True,
    # will skip assets that already exists.
    "skipExistingAssets": True
}

ba_api = "https://yostar-serverinfo.bluearchiveyostar.com/r64_4hwwigy8ojry9k25hduz.json"

ba_api2 = "https://prod-noticeindex.bluearchiveyostar.com/prod/index.json"


def getVersion():
    '''
    Return latest version of Blue Archive Japan
    Unused for now
    '''
    data = requests.get(ba_api2).json()
    return data["LatestClientVersion"]


def getBaseResourceURL():
    '''
    Return resource url for Blue Archive
    '''
    data = requests.get(ba_api).json()
    print(data)
    return data["ConnectionGroups"][0]['OverrideConnectionGroups'][-1]['AddressablesCatalogUrlRoot']
    # https://prod-clientpatch.bluearchiveyostar.com/r47_1_22_46zlzvd7mur326newgu8_2 + /Android/bundleDownloadInfo.json


def getAssetList():
    '''
    Return list of Blue Archive assets url path.
    Media Types:
    1 - Audio
    2 - Video
    3 - Photo
    '''
    data = []
    base_url = getBaseResourceURL()
    res_url = base_url + '/MediaResources/MediaCatalog.json'
    res = requests.get(res_url).json()
    for asset in res["Table"].items():
        if 2 != asset[1]["MediaType"]:
            # append url and path
            data.append(base_url + '/MediaResources/' + asset[1]["path"])
    return data


def downloadFile(url, fname):
    src = requests.get(url).content
    with open(fname, 'wb') as f:
        f.write(src)


if __name__ == "__main__":
    # make folders
    if not (os.path.isdir("./assets")):
        os.makedirs("./assets")

    # There are several ResourceURL to a version
    ver = getBaseResourceURL() + "/MediaResources/MediaCatalog.json"
    print(ver)
    """
        if (os.path.isfile("./version.txt")):
        with open("./version.txt", "r") as f:
            ver_temp = f.read()
        if str(ver) == str(ver_temp):
            print(f"[{ver}] No new update. Stopping.")
            exit(1)
        else:
            print(f"Update {ver_temp} to {ver}")
            with open("./version.txt", "w") as f:
                f.write(ver)
    else:
        with open("./version.txt", "w") as f:
            f.write(ver)

    """

    # get asset list
    asset_list = getAssetList()

    # download list of model list
    for index, mediaFile in enumerate(asset_list, start=1):
        print("="*30)
        print(f"{index}/{len(asset_list)}")
        fname = mediaFile.split("/")[-1]
        destDownload = f"./assets/{mediaFile.split('MediaResources/')[1]}"

        print(fname)

        # skip if already exists
        if option["skipExistingDownloadedResource"] and os.path.isfile(destDownload):
            print("Already downloaded. Skipping.")
            continue


        if not (os.path.isdir(destDownload.rsplit("/", 1)[0])):
            os.makedirs(destDownload.rsplit("/", 1)[0])

        downloadFile(mediaFile, destDownload)

