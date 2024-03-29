from flair.data import Corpus, Sentence
from flair.datasets import CSVClassificationCorpus
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentRNNEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer

data_folder = './data'
# define columns
column_name_map = {2: 'text', 1:'label_topic'}
# 1. get the corpus
corpus: Corpus = CSVClassificationCorpus(data_folder,
                                        column_name_map,
                                        skip_header=True,
                                        delimiter='\t')

# 2. create the label dictionary
label_dict = corpus.make_label_dictionary()

# 3. make a list of word embeddings
word_embeddings = [WordEmbeddings('glove'),

                   # comment in flair embeddings for state-of-the-art results
                   # FlairEmbeddings('news-forward'),
                   # FlairEmbeddings('news-backward'),
                   ]

# 4. initialize document embedding by passing list of word embeddings
# Can choose between many RNN types (GRU by default, to change use rnn_type parameter)
document_embeddings: DocumentRNNEmbeddings = DocumentRNNEmbeddings(word_embeddings,
                                                                    hidden_size=512,
                                                                    reproject_words=True,
                                                                    reproject_words_dimension=256,
                                                                    )

# 5. create the text classifier
classifier = TextClassifier(document_embeddings, label_dictionary=label_dict)

# 6. initialize the text classifier trainer
trainer = ModelTrainer(classifier, corpus)

# 7. start the training
trainer.train('resources/taggers/ag_news',
              learning_rate=0.1,
              mini_batch_size=5,
              anneal_factor=0.5,
              patience=5,
              max_epochs=10)

# 8. plot training curves (optional)
# from flair.visual.training_curves import Plotter
# plotter = Plotter()
# plotter.plot_training_curves('resources/taggers/ag_news/loss.tsv')
# plotter.plot_weights('resources/taggers/ag_news/weights.txt')


classifier = TextClassifier.load('resources/taggers/ag_news/final-model.pt')

# create example sentence
sentence = Sentence('Add it to playlist')

# predict tags and print
classifier.predict(sentence)

print(sentence.labels)