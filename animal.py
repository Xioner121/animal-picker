# importing Flask and other modules
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from deepface import DeepFace
from icrawler.builtin import GoogleImageCrawler
import shutil
import wikipedia
import random
import time
from pathlib import Path
# Flask constructor
app = Flask(__name__)  

#Confugres upload folder
upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder

#Routes home for GET, POST methods
@app.route('/', methods =["GET", "POST"])
def submit_data():
    if request.method == "POST":
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename) #Full file path
        
        favAnimal = request.form.get("aName") #name of favorite animal
        time.sleep(2)
        
        #Start of AI/ML code
        # emotion detection
        face_analysis = DeepFace.analyze(img_path = img, enforce_detection=False)
        dominantEmotion = face_analysis[0]["dominant_emotion"]
        face_analysis[0]["emotion"].pop(dominantEmotion)
        secondEmotion = max(face_analysis[0]["emotion"])

        # sets favorite animal and search query
        print(dominantEmotion + " and " + secondEmotion)
        favorite_animal = favAnimal
        query = favorite_animal + " " + dominantEmotion + " and " + secondEmotion + " animal"

        # finds images using google image crawler
        path = Path("static/000001.jpg")
        if path.is_file():
            os.remove("static/000001.jpg")
            
        filter = dict(type="photo")
        image_crawler = GoogleImageCrawler(storage = {"root_dir": r'static'})
        image_crawler.crawl(keyword = query, filters = filter, max_num = 1)
 
        #os.rename("static/" + file, "static/animalImage.jpg")
        # keeps one random image
        #randInt = random.randint(1,3)
        #for file in os.listdir("static"):
            #if file != "00000" + str(randInt) + ".jpg":
                #os.remove("static/" + file)
            #else:
                #os.rename("static/" + file, "static/animalImage.jpg")
        
        time.sleep(2) # Sleep for 3 seconds
        #PEOPLE_FOLDER = os.path.join('images') #end of AI/ML code

        #app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
        #img2 = os.path.join(app.config['UPLOAD_FOLDER'], 'animalImage.jpg')
        #imgPath = url_for('images', filename='animalImage.jpg')
        
        def searchWikipedia():
            search = wikipedia.search(favorite_animal, results = 1)
            if not search:
                search = wikipedia.suggest(favorite_animal)
                if search == None:
                    return ["You may have spelled your favorite animal wrong.", "No link found."]
                try:
                    result = wikipedia.summary(search, auto_suggest=False)
                    link = wikipedia.page(search, auto_suggest=False).url
                except:
                    return ["Wikipedia not found. Try to be specific.", "No link found."]
            else:
                try:
                    result = wikipedia.summary(search[0], auto_suggest=False)
                    link = wikipedia.page(search[0], auto_suggest=False).url
                except:
                    return ["Wikipedia not found. Try to be specific.", "No link found."]
            return [result, link]
        wikiDescription = searchWikipedia()[0] + "\n \n" + "Learn More: "+ searchWikipedia()[1]
        return render_template('index.html', foundImage=True, description = wikiDescription)
    return render_template("index.html")
 
#Default Home Page
@app.route('/')
def home(): 
    return render_template("index.html")

if __name__=='__main__':
   app.run()