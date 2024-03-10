from flask import Flask,render_template
import pickle

popular_df = pickle.load(open('popular.pkl','rb'))
r_rating = [round(rating,2) for rating in popular_df['avg_rating'].values]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                            book_name = list(popular_df['Book-Title'].values),
                            author = list(popular_df['Book-Author'].values),
                            image = list(popular_df['Image-URL-M'].values),
                            votes = list(popular_df['num_rating'].values),
                            rating = r_rating
                        )

if __name__ == "__main__":
    app.run(debug =True, port=5001)