# import streamlit as st
# import nltk
# import spacy
# from nltk.corpus import stopwords
# nltk.download('stopwords')
# spacy.load('en_core_web_sm')
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import pandas as pd
# import base64, random
# import time, datetime
# from pyresparser import ResumeParser
# from pdfminer3.layout import LAParams, LTTextBox
# from pdfminer3.pdfpage import PDFPage
# from pdfminer3.pdfinterp import PDFResourceManager
# from pdfminer3.pdfinterp import PDFPageInterpreter
# from pdfminer3.converter import TextConverter
# import io, random
# from streamlit_tags import st_tags
# from PIL import Image
# import pymysql
# from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
# import pafy
# import plotly.express as px
# import youtube_dl

# def fetch_yt_video(link):
#     video = pafy.new(link)
#     return video.title

# def get_table_download_link(df, filename, text):
#     """Generates a link allowing the data in a given panda dataframe to be downloaded
#     in:  dataframe
#     out: href string
#     """
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
#     href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
#     return href

# def pdf_reader(file):
#     resource_manager = PDFResourceManager()
#     fake_file_handle = io.StringIO()
#     converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
#     page_interpreter = PDFPageInterpreter(resource_manager, converter)
#     with open(file, 'rb') as fh:
#         for page in PDFPage.get_pages(fh,
#                                       caching=True,
#                                       check_extractable=True):
#             page_interpreter.process_page(page)
#         text = fake_file_handle.getvalue()

#     # close open handles
#     converter.close()
#     fake_file_handle.close()
#     return text

# def show_pdf(file_path):
#     with open(file_path, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#     pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
#     st.markdown(pdf_display, unsafe_allow_html=True)

# def course_recommender(course_list):
#     st.subheader("*Courses & Certificates🎓 Recommendations*")
#     c = 0
#     rec_course = []
#     no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
#     random.shuffle(course_list)
#     for c_name, c_link in course_list:
#         c += 1
#         st.markdown(f"({c}) [{c_name}]({c_link})")
#         rec_course.append(c_name)
#         if c == no_of_reco:
#             break
#     return rec_course

# connection = pymysql.connect(host='localhost', user='root', password='root')
# cursor = connection.cursor()

# def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills,
#                 courses):
#     DB_table_name = 'user_data'
#     insert_sql = "insert into " + DB_table_name + """
#     values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
#     rec_values = (
#     name, email, str(res_score), timestamp, str(no_of_pages), reco_field, cand_level, skills, recommended_skills,
#     courses)
#     cursor.execute(insert_sql, rec_values)
#     connection.commit()

# st.set_page_config(
#     page_title="Smart Resume Analyzer",
#     page_icon='./Logo/SRA_Logo.ico',
# )

# def run():
#     st.title("Smart Resume Analyser")
#     st.sidebar.markdown("# Choose User")
#     activities = ["Normal User", "Admin"]
#     choice = st.sidebar.selectbox("Choose among the given options:", activities)
#     img = Image.open('./Logo/logo.png')
#     img = img.resize((250, 250))
#     st.image(img)

#     # Create the DB
#     db_sql = """CREATE DATABASE IF NOT EXISTS SRA;"""
#     cursor.execute(db_sql)
#     connection.select_db("sra")

