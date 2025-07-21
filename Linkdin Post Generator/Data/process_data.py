import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from LLM_code import llm

# Data/process_data.py
# This script processes LinkedIn posts by extracting metadata such as line count, language, and tags

def process_post(raw_file_path, processed_file_path="data/process_posts.json"):
    enriched_posts = []
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    for epost in enriched_posts:
        print(epost)

    # Ensure the output directory exists
    output_dir = os.path.dirname(processed_file_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save enriched posts to the specified processed_file_path
    with open(processed_file_path, "w", encoding="utf-8") as outfile:
        json.dump(enriched_posts, outfile, ensure_ascii=False, indent=4)



def extract_metadata(post_1):
    template = """
    you are given a Linkdin Post.You need to extract numbers of lines, 
    language of the posts and tags. 
    1. Return a valid JSON. No Preamble
    2. JSON object should have exactly three keys:line_count,language and tags.
    3. Tags is an array of text tags. Extract maximum two tags. 
    4. Language should be English .
    
    Here is the actual post on which you need to perform this task:
    {post_2}
    
    
    """
    
    prompt_t = PromptTemplate.from_template(template)
    chain = prompt_t | llm
    llm_response = chain.invoke(input={'post_2':post_1})
    
    
    
    try:
        json_parser = JsonOutputParser()
        response = json_parser.parse(llm_response.content)
    except OutputParserException:
        raise OutputParserException("Context too big . Unable to parse jobs.")
    return response



if __name__=="__main__":
    process_post("data/actual_posts.json","data/process_posts.json")
    
    