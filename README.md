# Facial-Recognition-using-OpenCV
An OpenCV project with HTML, CSS frontend and fastapi for server side scripting that uses MongoDB for storing face data.
## Files included:
- main.py : This file contains the fastapi code that renders the index.html, recog.html and learn.html file, and the code to recognise faces from images</li>
- templates : This directory contains index.html, recog.html and learn.html. Jinja is used to use this templates directory.
  - index.html : Home HTML page
  - recog.html : The page that is rendered after a face is recognised to show result
  - learn.html  : The page that is rendered after a successful learning procedure
- static : This directory contains the css styling file and icons for the webpage

## Working:
- The project uses the face recognition and mediapipe module to recognise a face and extract face landmarks from it after processing. A compare function is used to recognise a similar face.
- When a face is learned these landmarks are extracted and is fed into a MongoDB database.
- During recognition the landmarks of the given image is compared to each of the landmarks already present in the MongoDB database. The result is hence fetched and displayed.
## Run the project
- Use the following command to execute the application:
```
uvicorn main:app
```
The packages that should be installed are included in requirements.txt. To install all that packages in one stretch use the following command in a shell where requirements.txt exist :
```
pip install -r requirements.txt
```
After using uvicorn to execute use the localhost link provided to initialte the application.
You can add a '/docs' to the end of the localhost link to see the documentation.
