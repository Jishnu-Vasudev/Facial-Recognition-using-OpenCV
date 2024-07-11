import io
import cv2
import face_recognition as fr
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import mongoengine as monge
import base64

app = FastAPI()
monge.connect(host="mongodb://localhost:27017/Face_Information", db="Face_Information")

# Mount static files like CSS and icons
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2Templates instance with templates directory
templates = Jinja2Templates(directory="templates")

class Person(monge.Document):
    name = monge.StringField()
    encode = monge.ListField()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/recognise")
async def recoimage(request: Request, file: UploadFile = File(...)):
    content = await file.read()
    img = fr.load_image_file(io.BytesIO(content))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_locations = fr.face_locations(img)
    if not face_locations:
        raise HTTPException(status_code=404, detail="No face detected in the image.")

    encode_img = fr.face_encodings(img)[0]

    recognized_name = None
    for person in Person.objects():
        if fr.compare_faces([person.encode], encode_img):
            recognized_name = person.name
            # Draw rectangle around the face
            top, right, bottom, left = face_locations[0]  # Assuming only one face is recognized
            cv2.rectangle(img, (left, top), (right, bottom), (255, 0, 255), 2)
            # Add text with recognized name
            cv2.putText(img, recognized_name, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            break

    if recognized_name is None:
        recognized_name = "Unknown"

    # Convert image to base64 format for displaying in HTML
    retval, buffer = cv2.imencode('.jpg', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return templates.TemplateResponse("recog.html", {"request": request, "recognized_name": recognized_name, "image": img_base64})

@app.post("/learn")
async def learnimg(request: Request, file: UploadFile = File(...)):
    content = await file.read()
    img = fr.load_image_file(io.BytesIO(content))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_locations = fr.face_locations(img)
    if not face_locations:
        raise HTTPException(status_code=404, detail="No face detected in the image.")

    encode_img = fr.face_encodings(img)[0]

    name = file.filename.split(".")[0]
    person = Person(name=name, encode=encode_img.tolist())
    person.save()

    return templates.TemplateResponse("learn.html", {"request": request, "name": name, "image": base64.b64encode(content).decode('utf-8')})
