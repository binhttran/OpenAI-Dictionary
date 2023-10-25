import openai
import json
import webbrowser
import os

def read_key():
    api_key = open("API_KEY2.txt", "r").read().strip('\n')
    openai.api_key = api_key


def dictionary(word_list):
        response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [{"role": "user", "content": f"Pretend this is a dictionary for one word. Create a valid JSON array of object with no white space. The key is {word_list} and the value is the definition of the key."}],    
        temperature = 0.2 
        )
        # completion summary
        api_usage = response['usage']
        print('total token consumed: {0}'.format(api_usage['total_tokens']))
        print("finish reason: " + response['choices'][0].finish_reason)

        data = response.choices[0].message.content
        return data   
       
  
def parse_response(definitions, response):
         data = json.loads(response)
          #loop through a list of dictionary, to extract the vocab and the definition
         for vocabAttempt in data:
            for vocab in vocabAttempt:
                definitions = definitions + "<li><b>" + vocab + "</b>: " + vocabAttempt[vocab] + "</li><br><br>\n\t\t\t"     
         return definitions

def updated_html(file, response):          
        html_content = file.replace('{definitions}', response)
        return html_content

def open_updated(response):        
    with open('updated.html', 'w') as file:
        file.write(response)  
        file.close()
        filename = 'file:///'+os.getcwd()+'/' + 'updated.html'; webbrowser.open_new_tab(filename)  
      
                       
def main():       
    with open("ai definitions.html", 'r') as file:
            html_content = file.read()    
    read_key()
    filtered_response = ""
    file = open("word_list.txt", "r").readlines()
    for line in file:
            word = line.strip('\n')
            response = dictionary(word)
            filtered_response = parse_response(filtered_response, response)
    x = updated_html(html_content, filtered_response)
    open_updated(x)
   

if __name__== "__main__":
    main() 
       