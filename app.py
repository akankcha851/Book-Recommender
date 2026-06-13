from flask import Flask, render_template, request
import pickle
import numpy as np

popular = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
book = pickle.load(open('book.pkl', 'rb'))
same_score = pickle.load(open('same_score.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        'index.html',
        book_name=list(popular['Book-Title'].values),
        author=list(popular['Book-Author'].values),
        image=list(popular['Image-URL-M'].values),
        votes=list(popular['ratings'].values),
        rating=list(popular['a_rating'].values)
    )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():

    user_input = request.form.get('user_input')

    data = []

    try:
        index = np.where(pt.index == user_input)[0][0]

        similar_items = sorted(
            list(enumerate(same_score[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:9]

        for i in similar_items:

            temp_df = book[book['Book-Title'] == pt.index[i[0]]]

            item = []

            item.append(
                temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0]
            )

            item.append(
                temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0]
            )

            item.append(
                temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]
            )

            data.append(item)

    except:
        pass

    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)