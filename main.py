import gensim
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pandas as pd
import multiprocessing
from sklearn.metrics import accuracy_score



def get_vectors(model, tagged_docs):
    feature_matrix = []
    label_list = []
    for tagged_docs in tagged_docs:
        feature_matrix.append(model.infer_vector(tagged_docs.words))
        label_list.append(tagged_docs.tags[0])

    return feature_matrix, label_list


def tag_document(doc):
    return doc.apply(
        lambda row: TaggedDocument(words=row[0], tags=[row[1]]), axis=1)


df = pd.read_csv('./youtube_comments.csv')

df['comment'] = df['comment'].apply(gensim.utils.simple_preprocess)

train, test = train_test_split(df)
train_tagged = tag_document(train)
test_tagged = tag_document(test)

# This isn't in the blog, but gensim can also save your Doc2Vec model to local memory so you won't have to train again if you use it a second+ time.
try:
    model = Doc2Vec.load('youtube_model.doc2vec')
except FileNotFoundError:
    model = Doc2Vec(documents=train_tagged, workers=multiprocessing.cpu_count())
    model.save('youtube_model.doc2vec')

x_train, y_train = get_vectors(model, train_tagged)
x_test, y_test = get_vectors(model, test_tagged)

classifier = LogisticRegression()
classifier.fit(x_train, y_train)
y_pred = classifier.predict(x_test)

print('Accuracy:', accuracy_score(y_test, y_pred))
