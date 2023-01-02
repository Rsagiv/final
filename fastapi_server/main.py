import uvicorn
import ast
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from fastapi import FastAPI, File, UploadFile, Query
from typing import List
from fastapi.responses import FileResponse

app = FastAPI()

#def encrypt(file_content):
#    iv = get_random_bytes(16)
#    cipher = AES.new('This is a key123'.encode("utf8"), AES.MODE_CFB, iv)
#    ciphertext = cipher.encrypt(file_content)
#    return iv + ciphertext


@app.post("/")
def upload(files: List[UploadFile] = File(...)):
  for file in files:
    split_name=(file.filename).split("_")
    try:
      if "a" in split_name[1]:
        contents_first_half = file.file.read()
      else:
        contents_second_half = file.file.read()
    except Exception:
      return {"message": "There was an error uploading the file(s)"}
    finally:
      file.file.close()
  full_file = contents_first_half + contents_second_half
  h = hashlib.sha512()
  h.update(full_file)
  hash_file = h.hexdigest()
  iv = get_random_bytes(16)
  cipher = AES.new('This is a key123'.encode("utf8"), AES.MODE_CFB, iv)
  ciphertext = cipher.encrypt(hash_file.encode("utf8"))
  end_file = iv + ciphertext
  full_file_hash = full_file + end_file
  with open(f'/home/roeihafifot/uploaded_photos/{split_name[0]}.jpg', 'wb') as f:
    f.write(full_file_hash)
  

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8080)