#     # Create table
#     DB_table_name = 'user_data'
#     table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
#                     (ID INT NOT NULL AUTO_INCREMENT,
#                      Name varchar(100) NOT NULL,
#                      Email_ID VARCHAR(50) NOT NULL,
#                      resume_score VARCHAR(8) NOT NULL,
#                      Timestamp VARCHAR(50) NOT NULL,
#                      Page_no VARCHAR(5) NOT NULL,
#                      Predicted_Field VARCHAR(25) NOT NULL,
#                      User_level VARCHAR(30) NOT NULL,
#                      Actual_skills VARCHAR(300) NOT NULL,
#                      Recommended_skills VARCHAR(300) NOT NULL,
#                      Recommended_courses VARCHAR(600) NOT NULL,
#                      PRIMARY KEY (ID));
#                     """
#     cursor.execute(table_sql)
#     if choice == 'Normal User':
#         pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
#         if pdf_file is not None:
#             save_image_path = './Uploaded_Resumes/' + pdf_file.name
#             with open(save_image_path, "wb") as f:
#                 f.write(pdf_file.getbuffer())
#             show_pdf(save_image_path)
#             resume_data = ResumeParser(save_image_path).get_extracted_data()
#             if resume_data:                
#                 resume_text = pdf_reader(save_image_path)       
#                 st.header("*Resume Analysis*")
#                 st.success("Hello " + resume_data['name'])
#                 st.subheader("*Your Basic info*")
#                 try:
#                     st.text('Name: ' + resume_data['name'])
#                     st.text('Email: ' + resume_data['email'])
#                     st.text('Contact: ' + resume_data['mobile_number'])
#                     st.text('Resume pages: ' + str(resume_data['no_of_pages']))
#                 except:
#                     pass
#                 cand_level = ''
#                 if resume_data['no_of_pages'] == 1:
#                     cand_level = "Fresher"
#                     st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are looking Fresher.</h4>''',
#                                 unsafe_allow_html=True)
#                 elif resume_data['no_of_pages'] == 2:
#                     cand_level = "Intermediate"
#                     st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',
#                                 unsafe_allow_html=True)
#                 elif resume_data['no_of_pages'] >= 3:
#                     cand_level = "Experienced"
#                     st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',
#                                 unsafe_allow_html=True)

#                 st.subheader("*Skills Recommendation💡*")
#                 ## Skill shows
#                 keywords = st_tags(label='### Skills that you have',
#                                    text='See our skills recommendation',
#                                    value=resume_data['skills'], key='1')

#                 ##  recommendation
#                 ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep Learning', 'flask',
#                               'streamlit']
#                 web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
#                                'javascript', 'angular js', 'c#', 'flask']
#                 android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
#                 ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
#                 uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
#                                 'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
#                                 'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
#                                 'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
#                                 'user research', 'user experience']

#                 recommended_skills = []
#                 reco_field = ''
#                 rec_course = ''
#                 ## Courses recommendation
#                 for i in resume_data['skills']:
#                     ## Data science recommendation
#                     if i.lower() in ds_keyword:
#                         print(i.lower())
#                         reco_field = 'Data Science'
#                         st.success("* Our analysis says you are looking for Data Science Jobs.*")
#                         recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
#                                               'Data Mining', 'Clustering & Classification', 'Data Analytics',
#                                               'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
#                                               'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask",
#                                               'Streamlit']
#                         recommended_keywords = st_tags(label='### Recommended skills for you.',
#                                                        text='Recommended skills generated from System',
#                                                        value=recommended_skills, key='2')
#                         st.markdown(
#                             '''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to resume will boost 🚀 the chances of getting a Job</h4>''',
#                             unsafe_allow_html=True)
#                         rec_course = course_recommender(ds_course)
#                         break

#                     ## Web development recommendation
#                     elif i.lower() in web_keyword:
#                         print(i.lower())
#                         reco_field = 'Web Development'
#                         st.success("* Our analysis says you are looking for Web Development Jobs *")
#                         recommended_skills = ['React', 'Django', 'Node js', 'React js', 'PHP', 'Laravel', 'Magento',
#                                               'Wordpress', 'Javascript', 'Angular js', 'c#', 'Flask', 'SDK']
#                         recommended_keywords = st_tags(label='### Recommended skills for you.',
#                                                        text='Recommended skills generated from System',
#                                                        value=recommended_skills, key='3')
#                         st.markdown(
#                             '''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to resume will boost 🚀 the chances of getting a Job</h4>''',
#                             unsafe_allow_html=True)
#                         rec_course = course_recommender(web_course)
#                         break

#                     ## Android development recommendation
#                     elif i.lower() in android_keyword:
#                         print(i.lower())
#                         reco_field = 'Android Development'
#                         st.success("* Our analysis says you are looking for Android App Development Jobs *")
#                         recommended_skills = ['Android', 'Android Development', 'Flutter', 'Kotlin', 'XML', 'Java',
#                                               'Kivy', 'GIT', 'SDK', 'SQLite']
#                         recommended_keywords = st_tags(label='### Recommended skills for you.',
#                                                        text='Recommended skills generated from System',
#                                                        value=recommended_skills, key='4')
#                         st.markdown(
#                             '''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to resume will boost 🚀 the chances of getting a Job</h4>''',
#                             unsafe_allow_html=True)
#                         rec_course = course_recommender(android_course)
#                         break

