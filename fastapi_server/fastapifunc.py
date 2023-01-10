import uvicorn
import ast
import hashlib
import logging
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from fastapi import FastAPI, File, UploadFile, Query
from typing import List
from fastapi.responses import FileResponse

app = FastAPI()
# open config file
with open("/home/roeihafifot/config.json") as jsonfile:
    configfile = json.load(jsonfile)

# create a new handler and connect the logger to logs.txt
logger = logging.getLogger(configfile["LoggerName"])
logger.setLevel(logging.DEBUG)
createhandler = logging.StreamHandler()
createhandler.setLevel(logging.DEBUG)
formatter = logging.Formatter(configfile["LogFormatter"])
createhandler.setFormatter(formatter)
logger.addHandler(createhandler)
handler = logging.FileHandler(configfile["LogFile"])
logger.addHandler(handler)


def encrypt(first_half, second_half):
    full_file = first_half + second_half
    # enctypt the data of the file with sha512 and a random iv
    hash = hashlib.sha512()
    hash.update(full_file)
    hash_file = hash.hexdigest()
    iv = get_random_bytes(16)
    cipher = AES.new('This is a key123'.encode("utf8"), AES.MODE_CFB, iv)
    ciphertext = cipher.encrypt(hash_file.encode("utf8"))
    end_file = iv + ciphertext
    # adds the iv and the encrypted hash to the ens of the file
    full_file_hash = full_file + end_file
    return full_file_hash


@app.post("/")
def upload(files: List[UploadFile] = File(...)):
    # create's variable for each half of the file that is sent
    for upload_file in files:
        logger.info(f'success upload - uploaded file to FastApi server: {upload_file.filename}')
        split_name = (upload_file.filename).split("_")
        try:
            if "a" == split_name[1].split(".")[0]:
                contents_first_half = upload_file.file.read()
            else:
                contents_second_half = upload_file.file.read()
        except Exception:
            logger.info(f'error upload - There was an error uploading: {upload_file.filename}')
            return {"message": "There was an error uploading the file(s)"}
        finally:
            upload_file.file.close()
    # create variable that containes the full leangth of the file
    full_file_hash = encrypt(contents_first_half, contents_second_half)
    # writes the content of the file with the signeture to a local file
    try:
        with open(f'/home/roeihafifot/uploaded_photos/{split_name[0]}.jpg', 'wb') as f:
            f.write(full_file_hash)
        logger.info(f'success merge - merged files and created file: {split_name[0]}')
    except Exception:
        logger.info(f'error merge - There was an error merging and creating file: {split_name[0]}')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
