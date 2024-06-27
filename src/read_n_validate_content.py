import fitz
import pandas as pd

def read_content(input_filepath):
    pdf_doc = fitz.open(input_filepath)
    text = ""

    for pageno in range(pdf_doc.page_count):
        page = pdf_doc.load_page(pageno)
        text += page.get_text()
    print("Reading content successfully")

    return text

def text_to_df(text):
    df = pd.DataFrame([text], columns = ['text'])
    print("Converting to dataframe successfully")
    return df

def save_to_csv(df, output_filepath): #do not need to save to csv
    df.to_csv(output_filepath, encoding = 'utf-8-sig', index=False)
    print("Saving to csv successfully")

if __name__ == '__main__':
    filename = 'med_knowledge0' #to accept the input filename from user
    input_filepath = '../data' + '/' + filename + '.pdf'
    output_filepath = '../data' + '/' + filename + '.csv'
    
    text = read_content(input_filepath)
    df = text_to_df(text)
    save_to_csv(df, output_filepath)