import uvicorn
import hashlib
import final.utils.mainutils as utils
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from fastapi import FastAPI, File, UploadFile, Query
from typing import List

app = FastAPI()

configfile = utils.import_config_file("./config.json")

# create a new handler and connect the logger to logs.txt file
logger = utils.create_logger(configfile["LoggerName"], configfile["LogFormatter"], configfile["LogFile"])


def encrypt(first_half, second_half):
    full_file = first_half + second_half

    # create hash of the two file names combined
    file_names_hash = hashlib.sha512()
    file_names_hash.update(full_file)
    hash_file = file_names_hash.hexdigest()

    # encrypt the resulting hash with sha512 and a random iv
    iv = get_random_bytes(16)
    cipher = AES.new('This is a key123'.encode("utf8"), AES.MODE_CFB, iv)
    ciphertext = cipher.encrypt(hash_file.encode("utf8"))
    end_file = iv + ciphertext

    # add the iv and the encrypted hash to the end of the file
    full_file_hash = full_file + end_file
    return full_file_hash, end_file


def read_uploaded_file(uploaded_file):
    try:
        logger.info(f'success upload - uploaded file to FastApi server: {uploaded_file.filename}')
        split_name = uploaded_file.filename.split("_")
        index = 0 if ("a" == split_name[1].split(".")[0]) else 1
        content = uploaded_file.file.read()
        return index, content, split_name[0]
    except Exception as e:
        logger.error(f'error upload - There was an error uploading: {uploaded_file.filename} - {str(e)}')
        return {"message": "There was an error uploading the file(s)"}
    finally:
        uploaded_file.file.close()


@app.post("/")
def upload(files: List[UploadFile] = File(...)):

    if not len(files) == 2:
        return 400

    name = ''
    content = [None, None]
    for f in files:
        index, file_content, name = read_uploaded_file(f)
        content[index] = file_content

    if content[0] is None or content[1] is None:
        return 400

    # create variable that of both files plus the hash
    full_file_hash = encrypt(content[0], content[1])[0]
    # writes the content of the file with the signature to a local file
    try:
        with open(f'/home/roeihafifot/uploaded_photos/{name}.jpg', 'wb') as f:
            f.write(full_file_hash)
        logger.info(f'success merge - merged files and created file: {name}')
    except Exception as e:
        logger.error(f'error merge - There was an error merging and creating file: {name} - {e}')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
