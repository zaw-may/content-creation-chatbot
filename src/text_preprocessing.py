import fitz
import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

stop_words = set(stopwords.words('english'))

#download once
nltk.download('punkt') #for word_tokenize
nltk.download('wordnet') #for WordNetLemmatizer
nltk.download('averaged_perceptron_tagger') #for part-of-speech tagging

def open_text_data(input_filepath):
    #Reading text document from PDF
    pdf_doc = fitz.open(input_filepath)
    text = ""   
    for page_num in range(pdf_doc.page_count):
        page = pdf_doc.load_page(page_num)
        text += page.get_text()
    df = pd.DataFrame([text], columns = ['text'])

    print("Reading text document successfully")
    return df

def convert_lowercase(df):
    df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    print("Converting to lowercase successfully")
    return df

def remove_others(df):
    #Remove URLs
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    def remove_urls(text):
        return url_pattern.sub(r'', text)
    df['text'] = df['text'].apply(lambda x: remove_urls(x))
    #Remove special characters and non-word characters
    df = df.replace(to_replace = r'[^\w\s]', value = '', regex = True)
    #Remove numbers
    df = df.replace(to_replace = r'\d+', value = '', regex = True)

    print("Removing links, special characters, non-word characters and number successfully")
    return df

def all_tokenization_tasks(df):
    #Tokenization
    df['tokenized_text'] = df['text'].apply(lambda x: word_tokenize(x))

    #Tokenization using BertTokenizer
    #from transformers import BertTokenizer
    #tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    #df['tokenized_text'] = df['text'].apply(lambda x: tokenizer.tokenize(x)) 

    #Removing stop words
    df['tokenized_text'] = df['tokenized_text'].apply(lambda x: [word for word in x if word not in stop_words])

    #Stemming
    ps = PorterStemmer()
    def stem_words(text):
        return [ps.stem(word) for word in text]
    df['stemmed_text'] = df['tokenized_text'].apply(lambda x: stem_words(x))

    #Lemmatization
    lemmatizer = WordNetLemmatizer()
    def lemmatize_words(text):
        def get_wordnet_pos(word):
            word_loc = nltk.pos_tag([word])[0][1][0].upper()
            pos_dict = {"J": wordnet.ADJ,
                        "N": wordnet.NOUN,
                        "V": wordnet.VERB,
                        "R": wordnet.ADV}
            return pos_dict.get(word_loc, wordnet.NOUN)
        result = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in text]
        return result
    df['lemmatized_text'] = df['tokenized_text'].apply(lambda x: lemmatize_words(x))

    print("All tokenization tasks successfully")
    return df

def save_to_csv(df, output_filepath): #to check result data status
    df.to_csv(output_filepath, encoding = 'utf-8-sig', index=False)
    print("Saving to csv successfully")

if __name__ == '__main__':
    input_filepath = '../data/med_knowledge0.pdf'
    filename = 'text_preprocessed' #to accept the input filename from user
    output_filepath = '../data' + '/' + filename + '.csv'

    df = open_text_data(input_filepath)
    converted_df = convert_lowercase(df)
    removed_df = remove_others(converted_df) 
    tokenized_df = all_tokenization_tasks(removed_df)
    save_to_csv(tokenized_df, output_filepath)