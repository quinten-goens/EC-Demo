import streamlit as st
import lorem

def app():

    # Use the full page instead of a narrow central column
    st.markdown("<h1 style='text-align: left; color: black;'>About</h1>", unsafe_allow_html=True)
    st.markdown("""
### Data sources
* [ASMA Additional Time Dataset by ANS Performance, provided by the Performance Review Unit (PRU) from EUROCONTROL](https://ansperformance.eu/download/xls/ASMA_Additional_Time.xlsx)
* [European Daily COVID-19 Case Counts by European Centre for Disease Control](https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv)
""")
    st.markdown("""
    ### Sidebar image
* <a href="http://www.freepik.com">Designed by macrovector / Freepik</a>""",unsafe_allow_html=True)
    st.markdown("""
### Future releases and improvements
* Improve loading times further.
* Add automatic data fetching from the EUROCONTROL PRU website or implement an API for more granular data to provide daily up to date data. 
* Add visualizations displaying the impact of the Ukraine crisis on European aviation to the general public dashboard (once data is available).
* Add more visualizations based on provided feedback by the PRU.
* Port the application to a more versatile and scalable cloud platform (e.g. [AWS](https://aws.amazon.com/), [Google Cloud](https://cloud.google.com/), [Azure](https://azure.microsoft.com/en-us/), etc.)
* Create a more robust and flexible user interface by switching to a more function rich dashboarding platform such as e.g., [Dash Plotly](https://plotly.com/dash/) or [Panel](https://panel.holoviz.org/).""")
    st.markdown("""
    ### Software and hosting tools
    Here's a (non-exhaustive) list of the tools used to develop and host this dashboard: """)

    col1, col2,col2_ = st.columns((1,3,1))
    col1.image('resources/python.png', width=150)
    col2.markdown("""
### Python
Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Its language constructs and object-oriented approach aim to help programmers write clear, logical code for small- and large-scale projects.
""")
    

    col3,col4,col4_ = st.columns((1, 3, 1))
    col3.image('resources/streamlit.png', width=200)
    col4.markdown("""
### Streamlit
A faster way to build and deploy data apps. Streamlit is the first app framework built specifically for Machine Learning and Data Science teams. """)
    
    col5, col6, col6_ = st.columns((1, 3, 1))
    col5.image('resources/git.png', width=200)
    col6.markdown("""
### Git and GitHub
Git is a distributed version control system for tracking changes in computer files and coordinating work on those files among multiple people. It is most commonly used to track source code, but is often used to track data as well. Here it was used for versioning code and CI/CD.""")
   

    col7, col8, col8_ = st.columns((1, 3, 1))
    col7.image('resources/plotly.png', width=200)
    col8.markdown("""
### Plotly
Plotly provides online graphing, analytics, and statistics tools for individuals and collaboration, as well as scientific graphing libraries for Python, R, MATLAB, Perl, Julia, Arduino, and REST. 
    """)
    
    col9, col10,col10_ = st.columns((1, 3, 1))
    col9.image('resources/pandas.png', width=200)
    col10.markdown("""
### Pandas
Pandas is a software library written for the Python programming language for data manipulation and analysis. In particular, it offers data structures and operations for manipulating numerical tables and time series.""")
    

    col11, col12,col12_ = st.columns((1, 3, 1))
    col11.image('resources/numpy.png', width=200)
    col12.markdown("""
### Numpy
Numpy is a Python package for scientific computing with Python. It contains among other things a powerful N-dimensional array object and a sophisticated (and flexible) numerical processing library.""")
    
    col13, col14,col14_ = st.columns((1, 3, 1))
    col13.image('resources/docker.png', width=200)
    col14.markdown("""
### Docker
Docker is a platform for developers and sysadmins to build, ship, and run software in a containerized environment. Docker containers can be used to run applications like web servers, databases, and graphical user interfaces. Docker containers can also be used to run software in a virtual machine, such as in a cloud environment.

The application is fully containerized and is hosted by Streamlit.io, but could as easily be hosted on Azure, AWS, Google Cloud, or any other cloud provider because of the containerization.""")

    st.markdown("""
    ### The developer
    The developer of this platform is [Quinten Goens](https://www.linkedin.com/in/quinten-goens-741457144/). A physicist and astronomer who gained affinity and skills in data analytics / science, data engineering and cloud architecture throughout his studies and follow up career as a Data Analyst / Data Engineer. Quinten has a particular passion for dashboard development and data visualization and interpretation. During his free time he can be found in the indoor climbing halls around Brussels with friends or learning new data / cloud skills at home or in a cosy coffee place.   
    """)

    if st.button("Hire me"):
        st.balloons()
        st.markdown("""Get in touch via: QGoens@gmail.com""")