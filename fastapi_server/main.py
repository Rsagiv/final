import uvicorn
from fastapi import FastAPI, File, UploadFile, Query
from typing import List
from fastapi.responses import FileResponse

app = FastAPI()

#@app.get("/")
#def read_root():
#  return {"Roei final project!!!"}

  
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
  with open(f'/home/roeihafifot/uploaded_photos/{split_name[0]}.jpg', 'wb') as f:
    f.write(full_file)


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8080)
