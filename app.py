from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))


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

@app.route("/recommend")
def recommend_ui():
    return render_template('recommend.html')

@app.route("/recommend_books" , methods=['post'])
def recommend():
    user_input = request.form.get('user_data')
    index = np.where(pt.index == user_input)[0][0]   # get the row index
    similar_items = sorted(list(enumerate(similarity[index])), key = lambda x: x[1], reverse=True)[1:6]
    
    data = []
    for i in similar_items:
        items = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(items)
    print(data)
    return render_template('recommend.html' , data = data)

if __name__ == "__main__":
    app.run(debug =True, port=5001)