#                     ## IOS development recommendation
#                     elif i.lower() in ios_keyword:
#                         print(i.lower())
#                         reco_field = 'IOS Development'
#                         st.success("* Our analysis says you are looking for IOS App Development Jobs *")
#                         recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode', 'SDK',
#                                               'UIKit', 'SQLite', 'GIT', 'JSON', 'SwiftUI']
#                         recommended_keywords = st_tags(label='### Recommended skills for you.',
#                                                        text='Recommended skills generated from System',
#                                                        value=recommended_skills, key='5')
#                         st.markdown(
#                             '''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to resume will boost 🚀 the chances of getting a Job</h4>''',
#                             unsafe_allow_html=True)
#                         rec_course = course_recommender(ios_course)
#                         break

#                     ## Ui-UX development recommendation
#                     elif i.lower() in uiux_keyword:
#                         print(i.lower())
#                         reco_field = 'UI-UX Development'
#                         st.success("* Our analysis says you are looking for UI-UX Development Jobs *")
#                         recommended_skills = ['UI', 'UX', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq', 'Prototyping',
#                                               'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing',
#                                               'Adobe Illustrator', 'Illustrator', 'Adobe After Effects',
#                                               'After Effects', 'Adobe Premier Pro', 'Premier Pro', 'Adobe Indesign',
#                                               'Indesign', 'Wireframe', 'Solid', 'Grasp', 'User Research',
#                                               'User Experience']
#                         recommended_keywords = st_tags(label='### Recommended skills for you.',
#                                                        text='Recommended skills generated from System',
#                                                        value=recommended_skills, key='6')
#                         st.markdown(
#                             '''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to resume will boost 🚀 the chances of getting a Job</h4>''',
#                             unsafe_allow_html=True)
#                         rec_course = course_recommender(uiux_course)
#                         break

#                 st.subheader("*Resume Tips💡*")
#                 resume_score = 0
#                 if 'Objective' in resume_text:
#                     resume_score += 20
#                     st.markdown(
#                         '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective</h4>''',
#                         unsafe_allow_html=True)
#                 else:
#                     st.markdown(
#                         '''<h4 style='text-align: left; color: #fabc10;'>[-] Please add your career objective. It will give the impression to the recruiter that you are clear about your goals and ambitions.</h4>''',
#                         unsafe_allow_html=True)

#                 if 'Declaration' in resume_text:
#                     resume_score += 20
#                     st.markdown(
#                         '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Declaration</h4>''',
#                         unsafe_allow_html=True)
#                 else:
#                     st.markdown(
#                         '''<h4 style='text-align: left; color: #fabc10;'>[-] Please add a declaration in your resume for authentication of the information provided.</h4>''',
#                         unsafe_allow_html=True)

#                 if 'Hobbies' or 'Interests' in resume_text:
#                     resume_score += 20
#                     st.markdown(
#                         '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Hobbies</h4>''',
#                         unsafe_allow_html=True)
#                 else:
#                     st.markdown(
#                         '''<h4 style='text-align: left; color: #fabc10;'>[-] Please add Hobbies. It will show your personal side to the recruiter.</h4>''',
#                         unsafe_allow_html=True)

#                 if 'Achievements' or 'Accomplishments' in resume_text:
#                     resume_score += 20
#                     st.markdown(
#                         '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Achievements</h4>''',
#                         unsafe_allow_html=True)
#                 else:
#                     st.markdown(
#                         '''<h4 style='text-align: left; color: #fabc10;'>[-] Please add Achievements. It will show how skillful you are.</h4>''',
#                         unsafe_allow_html=True)

#                 if 'Projects' in resume_text:
#                     resume_score += 20
#                     st.markdown(
#                         '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Projects</h4>''',
#                         unsafe_allow_html=True)
#                 else:
#                     st.markdown(
#                         '''<h4 style='text-align: left; color: #fabc10;'>[-] Please add Projects. It will show your work experience and strengths.</h4>''',
#                         unsafe_allow_html=True)

