from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fpdf import FPDF

def scraper(chromedriver_path):

    """Get the health education knowledge from WebMed Website."""

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument('headless')

    driver = webdriver.Chrome(options = chrome_options)

    urls = [
        'https://www.webmd.com/fitness-exercise/news/20240528/step-up-to-better-health-the-case-for-taking-the-stairs',
        'https://www.webmd.com/diet/features/the-benefits-of-vitamin-c',
        'https://www.webmd.com/diet/what-are-processed-foods',
    ]

    serialno = 0

    for url in urls:
        
        driver.get(url)
        content_xml = driver.find_element("xpath", '//*[@id="ContentPane30"]/article/div/div[3]')
        content_html = content_xml.get_attribute('innerHTML')
        #driver.quit()

        soup = BeautifulSoup(content_html, 'html.parser')
        content_text = soup.get_text(separator = '\n', strip = True)
        
        result_pdf = FPDF()
        result_pdf.add_page()
        result_pdf.set_auto_page_break(auto = True, margin = 15)
        result_pdf.set_font("Arial", size = 12)
    
        for line in content_text.split('\n'):
            result_pdf.multi_cell(w = 0, h = 10, txt = line.encode('latin1', 'replace').decode('latin1')) 

        file_path = "..\data\med_knowledge"
        filext = ".pdf" 
        filename = "med_knowledge" + str(serialno) + filext
        filepath_n_name = file_path +  str(serialno) + filext
        result_pdf.output(filepath_n_name)
        print(f"Content Saved to {filename}")

        serialno += 1

    return 

if __name__ == '__main__':
    chromedriver_path = 'D:\\chromedriver.exe'  
    scraper(chromedriver_path)