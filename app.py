
from flask import Flask,render_template,request,url_for

def assistant():
    def call():
        import pyttsx3
        import speech_recognition as sr
        import time
        import wikipedia
        from googlesearch import search
        import webbrowser
        import requests
        import os
        import pywhatkit
        import contacts,weather1
        from email.message import EmailMessage
        import ssl,smtplib
        from googletrans import Translator
        from gtts import gTTS
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
        import pygame
        from pydub import AudioSegment
        #import gem
        engine=pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)

        def speak(arf):
            engine.say(arf)
            engine.runAndWait()

        def takecommand():
            tty = sr.Recognizer()
            with sr.Microphone() as source:
                print("Recording...")
                tty.pause_threshold = 0.8
                audio = tty.listen(source)
            try:
                print("Recognizing")
                query = tty.recognize_google(audio, language="en-in")
                print(f"You said: {query}")
            except Exception as e:
                print("I don't understand.")
                speak("I don't understand,please try again:")
                return "None"
            return query
        
        def gem(qu):
            import os
            import logging
            import absl.logging
            from contextlib import contextmanager
            import sys
            import google.generativeai as genai

            @contextmanager
            def suppress_stderr():
                stderr_fileno = sys.stderr.fileno()
                with open(os.devnull, 'w') as devnull:
                    old_stderr = os.dup(stderr_fileno)
                    os.dup2(devnull.fileno(), stderr_fileno)
                    try:
                        yield
                    finally:
                        os.dup2(old_stderr, stderr_fileno)

            absl.logging.use_python_logging()

            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
            os.environ['GRPC_VERBOSITY'] = 'ERROR'
            os.environ['GRPC_CPP_LOG_SEVERITY'] = 'ERROR'

            logging.getLogger('absl').setLevel(logging.ERROR)
            logging.getLogger('grpc').setLevel(logging.ERROR)

            api_key = "AIzaSyDgwyjRVtB0XLiKmboShMPepSZ1L3j8j4I"

            with suppress_stderr():
                genai.configure(api_key=api_key)

            def get_ans(que):
                generation_config = {
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 64,
                    "max_output_tokens": 8192,
                    "response_mime_type": "text/plain",
                }

                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    generation_config=generation_config,
                )

                chat_session = model.start_chat(
                    history=[]
                )

                response = chat_session.send_message(que)

                return response.text
            ans=get_ans(qu)
            return ans




        
        def hin(aud):
            # Sample Hindi text
            text = aud

            # Create gTTS object
            tts = gTTS(text, lang='hi')

            # Save the audio file
            audio_file = "output.mp3"
            tts.save(audio_file)

            audio = AudioSegment.from_file(audio_file)

# Increase playback speed by 1.5x (you can adjust this factor as needed)
            faster_audio = audio.speedup(playback_speed=10)

