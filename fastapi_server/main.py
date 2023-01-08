import uvicorn
import ast
import hashlib
import logging
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from fastapi import FastAPI, File, UploadFile, Query
from typing import List
from fastapi.responses import FileResponse

app = FastAPI()

#create a new handler and connect the logger to logs.txt
logger = logging.getLogger('elastic')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
handler = logging.FileHandler('/home/roeihafifot/logs.txt')
logger.addHandler(handler)

#def encrypt(file_content):
#    iv = get_random_bytes(16)
#    cipher = AES.new('This is a key123'.encode("utf8"), AES.MODE_CFB, iv)
#    ciphertext = cipher.encrypt(file_content)
#    return iv + ciphertext


@app.post("/")
def upload(files: List[UploadFile] = File(...)):
  #create's variable for each half of the file that is sent
  for file in files:
    logger.info(f'success upload - uploaded file to FastApi server: {file.filename}')
    split_name=(file.filename).split("_")
    try:
      if "a" in split_name[1]:
        contents_first_half = file.file.read()
      else:
        contents_second_half = file.file.read()
    except Exception:
      return {"message": "There was an error uploading the file(s)"}
      logger.info(f'error upload - There was an error uploading: {file.filename}')
    finally:
      file.file.close()
  #create variable that containes the full leangth of the file
  full_file = contents_first_half + contents_second_half
  #enctypt the data of the file with sha512 and a random iv
  h = hashlib.sha512()
  h.update(full_file)
  hash_file = h.hexdigest()
  iv = get_random_bytes(16)
  cipher = AES.new('This is a key123'.encode("utf8"), AES.MODE_CFB, iv)
  ciphertext = cipher.encrypt(hash_file.encode("utf8"))
  #adds the iv and the encrypted hash to the ens of the file
  end_file = iv + ciphertext
  full_file_hash = full_file + end_file
  #writes the content of the file with the signeture to a local file
  try:
    with open(f'/home/roeihafifot/uploaded_photos/{split_name[0]}.jpg', 'wb') as f:
      f.write(full_file_hash)
    logger.info(f'success merge - merged files and created file: {split_name[0]}')
  except:
    logger.info(f'error merge - There was an error merging and creating file: {split_name[0]}') 

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8080)