## HW 1
## SI 364 F18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".

##StackOverflow


## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask, request
app = Flask(__name__)
app.debug = True

@app.route('/class')
def hello_to_you():
    return 'Welcome to SI 364!'



## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

# {
#  "resultCount":0,
#  "results": []
# }


## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

import requests
import json

@app.route('/movie/<movie_name>')
def get_movie_data(movie_name):

    #movie_data = requests.get('http://itunes.apple.com/search?', params = {'term': movie_name, 'entity': 'movie'})
    movie_data = requests.get('https://itunes.apple.com/search?term=' + movie_name)
    return movie_data.text

## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.

@app.route('/question/')
def user_input():
    number = """<!DOCTYPE html>
<html>
<body>
<form action="http://localhost:5000/double_your_num" method="post">
  Enter Your Favorite Number!<br>
  <br></br>
  <input type="text" name="number">
  <br>
  <br></br>
  <input type="submit" value="Submit">
</form>
</body>
</html>"""
    return number

@app.route('/double_your_num',methods=['POST', 'GET'])
def double_number():
  if request.method == 'POST':
    user_num = str(request.form['number'])
    doubled = int(user_num)*2
    return "<p>Double your favorite number is {}</p>".format(str(doubled))



## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.
import re

@app.route('/numbers',methods=["POST","GET"])
## The user will use this tool to find fun facts about different numbers that they may find interesting. This uses the open-source Numbers API, which takes an integer as input and can return fun facts about numbers, dates, or years.
def numbers_call():
  alt = """
  <!DOCTYPE html>
  <html>
  <body>
  <form action="http://localhost:5000/numbers" method='POST'>
    What kind of Number would you like to enter?<br>
    <input type="checkbox" name="integer" value="integter"> Integer<br>
    <input type="checkbox" name="date" value="date"> Date<br>
    <input type="checkbox" name="year" value="year"> Year<br>
    <input type="checkbox" name="other" value="other"> Other<br>
    Enter the number here: <br><input type="text" name="input"<br>
    <input type="submit" value="Submit">
  </form>
</body>
</html>
"""
  if request.method == "POST":


    user_input = str(request.form['input'])


    number_info = requests.get('http://numbersapi.com/' + user_input + "?json")
    number_json = json.loads(number_info.text)
    number_text = json.dumps(number_json)

    #number_indexed = findall('"([^"]*)"', number_text)
    number_indexed = str(re.findall(r'"(.*?)"', number_text))
    #number_indexed = number_text[3]
    textlist = number_text.split(',')
    index = textlist[0] 
    number_indexed_2 = str(re.findall(r'"(.*?)"', index))
    textlist_2 = number_indexed_2.split(',')
    index2 = textlist_2[1]
    index2 = index2.replace("\"", "")
    index2 = index2.replace("\'", "")
    index2 = index2.replace("]", "")



    return "Here is an interesting fact about {}:       ".format(user_input) + index2
    #return "Here:"
    #return type(number_info)
    #print(number_json)
    #return number_json
    #return number_json
  else:
  	return alt



if __name__ == '__main__':
    app.run()