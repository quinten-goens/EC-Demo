import streamlit as st
import lorem    

def app():

    # Use the full page instead of a narrow central column
    st.markdown("<h1 style='text-align: left; color: black;'>Queries and Views</h1>", unsafe_allow_html=True)
    st.markdown("""
### Question Two
Given the ER diagram from Question 1:
* **Part I: Write a query to extract the data as in the DATA sheet in the original dataset.**
* **Part II: Define some example views to ease queries by an operational analysts and sketch them out.**""")
    
    st.markdown("""
### Part I: Recreate dataset through SQL Query
    """)
    col2,col1 = st.columns((2,3))
    col1.markdown("""
**Tables with example row:**

The various tables in the hypothetical database used are named `flight`, `asma_entry`, `airport` and `state`. Here we display a single row for each of these.

**flight AS f**

| id | flight_nr | arrival_date | arrival_time | arrival_airport_id | departure_airport_id | asma_entry_id |
|----|---------------|----------------|--------------|--------------------|----------------------|---------------|
| 1  | AB1234        | 2021-12-31     | 12:20:22     | 2                  | 1                    | 1             |

<br/><br/>
**airport AS a**
| id | name     | icoa | asma_radius | pru_asma_monitoring | state_id |
|----|----------|------|-------------|---------------------|----------|
| 1  | Brussels | EBBR | 40          | TRUE                | 1        |

<br/><br/>
**state AS s**
| id | name |
|----|------|
| 1  | Belgium |

<br/><br/>
**asma_entry AS ae**
| id | asma_entry_time | unimpeded_asma_time | additional_asma_time |
|----|-----------------|-----------------------|---------------------|
| 1  | 12:08:46 | 12.1 | 0.5                   |

    """,unsafe_allow_html=True)
    query = """
SELECT 
  f.arrival_year, 
  f.arrival_month_char, 
  f.arrival_month, 
  a.icao, 
  a.name, 
  s.name, 
  a.asma_radius, 
  COUNT(f.id), 
  SUM(ae.unimpeded_asma_time), 
  SUM(ae.additional_asma_time)
FROM 
  (SELECT 
      date_part('year', flight.arrival_date) as arrival_year, 
      to_char(flight.arrival_date, 'MON') as arrival_month_char, 
      date_part('month', flight.arrival_date) as arrival_month, 
      flight.*
  FROM flight) AS f 
  JOIN asma_entry AS ae ON f.asma_entry_id = ae.id 
  JOIN airport AS a ON f.arrival_airport_id = a.id 
  JOIN state AS s ON a.state_id = s.id 
WHERE 
  a.pru_asma_monitoring = TRUE 
GROUP BY
  f.arrival_year, 
  f.arrival_month_char, 
  f.arrival_month, 
  a.icao, 
  a.name, 
  s.name, 
  a.asma_radius 
ORDER BY 
  f.arrival_year ASC, 
  f.arrival_month ASC, 
  s.name ASC, 
  a.name ASC;
    """
    col2.markdown("""
**Requested query (in PostgreSQL):**

The requested query to obtain the data as provided in the DATA sheet of the XLSX file can be found below. It is written in and tested with PostgreSQL.
""")
    col2.code(query,language='sql')
    st.markdown("""
**Resulting table:**

After renaming columns we get: 
| YEAR | MONTH_MON | MONTH_NUM | APT_ICAO | APT_NAME | STATE_NAME | ASMA_RADIUS | FLT_ASMA_UNIMP_2 | TIME_ASMA_UNIMP_2 | TIME_ASMA_ADD_2 |
|-----|------------|-----------|----------|---------|-----------|-------------|--------------------|-------------------|-------------------|
| 2021 | DEC | 12      | EBBR     | Brussels  | Belgium     | 40          | [count]                 | [sum]                | [sum]                |""")
    st.markdown("""<br></br>""",unsafe_allow_html=True)

    st.markdown("""
### Part II: Define views

Various views can be defined by grouping and aggregating the data in a variety of ways. There are spatial groupings possible (by airport, state or Europe wide) and temporal groupings (by day, month or year). \
    Below we first apply the temporal groupings by year and month and show the different queries for the different spacial groupings. We follow up with the same views but grouped by year only (less temporal granularity). 
    
In order to aid the operational analysts we added two columns to the table indicating the average unimpeded ASMA time `AVG_ASMA_UNIMP_2` and the average additional ASMA time `AVG_ASMA_ADD_2`.      
    
*Note: Temporarily collapsing the web app sidebar allows you to read the queries more easily.*
    """)
    st.markdown("""
#### Temporal grouping: By year and month""")
    col3,col4,col5 = st.columns((1,1,1))
    col3.markdown("""**View 1: Grouped by airport**""")
    query1 = """
SELECT 
  f.arrival_year, 
  f.arrival_month_char, 
  f.arrival_month, 
  a.icao, 
  a.name, 
  s.name, 
  a.asma_radius, 
  COUNT(f.id), 
  SUM(ae.unimpeded_asma_time), 
  SUM(ae.additional_asma_time),
  SUM(ae.unimpeded_asma_time)/COUNT(f.id),
  SUM(ae.additional_asma_time)/COUNT(f.id)
FROM 
  (SELECT 
      date_part('year', flight.arrival_date) as arrival_year, 
      to_char(flight.arrival_date, 'MON') as arrival_month_char, 
      date_part('month', flight.arrival_date) as arrival_month, 
      flight.*
  FROM flight) AS f 
  JOIN asma_entry AS ae ON f.asma_entry_id = ae.id 
  JOIN airport AS a ON f.arrival_airport_id = a.id 
  JOIN state AS s ON a.state_id = s.id 
WHERE 
  a.pru_asma_monitoring = TRUE 
GROUP BY
  f.arrival_year, 
  f.arrival_month_char, 
  f.arrival_month, 
  a.icao, 
  a.name, 
  s.name, 
  a.asma_radius 
ORDER BY 
  f.arrival_year ASC, 
  f.arrival_month ASC, 
  s.name ASC, 
  a.name ASC;
    """
    col3.code(query1,language='sql')

    col4.markdown("""**View 2: Grouped by state**""")
    query2="""
SELECT 
  f.arrival_year, 
  f.arrival_month_char, 
  f.arrival_month, 
  s.name, 
  COUNT(f.id), 
  SUM(ae.unimpeded_asma_time), 
  SUM(ae.additional_asma_time),
  SUM(ae.unimpeded_asma_time)/COUNT(f.id),
  SUM(ae.additional_asma_time)/COUNT(f.id)
FROM 
  (SELECT 
      date_part('year', flight.arrival_date) as arrival_year, 
      to_char(flight.arrival_date, 'MON') as arrival_month_char, 
      date_part('month', flight.arrival_date) as arrival_month, 
      flight.*
  FROM flight) AS f 
  JOIN asma_entry AS ae ON f.asma_entry_id = ae.id 
  JOIN airport AS a ON f.arrival_airport_id = a.id 
  JOIN state AS s ON a.state_id = s.id 
WHERE 
  a.pru_asma_monitoring = TRUE 
GROUP BY
  f.arrival_year, 
  f.arrival_month_char, 
  f.arrival_month, 
  s.name
ORDER BY 
  f.arrival_year ASC, 
  f.arrival_month ASC, 
  s.name ASC
    """
    col4.code(query2,language='sql')

    col5.markdown("""**View 3: No spatial grouping (Europe wide)**""")
    query3="""
SELECT 
  f.arrival_year, 
  f.arrival_month_char, 
  f.arrival_month, 
  COUNT(f.id), 
  SUM(ae.unimpeded_asma_time), 
  SUM(ae.additional_asma_time),
  SUM(ae.unimpeded_asma_time)/COUNT(f.id),
  SUM(ae.additional_asma_time)/COUNT(f.id)
FROM 
  (SELECT 
      date_part('year', flight.arrival_date) as arrival_year, 
      to_char(flight.arrival_date, 'MON') as arrival_month_char, 
      date_part('month', flight.arrival_date) as arrival_month, 
      flight.*
  FROM flight) AS f 
  JOIN asma_entry AS ae ON f.asma_entry_id = ae.id 
  JOIN airport AS a ON f.arrival_airport_id = a.id 
WHERE 
  a.pru_asma_monitoring = TRUE 
GROUP BY
  f.arrival_year, 
  f.arrival_month_char, 
  f.arrival_month
ORDER BY 
  f.arrival_year ASC, 
  f.arrival_month ASC
    """
    col5.code(query3,language='sql')
    st.markdown("""
**Table view 1: Grouped by airport:**

*Note: The table below was split in two rows to improve readability.*

| YEAR | MONTH_MON | MONTH_NUM | APT_ICAO | APT_NAME | STATE_NAME | ASMA_RADIUS | FLT_ASMA_UNIMP_2 | 
|-----|------------|-----------|----------|---------|-----------|-------------|--------------------|
| 2021 | DEC | 12      | EBBR     | Brussels  | Belgium     | 40          | [count]                 | 

<br></br>

| TIME_ASMA_UNIMP_2 | TIME_ASMA_ADD_2 | AVG_ASMA_UNIMP_2 | AVG_ASMA_ADD_2 |
|-------------------|-------------------|-----------------|---------------|
|[sum]                | [sum]                | [mean] |[mean]| 



<br></br>
**Table view 2: Grouped by state:**
 
| YEAR | MONTH_MON | MONTH_NUM | STATE_NAME | FLT_ASMA_UNIMP_2 | TIME_ASMA_UNIMP_2 | TIME_ASMA_ADD_2 | AVG_ASMA_UNIMP_2 | AVG_ASMA_ADD_2 |
|-----|------------|-----------|-----------|--------------------|-------------------|-----------------|---------------|---------------|
| 2021 | DEC | 12       | Belgium         | [count]            | [sum]                | [sum]                | [mean] |[mean]|

<br></br>
**Table view 3: No spatial grouping (Europe wide):**
 
| YEAR | MONTH_MON | MONTH_NUM | FLT_ASMA_UNIMP_2 | TIME_ASMA_UNIMP_2 | TIME_ASMA_ADD_2 | AVG_ASMA_UNIMP_2 | AVG_ASMA_ADD_2 |
|-----|------------|-----------|--------------------|-------------------|-----------------|---------------|---------------|
| 2021 | DEC | 12           | [count]            | [sum]                | [sum]                | [mean] |[mean]|""",unsafe_allow_html=True)
    st.markdown("""<br></br>
#### Temporal grouping: By year""",unsafe_allow_html=True)
    col6,col7,col8 = st.columns((1,1,1))
    col6.markdown("""**View 4: Grouped by airport**""")
    query4="""
SELECT 
  f.arrival_year, 
  a.icao, 
  a.name, 
  s.name, 
  a.asma_radius, 
  COUNT(f.id), 
  SUM(ae.unimpeded_asma_time), 
  SUM(ae.additional_asma_time),
  SUM(ae.unimpeded_asma_time)/COUNT(f.id),
  SUM(ae.additional_asma_time)/COUNT(f.id)
FROM 
  (SELECT 
      date_part('year', flight.arrival_date) as arrival_year, 
      flight.*
  FROM flight) AS f 
  JOIN asma_entry AS ae ON f.asma_entry_id = ae.id 
  JOIN airport AS a ON f.arrival_airport_id = a.id 
  JOIN state AS s ON a.state_id = s.id 
WHERE 
  a.pru_asma_monitoring = TRUE 
GROUP BY
  f.arrival_year, 
  a.icao, 
  a.name, 
  s.name, 
  a.asma_radius 
ORDER BY 
  f.arrival_year ASC, 
  s.name ASC, 
  a.name ASC;
"""
    col6.code(query4,language='sql')
    col7.markdown("""**View 5: Grouped by state**""")
    query5="""
SELECT 
  f.arrival_year, 
  s.name, 
  COUNT(f.id), 
  SUM(ae.unimpeded_asma_time), 
  SUM(ae.additional_asma_time),
  SUM(ae.unimpeded_asma_time)/COUNT(f.id),
  SUM(ae.additional_asma_time)/COUNT(f.id)
FROM 
  (SELECT 
      date_part('year', flight.arrival_date) as arrival_year, 
      flight.*
  FROM flight) AS f 
  JOIN asma_entry AS ae ON f.asma_entry_id = ae.id 
  JOIN airport AS a ON f.arrival_airport_id = a.id 
  JOIN state AS s ON a.state_id = s.id 
WHERE 
  a.pru_asma_monitoring = TRUE 
GROUP BY
  f.arrival_year, 
  s.name
ORDER BY 
  f.arrival_year ASC, 
  s.name ASC
"""
    col7.code(query5,language='sql')
    col8.markdown("""**View 6: No spatial grouping (Europe wide)**""")
    query6="""
SELECT 
  f.arrival_year, 
  COUNT(f.id), 
  SUM(ae.unimpeded_asma_time), 
  SUM(ae.additional_asma_time),
  SUM(ae.unimpeded_asma_time)/COUNT(f.id),
  SUM(ae.additional_asma_time)/COUNT(f.id)
FROM 
  (SELECT 
      date_part('year', flight.arrival_date) as arrival_year, 
      flight.*
  FROM flight) AS f 
  JOIN asma_entry AS ae ON f.asma_entry_id = ae.id 
  JOIN airport AS a ON f.arrival_airport_id = a.id 
WHERE 
  a.pru_asma_monitoring = TRUE 
GROUP BY
  f.arrival_year 
ORDER BY 
  f.arrival_year ASC
"""
    col8.code(query6,language='sql')

    st.markdown("""
    <br></br>
**Table view 4: Grouped by airport:**
 
| YEAR | APT_ICAO | APT_NAME | STATE_NAME | ASMA_RADIUS | FLT_ASMA_UNIMP_2 | TIME_ASMA_UNIMP_2 | TIME_ASMA_ADD_2 | AVG_ASMA_UNIMP_2 | AVG_ASMA_ADD_2 |
|-----|----------|----------|-----------|-----------|--------------------|-------------------|-----------------|---------------|---------------|
| 2021 | EBBR     | Brussels  | Belgium     | 40          | [count]                 | [sum]                | [sum]                | [mean] |[mean]| 

<br></br>
**Table view 5: Grouped by state:**
 
| YEAR | STATE_NAME | FLT_ASMA_UNIMP_2 | TIME_ASMA_UNIMP_2 | TIME_ASMA_ADD_2 | AVG_ASMA_UNIMP_2 | AVG_ASMA_ADD_2 |
|-----|-----------|--------------------|-------------------|-----------------|---------------|---------------|
| 2021 | Belgium         | [count]            | [sum]                | [sum]                | [mean] |[mean]|

<br></br>
**Table view 6: No spatial grouping (Europe wide):**
 
| YEAR |  FLT_ASMA_UNIMP_2 | TIME_ASMA_UNIMP_2 | TIME_ASMA_ADD_2 | AVG_ASMA_UNIMP_2 | AVG_ASMA_ADD_2 |
|-----|--------------------|-------------------|-----------------|---------------|---------------|
| 2021 | [count]            | [sum]                | [sum]                | [mean] |[mean]|""",unsafe_allow_html=True)

    st.markdown("""<br></br>
#### Creating views
To create a view, you can wrap the above queries using the `CREATE VIEW` statement in e.g., PostgreSQL. 
""",unsafe_allow_html=True)
    create_view = """
    CREATE VIEW view_name AS
    [QUERY];
"""
    st.code(create_view,language='sql')
    st.markdown("""<br></br>
#### Additional ideas
* Add a temporal grouping by day to the above. 
* Create views for specific years (e.g. group by month on state or airport where year = 2021)
* Create views with metrics for specific requested airports or states.
* ...  
""",unsafe_allow_html=True)