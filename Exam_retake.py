# Import the colorama module for colored terminal output
import colorama
from colorama import Fore, Back, Style
import requests
import json
import re
import time

# Initialize colorama
colorama.init(autoreset=True)

# Display the header
print(Fore.YELLOW + """
.............................
.    Regive Exam Script    .
.    BY: GAURAV KR.        .
............................
""" + Style.RESET_ALL)

def authenticate_user(username, password):
    url = "https://erp.nttftrg.com/rest/mobile/authenticate/user"
    payload = {
        "userName": username,
        "password": password
    }
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://nttf.ilearn.edusquares.com",
        "Referer": "https://nttf.ilearn.edusquares.com/",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("status") == 1:
            user_id = response_data.get("data", {}).get("userId")
            print(f"{Fore.GREEN}✅ Authentication successful. User ID: {user_id}{Style.RESET_ALL}")
            return user_id, response_data
        else:
            print(f"{Fore.RED}❌ Authentication failed: {response_data.get('message')}{Style.RESET_ALL}")
            return None, None
    else:
        print(f"{Fore.RED}❌ Authentication request failed with status code: {response.status_code}{Style.RESET_ALL}")
        return None, None

def fetch_test_password_and_url(tenant, test_id, user_id):
    url = "https://soaz3ulallctn6szdu3wwmgmaa0lkepj.lambda-url.ap-southeast-1.on.aws"
    payload = {
        "tenant": tenant,
        "testId": test_id,
        "userId": user_id,
        "isTimer": False,
        "isUpdate": False
    }
    headers = {
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "https://nttf.ilearn.edusquares.com",
        "Referer": "https://nttf.ilearn.edusquares.com/"
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response_data = response.json()
    password = response_data.get("password")
    test_paper_url = response_data.get("testPaperUrl").replace("\\", "")
    return password, test_paper_url

def fetch_test_questions(tenant, test_id, user_id, s3_url):
    url = "https://5or2in4w2avvenkbbm2fpetjle0fijue.lambda-url.ap-southeast-1.on.aws"
    payload = {
        "tenant": tenant,
        "testId": test_id,
        "userId": user_id,
        "s3Url": s3_url
    }
    headers = {
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "https://nttf.ilearn.edusquares.com",
        "Referer": "https://nttf.ilearn.edusquares.com/"
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response_data = response.json()
    return response_data

def submit_answer(tenant, test_id, user_id, question_id, section_id, choice_id, choice_string):
    url = "https://soaz3ulallctn6szdu3wwmgmaa0lkepj.lambda-url.ap-southeast-1.on.aws"
    timestamp = int(time.time() * 1000)
    
    payload = {
        "tenant": tenant,
        "testId": test_id,
        "userId": user_id,
        "t": timestamp,
        "ts": 1,
        "questionid": question_id,
        "sectionid": section_id,
        "attemptedchoiceid": choice_id,
        "attemptedchoicestring": choice_string,
        "status": "A",
        "isTimer": False,
        "isUpdate": True
    }
    
    headers = {
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "https://nttf.ilearn.edusquares.com",
        "Referer": "https://nttf.ilearn.edusquares.com/",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0"
    }
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        print(f"{Fore.GREEN}✅ Answer submitted for Question ID: {question_id}\n{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}❌ Failed to submit answer. Status code: {response.status_code}{Style.RESET_ALL}")
        return False

def remove_span_tags(text):
    if not text:
        return ""
    return re.sub(r'</?span>', '', text)

def get_choice_details(choices, user_input):
    user_input = user_input.upper()
    for choice in choices:
        if choice.get('choiceString', '') == user_input:
            return choice.get('id'), choice.get('choiceString')
    return None, None

def main():
    tenant = "nttf2"
    username = input(Fore.CYAN + "Enter your username: " + Style.RESET_ALL)
    password = input(Fore.CYAN + "Enter your password: " + Style.RESET_ALL)
    
    user_id, auth_data = authenticate_user(username, password)
    if not user_id:
        print(Fore.RED + "Exiting." + Style.RESET_ALL)
        return
    
    test_id = input(Fore.CYAN + "Enter the test ID: " + Style.RESET_ALL)
    test_password, test_paper_url = fetch_test_password_and_url(tenant, test_id, user_id)
    print(f"{Fore.MAGENTA}📝 Test password: {test_password}{Style.RESET_ALL}")
    
    test_data = fetch_test_questions(tenant, test_id, user_id, test_paper_url)
    
    if 'data' not in test_data or 'sections' not in test_data['data']:
        print(f"{Fore.RED}⚠️ Test data not found.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.BLUE}🔍 Starting test...\n{Style.RESET_ALL}")
    for section in test_data['data']['sections']:
        section_id = section.get('id')
        questions = section.get('questions', [])
        
        for i, question in enumerate(questions, 1):
            question_text = remove_span_tags(question.get('statement', ''))
            question_id = question.get('id')
            choices = question.get('choices', [])
            
            print(f"\n{Fore.YELLOW}Question {i}: {question_text}{Style.RESET_ALL}")
            for choice in choices:
                label = choice.get('choiceString')
                text = remove_span_tags(choice.get('name', ''))
                print(f"{Fore.WHITE}  {label}: {text}{Style.RESET_ALL}")
            
            while True:
                user_input = input(Fore.CYAN + "Your answer (a/b/c/d): " + Style.RESET_ALL).strip().lower()
                if user_input in ['a', 'b', 'c', 'd']:
                    choice_id, choice_string = get_choice_details(choices, user_input)
                    if choice_id:
                        submit_answer(tenant, test_id, user_id, question_id, section_id, choice_id, choice_string)
                        break
                    else:
                        print(f"{Fore.RED}❌ Invalid option. Try again.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Please enter a valid choice (a/b/c/d).{Style.RESET_ALL}")
    
    # ✅ Submit test after all questions
    print(f"{Fore.BLUE}📤 Submitting full test...{Style.RESET_ALL}")
    final_submit_url = "https://soaz3ulallctn6szdu3wwmgmaa0lkepj.lambda-url.ap-southeast-1.on.aws"
    final_payload = {
        "tenant": tenant,
        "testId": int(test_id),
        "userId": [user_id],
        "testSubmit": True,
        "submitStatus": 1,
        "autoSubmitToRDS": True,
        "siteUrl": "https://erp.nttftrg.com/"
    }
    headers = {
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "https://nttf.ilearn.edusquares.com",
        "Referer": "https://nttf.ilearn.edusquares.com/",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0"
    }

    response = requests.post(final_submit_url, data=json.dumps(final_payload), headers=headers)

    if response.status_code == 200:
        print(f"{Fore.GREEN}✅ Test submitted successfully! \n \n ................\n New Marks Updated in ERP Server \n BY: GAURAV KR KALINDI \n ................{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Test submission failed. Status: {response.status_code}{Style.RESET_ALL}")
        print(f"{Fore.RED}Response: {response.text}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
