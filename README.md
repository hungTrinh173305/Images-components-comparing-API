## Project Overview
- An API that compares images' components using background substraction.
- Run by ```python main.py```, then copy the local url (eg. ```http://127.0.0.1:5000```) into your browser.
- Input two images, output an image with bounded rectangle on differences bewtween the two images.
- Recommend to use images from ```static/toCompareImages``` for the API. 

## Project Files
1. ```static/results``` - Contains all result images that the API has compared
2. ```static/toCompareImages``` - Contains sample images to compare.
3. ```static/uploads``` - Contains all uploaded images to the API.
4. ```templates/``` - Contains html templates used for the project.
5. ```main.py``` - The main code file to run

## Installation & Dependences
Requires Python 3 with flask and opencv.
