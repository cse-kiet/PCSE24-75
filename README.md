# Smart Resume Analyser App
[![Python 3.8.10]  
## Abstarct
In the current job market, recruiters face challenges with the substantial number of resumes they receive. This often results in time-consuming and ineffective screening procedures. To tackle this problem, we introduce the Resume Parser with AI Voice Bot project. This innovative solution uses advanced natural language processing techniques to simplify the candidate selection process. Our project aims to automate the process of parsing resumes, extracting relevant information, and providing mock interviews autonomously. By leveraging state-of-the-art NLP algorithms, the system can analyze resumes to identify crucial qualifications, skills, and experiences, making candidate categorization more precise.
Incorporating advanced technologies into it, our social initiative project seeks to change the way we hire new employees. Within it, there are several primary aspects. One of them is a tool for analyzing resumes via intelligent systems that apply specifically trained algorithms to collect regular pieces of information from irregularly composed documents. This search covers many areas like lifestyle particulars (job title, phone), academic background, work history (positions held), competence set, and stand-out results achieved during the previous tenure periods.
One of the main reasons why you would combine a Resume Parser with an AI Voice Bot is to help improve the recruitment procedure by making it a less manual and time-consuming process of scanning resumes. When we do get these processes automated though, we expect a better chance at assessing employees’ quality- making recruitment more streamlined while at the same time being effective. By offering these tools like data analytics, the system gives recruiters a proper understanding to the extent that they can make valid decisions.
This project is a significant development in Human Resources (HR) because it applies Natural Language Processing (NLP) approaches to automate the traditional recruitment process. Tests have shown that this system is reliable and efficient when used during actual recruitment processes, thus offering a strong solution that improves the evaluation standards while at the same time lowering the administrative load involved.


## Source
- Extracting user's information from the Resume, I used [PyResparser](https://omkarpathak.in/pyresparser/)
- Extracting Resume PDF into Text, I used [PDFMiner](https://pypi.org/project/pdfminer/).

## Features
- User's & Admin Section
- Resume Score
- Career Recommendations
- Resume writing Tips suggestions
- Courses Recommendations
- Skills Recommendations
- Youtube video recommendations

## Usage
- Clone my repository.
- Open CMD in working directory.
- Run following command.
  ```
  pip install -r requirements.txt
  ```
- `App.py` is the main Python file of Streamlit Web-Application. 
- `Courses.py` is the Python file that contains courses and youtube video links.
- Download XAMP or any other control panel, and turn on the Apache & SQL service.
- To run app, write following command in CMD. or use any IDE.
  ```
  streamlit run App.py
  ```
- `Uploaded_Resumes` folder is contaning the user's uploaded resumes.
- `Classifier.py` is the main file which is containing a KNN Algorithm.
- For more explanation of this project see the tutorial on Machine Learning Hub YouTube channel.
- Admin side credentials is `machine_learning_hub` and password is `mlhub123`. 


