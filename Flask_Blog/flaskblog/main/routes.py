from flask import render_template, request, Blueprint
from flaskblog.models import Post
import requests
from flaskblog.posts.forms import Market
from flask import Response
main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    print("sdkfhgskdfjhs kjdfkjhfsdkjhksjdfh kjf")
    # posts = Post.query.all()
    page = request.args.get('page', 1, type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)

    market = Market()

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
        print("Satish =  ",market)
        print("Show Data1 = ",market.stockname.data)
        name = market.stockname.data
        r = requests.get('https://www.quandl.com/api/v3/datasets/NSE/'+name+'?column_index=1&api_key=xB2axeWukJ1qpQiD-Rg5')
        json_object = r.json()
        print("JSONNN1 = ",json_object)
        # return redirect(url_for('home'))

    # return render_template('home.html', data=posts)
    return render_template('home.html', posts=posts, market=market, data=json_object)
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
