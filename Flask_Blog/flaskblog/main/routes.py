from flask import render_template, request, Blueprint
from flaskblog.models import Post, Expert
import requests
from flaskblog.posts.forms import Market
from flask import Response
from flask import current_app
main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    imageArray = [{'image':'default.jpg', 'name':'A'},{'image':'Satish1.jpg','name':'B'},{'image':'Satish.jpg','name':'C'}]

    # posts = Post.query.all()
    page = request.args.get('page', 1, type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)

    experts = Expert.query.all()
    # print("experts = ",experts)
    # experts = experts[0]
    # print(experts.username, experts.firstname, experts.firstname, experts.email, experts.description)

    market = Market()
    # websiteExperience = CommentYourExperience()

    # str = 'https://www.quandl.com/api/v3/datasets/NSE/DVL?start_date=2019-01-04&end_date=2019-01-04&api_key=xB2axeWukJ1qpQiD-Rg5'
    # r = requests.get(str)
    # json_object = r.json()
    # print("JSON1 = ",json_object)
    # return redirect(url_for('/'))
    resp = Response("")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    json_object = {}
    if market.validate_on_submit():
        print("aaaaa",market)
        # print("Satish =  ",market)
        # print("Show Data1 = ",market.stockname.data)
        name = market.stockname.data
        r = requests.get('https://www.quandl.com/api/v3/datasets/NSE/'+name+'?column_index=1&api_key=xB2axeWukJ1qpQiD-Rg5')
        json_object = r.json()
        # print("JSONNN1 = ",json_object)
        # return redirect(url_for('home'))

    # return render_template('home.html', data=posts)
    # print("JSON OBJECT = ",json_object)
    newsData = getnews()
    
    # if websiteExperience.validate_on_submit() and websiteExperience.submitFeedback.data:
        # name = websiteExperience.experience.data
        # print("Experience = "+name)

    # print("newsData = ",newsData)
    return render_template('home.html', posts=posts, market=market, data=json_object, experts=experts, newsData=newsData)
    # return "Hello Satish!"




#     market = Market()

#     # str = 'https://www.quandl.com/api/v3/datasets/NSE/DVL?start_date=2019-01-04&end_date=2019-01-04&api_key=xB2axeWukJ1qpQiD-Rg5'
#     # r = requests.get(str)
#     # json_object = r.json()
#     # print("JSON1 = ",json_object)
#     # return redirect(url_for('/'))
#     json_object = {}
#     if market.validate_on_submit():
#         print("aaaaa",market)
#         print("Satish =  ",market)
#         print("Show Data1 = ",market.stockname.data)
#         r = requests.get('https://www.quandl.com/api/v3/datasets/NSE/'+market.stockname.data+'?start_date=2019-01-04&end_date=2019-01-04&api_key=xB2axeWukJ1qpQiD-Rg5')
#         json_object = r.json()
#         print("JSONNN = ",json_object)
#         return redirect(url_for('home'))
#     # return render_template('home.html', data=posts)
#     return render_template('home.html', posts=posts, market=market)
#     # return "Hello Satish!"

# # def show(name):

@main.route("/about")
def about():
    return render_template('about.html', title = 'About')


def getnews():
    # print("News Api Key",current_app.config['NEWS_API_KEY'])
    r = requests.get('https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey='+current_app.config['NEWS_API_KEY'])
    return r.json()