#                 st.subheader("*Resume Score📝*")
#                 st.markdown(
#                     """
#                     <style>
#                         .stProgress > div > div > div > div {
#                             background-color: #d73b5c;
#                         }
#                     </style>""",
#                     unsafe_allow_html=True,
#                 )
#                 my_bar = st.progress(0)
#                 score = 0
#                 for percent_complete in range(resume_score):
#                     score += 1
#                     time.sleep(0.1)
#                     my_bar.progress(percent_complete + 1)
#                 st.success('* Your Resume Score: ' + str(score) + '*')
                
#                 def send_confirmation_email(recipient_email, recipient_name):
#     # Sender details
#                     sender_email = "tanisha.2024cse1051@kiet.edu"
#                     sender_password = "Tanisha@123"
    
#     # Create message container
#                     msg = MIMEMultipart()
#                     msg['From'] = sender_email
#                     msg['To'] = recipient_email
#                     msg['Subject'] = "Interview Scheduled"
                    
#                     # Email body
#                     body = f"Dear {recipient_name},\n\nCongratulations! Your interview has been scheduled.\n\nBest regards,\nYour Name"
#                     msg.attach(MIMEText(body, 'plain'))
                    
#                     # Send email
#                     try:
#                         server = smtplib.SMTP('smtp.example.com', 587)  # Update with your SMTP server details
#                         server.starttls()
#                         server.login(sender_email, sender_password)
#                         text = msg.as_string()
#                         server.sendmail(sender_email, recipient_email, text)
#                         server.quit()
#                         st.success("Confirmation email sent successfully!")
#                     except Exception as e:
#                         st.error("Failed to send confirmation email. Please try again later.")
                                
                                
#             if score >= 14:
#                 if st.button('You qualify for an interview! Click here to schedule it.'):
#                     # Send confirmation email
#                     send_confirmation_email(resume_data['email'], resume_data['name'])
#                     # Redirect to interview scheduling page
#                     st.markdown('<meta http-equiv="refresh" content="0;url="">', unsafe_allow_html=True)


#                 else:
#                     st.markdown('''<h4 style='text-align: left; color: #fabc10;'>Your resume needs some improvement to qualify for an interview.</h4>''', unsafe_allow_html=True)

#                     ts = time.time()
#                     cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
#                     cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
#                     timestamp = str(cur_date + '_' + cur_time)

#                     insert_data(resume_data['name'], resume_data['email'], str(score), timestamp, str(resume_data['no_of_pages']),
#                                 reco_field, cand_level, str(keywords), str(recommended_keywords), str(rec_course))

#                     connection.commit()

#             else:
#                 st.error('Currently, only Normal User mode is supported in this demo.')

# run()

import streamlit as st
import nltk
import spacy
from nltk.corpus import stopwords
nltk.download('stopwords')
spacy.load('en_core_web_sm')
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import base64, random
import time, datetime
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io, random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
import pafy
import plotly.express as px
import youtube_dl
import os
from dotenv import load_dotenv

load_dotenv()  
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
INTERVIEW_LINK =  os.getenv("INTERVIEW_LINK") 

def send_confirmation_email(recipient_email, recipient_name):
    # Sender details
    sender_email = SENDER_EMAIL
    sender_password = SENDER_PASSWORD
    
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Interview Scheduled"
    
    # Email body
    body = f"Dear {recipient_name},\n\nCongratulations! Your interview has been scheduled.\n\nBest regards,\nYour Name"
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)  # Update with your SMTP server details
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Confirmation email sent successfully!")
    except Exception as e:
        print(f"Failed to send confirmation email. Error: {e}")
    



def fetch_yt_video(link):
    video = pafy.new(link)
    return video.title

def get_table_download_link(df, filename, text):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.subheader("*Courses & Certificates🎓 Recommendations*")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course

connection = pymysql.connect(host='localhost', user='root', password='root')
cursor = connection.cursor()

def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills,
                courses):
    DB_table_name = 'user_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (
    name, email, str(res_score), timestamp, str(no_of_pages), reco_field, cand_level, skills, recommended_skills,
    courses)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon='./Logo/SRA_Logo.ico',
)

