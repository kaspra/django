# React-Django-Razorpay-integration

- Install following dependencies
``` 
pip install django djangorestframework python-dotenv razorpay django-cors-headers
```
- create .env file, where manange.py file is located
```
RAZORPAY_KEY_ID= here add razorpay id key
RAZORPAY_KEY_SECRET= here add razorpay secret key
```
- run project
```
python manage.py runserver
```
- Setup React Project
- install npm packages, make sure your location should be where package.json file is located.
```
npm install .
```
- create .env file, where package.json file is located
```
REACT_APP_RAZORPAY_KEY_ID= here add razorpay id key
```
- run project
```
npm start
```