# Save the modified audio file
            faster_audio_file = "faster_output.mp3"
            faster_audio.export(faster_audio_file, format="mp3")

            # Initialize pygame mixer
            pygame.mixer.init()

            # Load and play the audio file
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            # Keep the script running until the audio finishes
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(2)

            # Optional: Remove the audio file after playing
            #os.remove(audio_file)

        
        def email_s():
            sender_email=contacts.sender_email
            password=contacts.password
            receiver=contacts.receiver

            speak("Enter subject")
            subject=input("Enter subject: ")

            speak("Enter message")
            xx=input("Enter message: ")
            #y=""
            yy=xx
            while True:
                x=input()
                if x=="done":
                    break
                yy=yy+"\n"+x

            em=EmailMessage()
            em['From']=sender_email
            em['To']=receiver
            em['subject']=subject
            em.set_content(yy)

            context=ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(sender_email,password)
                smtp.sendmail(sender_email,receiver,em.as_string())
            speak("Email sent successfully.")

            



        while True:
            speak("Hello sir, how can i help you?")
            que = takecommand()
            query = que.lower()




            if ("search" in query and ("on youtube" in query or "in youtube" in query)):
                res = query.replace("search", "")
                if "on youtube" in res:
                    ser = res.replace("on youtube", "")
                else:
                    ser=res.replace("in youtube","")
                url = f"https://www.youtube.com/results?search_query={ser}"
                speak(f"Searching {ser} on youtube.")
                webbrowser.open(url)
                break

            elif("search" in query):
                query=query.replace("search","")
                speak(f"Searching {query}.")
                url="https://www.google.com/search?q="+query
                webbrowser.open(url)
                break

            elif("email" in query or "mail" in query):
                speak("Enter email.")
                contacts.receiver=input("Enter email: ")
                email_s()
                break

            #elif("weather" in query or "whether" in query or "rain" in query):
            elif "swdefe" in query:
                city, region, country, lat, lon = weather1.get_current_location()
                weather = weather1.get_weather(lat, lon)
                if weather:
                    current_weather = weather['current_weather']
                    precipitation_probability = weather['hourly']['precipitation_probability'][0] if 'precipitation_probability' in weather['hourly'] else 'No data'
                    if("weather" in query or "whether" in query):
                        
                        print(f"Weather in {city} is {current_weather['temperature']} °C")
                        speak(f"Weather in {city} is {current_weather['temperature']} degrees celcius.")
                        #rain=precipitation_probability.replace("%","")
                        print(f"Chance of rain is {precipitation_probability} %")
                        speak(f"Chance of rain is {precipitation_probability} percent.")
                    else:
                        print(f"Chance of rain is {precipitation_probability} %")
                        speak(f"Chance of rain is {precipitation_probability} percent.")
                break
                
            

            elif ("time" in query):
                temp_time = time.localtime()
                timet = time.strftime("%I:%M %p", temp_time)
                speak(f"The time is {timet}")
                break

            elif("lock" in query):
                speak("Locking this PC.")
                loc="D:\\Power options\\Lock.bat"
                os.startfile(loc)
                break

            elif ("shutdown" in query or "shut down" in query):
                speak("Shutting down this PC.")
                loc = "D:\\Power options\\shutdown.bat"
                os.startfile(loc)
                break

            elif ("sleep" in query or "slip" in query):
                speak("Sleeping this PC.")
                loc = "D:\\Power options\\sleep.bat"
                os.startfile(loc)
                break

            elif ("restart" in query):
                speak("Restarting this PC.")
                loc = "D:\\Power options\\restart.bat"
                os.startfile(loc)
                break

            elif ("sign" in query):
                speak("Signing out of this User.")
                loc = "D:\\Power options\\sign.bat"
                os.startfile(loc)
                break

            elif ("open" in query):
                query = query.replace("open", "")
                num_results = 1
                search_results = search(query, num=num_results, lang="en")
                for i, result in enumerate(search_results, start=1):
                    url = result
                    break
                speak(f"Opening {query}")
                webbrowser.open(url)
                break

            elif ("wikipedia" in query):
                query = query.replace("wikipedia", "")
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to wikipedia")
                    print(results)
                    speak(results)
                    break
                except Exception as e:
                    speak("I don't know the answer.")
                    break
            
            elif "translate" in query:
                query=query.replace("translate","")
                def translate_text(text, src_lang='en', dest_lang='hi'):
                    translator = Translator()
                    try:
                        translated = translator.translate(text, src=src_lang, dest=dest_lang)
                        return translated.text
                    except Exception as e:
                        print(f"Error: {e}")
                        return None


                text_to_translate = query
                translated_text = translate_text(text_to_translate, src_lang='en', dest_lang='hi')
                if translated_text:
                    #print(f"Original text: {text_to_translate}")
                    print(f"Translated text in Hindi: {translated_text}")
                    #print(f"Transliterated text: {transliterated_text}")
                    hin(translated_text)
                    break

                
                    


            elif ("play music" in query):
                locc = "D:\\Songs"
                songs = os.listdir(locc)
                speak("Playing music")
                os.startfile(os.path.join(locc, songs[0]))
                break

            elif ("play" in query):
                query = query.replace("play", "")
                API_KEY = "AIzaSyAyDqrXj9_cR40CC5vwoquAT1dItqaD--M"

                search_url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    'part': 'snippet',
                    'q': query,
                    'maxResults': 1,
                    'type': 'video',
                    'key': API_KEY
                }

                response = requests.get(search_url, params=params)
                if response.status_code == 200:
                    search_results = response.json()
                    video_id = search_results['items'][0]['id']['videoId']
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    speak(f"playing{query}")
                    webbrowser.open(video_url)
                break

            elif ("vs" in query or "visual" in query):
                query = query.replace("open", "")
                app_loc = "C:\\Users\\Kartik\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                speak(f"Opening{query}")
                os.startfile(app_loc)
                break


            elif (("whatsapp" in query or "whats app" in query)):
                speak("Tell me the name: ")
                numb1 ="None"
                while True:
                    if numb1=="None":      
                        numb1 = takecommand()
                    else:
                        break
                
                num=""
                temp=0
                while True:
                    
                    for i,j in contacts.numbers.items():
                        if i.lower()==numb1.lower():
                            num=j
                            print(num)
                            temp=1
                            break
                    if temp==1:
                        break
                    else:
                        speak(f"{numb1} not found. Please tell me another name.")
                        numb1=takecommand()    
                speak("What's the message?")
                if num.startswith("+91"):
                    numb = num
                else:
                    numb="+91"+num
                mssg="None"
                while True:
                    if mssg=="None":      
                        mssg = takecommand()
                    else:
                        break

                speak("Sending message")
                print(numb,";")
                pywhatkit.sendwhatmsg_instantly(numb, mssg, wait_time=15, tab_close=True)
                break

            elif ("repeat" in query):
                speak("what do you want me to repeat?")
                repe = takecommand()
                speak(repe)
                break
            
            

            # elif any(keyword in query for keyword in ["what", "who","how","are","am","good","my","name","is"]):
            #     import json
            #     from difflib import get_close_matches

            #     def load_err(file_path: str) -> dict:
            #         try:
            #             with open(file_path, 'r') as file:
            #                 data = json.load(file)
            #         except FileNotFoundError:
            #             data = {"questions": []}
            #             save_err(file_path, data)
            #         return data

            #     def save_err(file_path: str, data: dict):
            #         with open(file_path, 'w') as file:
            #             json.dump(data, file, indent=2)

            #     def find_best_match(user_question: str, questions: list[str]) -> str | None:
            #         matches = get_close_matches(user_question, questions, n=1, cutoff=0.9)
            #         return matches[0] if matches else None

            #     def get_answer_for_question(question: str, err: dict) -> str | None:
            #         for q in err["questions"]:
            #             if q["question"] == question:
            #                 return q["answer"]

            #     def chat_bot():
            #         err = load_err('err.json')

            #         while True:
            #             user_input = query
            #             if user_input.lower() == "quit":
            #                 break

            #             question_list = [q["question"] for q in err["questions"]]
            #             best_match = find_best_match(user_input, question_list)

            #             if best_match:
            #                 answer = get_answer_for_question(best_match, err)
            #                 print(f"Bot: {answer}")
            #                 speak(answer)
            #                 break
            #             else:
            #                 speak("I don't know the answer to that. Please tell me the answer")
            #                 new_answer = takecommand()
            #                 if new_answer.lower() != "skip":
            #                     err["questions"].append({"question": user_input, "answer": new_answer})
            #                     save_err('err.json', err)
            #                     speak("Thank you! I've learned a new response.")
            #                     break

                
            #     chat_bot()
            #     break

            elif (query.startswith("hello")):
                speak("Hello sir, what should i do?")

            elif ("exit" in query or "nothing" in query):
                timew = time.localtime()
                tiime = time.strftime("%H", timew)
                if (int(tiime) > 21 and int(tiime) <= 24):
                    speak("Okay sir, good night")
                    
                elif (int(tiime) >= 0 and int(tiime) < 4):
                    speak("Okay sir, good night")
                else:
                    speak("okay sir, have a good day")
                break

            #elif any(keyword in query for keyword in ["what", "who","how","are","am","good","my","name","is"]):
            elif query!="none":
                ccc=0
                if "code" in query.lower() and "write" in query.lower():
                    quee=query+"without comments, only code"
                    ccc+=1
                else:
                    quee=query
                
                uu=gem(quee)
                print(uu)
                if ccc==0:
                    speak(uu)
                else:
                    xx=query.replace('write a',"")
                    speak(f"here is the {xx}")
    if __name__=="__main__":
        call()






app=Flask(__name__)
@app.route("/")
def home():
    return render_template('assist.html')



@app.route('/command', methods=['GET','POST'])
def command():
    if request.method=='POST':
        assistant()
        return "hgdfh"
    

if __name__=="__main__":
    app.run(debug=True)