def run():
    st.title("Smart Resume Analyser")
    st.sidebar.markdown("# Choose User")
    activities = ["Normal User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    img = Image.open('./Logo/SRA_Logo.jpg')
    img = img.resize((250, 250))
    st.image(img)

    # Create the DB
    db_sql = """CREATE DATABASE IF NOT EXISTS SRA;"""
    cursor.execute(db_sql)
    connection.select_db("sra")

    # Create table
    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(100) NOT NULL,
                     Email_ID VARCHAR(50) NOT NULL,
                     resume_score VARCHAR(8) NOT NULL,
                     Timestamp VARCHAR(50) NOT NULL,
                     Page_no VARCHAR(5) NOT NULL,
                     Predicted_Field VARCHAR(25) NOT NULL,
                     User_level VARCHAR(30) NOT NULL,
                     Actual_skills VARCHAR(300) NOT NULL,
                     Recommended_skills VARCHAR(300) NOT NULL,
                     Recommended_courses VARCHAR(600) NOT NULL,
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)
    if choice == 'Normal User':
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            save_image_path = './Uploaded_Resumes/' + pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            show_pdf(save_image_path)
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            if resume_data:                
                resume_text = pdf_reader(save_image_path)       
                st.header("*Resume Analysis*")
                st.success("Hello " + resume_data['name'])
                st.subheader("*Your Basic info*")
                try:
                    st.text('Name: ' + resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Contact: ' + resume_data['mobile_number'])
                    st.text('Resume pages: ' + str(resume_data['no_of_pages']))
                except:
                    pass
                cand_level = ''
                if resume_data['no_of_pages'] == 1:
                    cand_level = "Fresher"
                    st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are looking Fresher.</h4>''',
                                unsafe_allow_html=True)
                elif resume_data['no_of_pages'] == 2:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',
                                unsafe_allow_html=True)
                elif resume_data['no_of_pages'] >= 3:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',
                                unsafe_allow_html=True)

                st.subheader("*Skills Recommendation💡*")
                ## Skill shows
                keywords = st_tags(label='### Skills that you have',
                                   text='See our skills recommendation',
                                   value=resume_data['skills'], key='1')

                ##  recommendation
                ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep Learning', 'flask',
                              'streamlit']
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                               'javascript', 'angular js', 'c#', 'flask']
                android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
                ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
                uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
                                'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
                                'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
                                'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
                                'user research', 'user experience']

                recommended_skills = []
                reco_field = ''
                rec_course = ''
                ## Courses recommendation
                for i in resume_data['skills']:
                    ## Data science recommendation
                    if i.lower() in ds_keyword:
                        print(i.lower())
                        reco_field = 'Data Science'
                        st.success("* Our analysis says you are looking for Data Science Jobs.*")
                        recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
                                              'Data Mining', 'Clustering & Classification', 'Data Analytics',
                                              'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
                                              'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask",
                                              'Streamlit']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                       text='Recommended skills generated from System',
                                                       value=recommended_skills, key='2')
                        st.markdown(
                            '''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to resume will boost 🚀 the chances of getting a Job</h4>''',
                            unsafe_allow_html=True)
                        rec_course = course_recommender(ds_course)
                        break

                    ## Web development recommendation
                    elif i.lower() in web_keyword:
                        print(i.lower())
                        reco_field = 'Web Development'
                        st.success("* Our analysis says you are looking for Web Development Jobs *")
                        recommended_skills = ['React', 'Django', 'Node js', 'React js', 'PHP', 'Laravel', 'Magento',
                                              'Wordpress', 'Javascript', 'Angular js', 'c#', 'Flask', 'SDK']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                       text='Recommended skills generated from System',
                                                       value=recommended_skills, key='3')
                        st.markdown(
                            '''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to resume will boost 🚀 the chances of getting a Job</h4>''',
                            unsafe_allow_html=True)
                        rec_course = course_recommender(web_course)
                        break

                    ## Android development recommendation
                    elif i.lower() in android_keyword:
                        print(i.lower())
                        reco_field = 'Android Development'
                        st.success("* Our analysis says you are looking for Android App Development Jobs *")
                        recommended_skills = ['Android', 'Android Development', 'Flutter', 'Kotlin', 'XML', 'Java',
                                              'Kivy', 'GIT', 'SDK', 'SQLite']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                       text='Recommended skills generated from System',
                                                       value=recommended_skills, key='4')
                        st.markdown(
                            '''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to resume will boost 🚀 the chances of getting a Job</h4>''',
                            unsafe_allow_html=True)
                        rec_course = course_recommender(android_course)
                        break

                    ## IOS development recommendation
                    elif i.lower() in ios_keyword:
                        print(i.lower())
                        reco_field = 'IOS Development'
                        st.success("* Our analysis says you are looking for IOS App Development Jobs *")
                        recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode', 'SDK',
                                              'UIKit', 'SQLite', 'GIT', 'JSON', 'SwiftUI']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                       text='Recommended skills generated from System',
                                                       value=recommended_skills, key='5')
                        st.markdown(
                            '''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to resume will boost 🚀 the chances of getting a Job</h4>''',
                            unsafe_allow_html=True)
                        rec_course = course_recommender(ios_course)
                        break

                    ## Ui-UX development recommendation
                    elif i.lower() in uiux_keyword:
                        print(i.lower())
                        reco_field = 'UI-UX Development'
                        st.success("* Our analysis says you are looking for UI-UX Development Jobs *")
                        recommended_skills = ['UI', 'UX', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq', 'Prototyping',
                                              'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing',
                                              'Adobe Illustrator', 'Illustrator', 'Adobe After Effects',
                                              'After Effects', 'Adobe Premier Pro', 'Premier Pro', 'Adobe Indesign',
                                              'Indesign', 'Wireframe', 'Solid', 'Grasp', 'User Research',
                                              'User Experience']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                       text='Recommended skills generated from System',
                                                       value=recommended_skills, key='6')
                        st.markdown(
                            '''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to resume will boost 🚀 the chances of getting a Job</h4>''',
                            unsafe_allow_html=True)
                        rec_course = course_recommender(uiux_course)
                        break

                st.subheader("*Resume Tips💡*")
                resume_score = 0
                if 'Objective' in resume_text:
                    resume_score += 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>[-] Please add your career objective. It will give the impression to the recruiter that you are clear about your goals and ambitions.</h4>''',
                        unsafe_allow_html=True)

                if 'Declaration' in resume_text:
                    resume_score += 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Declaration</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>[-] Please add a declaration in your resume for authentication of the information provided.</h4>''',
                        unsafe_allow_html=True)

                if 'Hobbies' or 'Interests' in resume_text:
                    resume_score += 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Hobbies</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>[-] Please add Hobbies. It will show your personal side to the recruiter.</h4>''',
                        unsafe_allow_html=True)

                if 'Achievements' or 'Accomplishments' in resume_text:
                    resume_score += 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Achievements</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>[-] Please add Achievements. It will show how skillful you are.</h4>''',
                        unsafe_allow_html=True)

                if 'Projects' in resume_text:
                    resume_score += 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Projects</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>[-] Please add Projects. It will show your work experience and strengths.</h4>''',
                        unsafe_allow_html=True)

                st.subheader("*Resume Score📝*")
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #d73b5c;
                        }
                    </style>""",
                    unsafe_allow_html=True,
                )
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score += 1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)
                st.success('* Your Resume Score: ' + str(score) + '*')
                
                
                
                
                if score >= 14:
                    
                    if st.button('You qualify for an interview! Click here to schedule it.'):
                        send_confirmation_email(resume_data['email'],resume_data['name'])
                        print('email sent successfully')
                 
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>Your resume needs some improvement to qualify for an interview.</h4>''', unsafe_allow_html=True)
 
                    ts = time.time()
                    cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    timestamp = str(cur_date + '_' + cur_time)

                    insert_data(resume_data['name'], resume_data['email'], str(score), timestamp, str(resume_data['no_of_pages']),
                            reco_field, cand_level, str(keywords), str(recommended_keywords), str(rec_course))

                    connection.commit()

        else:
            st.error('Currently, only Normal User mode is supported in this demo.')

run()