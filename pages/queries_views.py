import streamlit as st
import lorem

def app():

    # Use the full page instead of a narrow central column
    st.markdown("<h1 style='text-align: left; color: black;'>Queries and Views</h1>", unsafe_allow_html=True)
    st.markdown("""
### Question Two
Given the ER diagram from Question 1:
* Define some example views to ease queries by an operational analysts and sketch them out.
* Write a query to extract the data as in the DATA sheet in the original dataset.""")
    st.markdown("""### Views""")
    st.markdown("""### Query
The various tables or relations are named flight, asma_entry, airport and state in the ER diagram, here we display a single row for each of these on the left hand side. The requested query to obtain the data as provided in the DATA sheet of the XLSX file can be found on the right hand side. It is written and tested with PostgreSQL.
    """)
    col1,col2 = st.columns((3,2))
    col1.markdown("""
**Tables with example row:**

**flight**

| id | flight_nr | departure_date | arrival_time | arrival_airport_id | departure_airport_id | asma_entry_id |
|----|---------------|----------------|--------------|--------------------|----------------------|---------------|
| 1  | AB1234        | 2021-12-31     | 12:20:22     | 2                  | 1                    | 1             |

<br/><br/>
**airport**
| id | name     | icoa | asma_radius | pru_asma_monitoring | state_id |
|----|----------|------|-------------|---------------------|----------|
| 1  | Brussels | EBBR | 40          | TRUE                | 1        |

<br/><br/>
**state**
| id | name |
|----|------|
| 1  | Belgium |

<br/><br/>
**asma_entry**
| id | asma_entry_time | unimpeded_asma_time | additional_asma_time |
|----|-----------------|-----------------------|---------------------|
| 1  | 12:08:46 | 12.1 | 0.5                   |

    """,unsafe_allow_html=True)
    query = """
SELECT 
  date_part('year', f.departure_date), 
  date_part('month', f.departure_date), 
  to_char(f.departure_date, 'MON'), 
  a.icao, 
  a.name, 
  s.name, 
  a.asma_radius, 
  COUNT(f.id), 
  SUM(ae.unimpeded_asma_time), 
  SUM(ae.additional_asma_time) 
FROM 
  flight as f 
  JOIN asma_entry AS ae ON f.asma_entry_id = ae.id 
  JOIN airport AS a ON f.arrival_airport_id = a.id 
  JOIN state as s ON a.state_id = s.id 
WHERE 
  a.pru_asma_monitoring = TRUE 
GROUP BY 
  date_part('year', f.departure_date), 
  date_part('month', f.departure_date), 
  to_char(f.departure_date, 'MON'), 
  a.icao, 
  a.name, 
  s.name, 
  a.asma_radius 
ORDER BY 
  date_part('year', f.departure_date) ASC, 
  date_part('month', f.departure_date) ASC, 
  s.name ASC, 
  a.name ASC;
    """
    col2.markdown("""**Requested query (in PostgreSQL):**""")
    col2.code(query,language='sql')