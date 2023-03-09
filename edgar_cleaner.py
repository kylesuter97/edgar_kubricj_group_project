import os
from bs4 import BeautifulSoup

def clean_html_text(html_text):

    #Takes html from file specified in "write_clean_html_text_files" function and reads it.
    with open(html_text, 'r', encoding='utf8') as f:
        html = f.read()

    #BeautifulSoup goes through HTML text and removes tags.
    soup = BeautifulSoup(html, 'html.parser')
    clean = soup.get_text()
    return clean

def write_clean_html_text_files(input_folder, dest_folder):

    #Specify start directory to read HTML files from.
    directory = os.fsencode(input_folder)

    for file in os.listdir(directory):

        #Change working directory to given location of HTML files.
        os.chdir(directory)
        filename = os.fsdecode(file)

        #Sends each file to "clean_html_text" function.
        clean = clean_html_text(file)

        #Specify end directory to write clean files to.
        os.chdir(dest_folder)

        #Create new file using the ticker and date from original HTML file, if it doesn't exist, and writes the clean text into it.
        new_file = open(filename.replace('.html', '.txt'), 'w', encoding='utf8')
        new_file.write(clean)
        new_file.close()

        print(f'{filename} has been created.')

        #