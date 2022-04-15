import streamlit as st
import lorem

def app():

    # Use the full page instead of a narrow central column
    st.markdown("<h1 style='text-align: left; color: black;'>Entity Relationship Diagram</h1>", unsafe_allow_html=True)
    st.markdown("""
### Question one
Using the ASMA additional time dataset from the [AIU Portal](https://ansperformance.eu/) define an Entity-Relationship that best represents the underlying data tables assuming that you have information on a per flight basis.
Please consider that some/all airports from a state may be present or may be removed from the dataset over time due to changes of the monitored set. Please provide a rationale for your design choices.""")
    st.markdown("""
### Data modelling requirements""")
    col1,col2 = st.columns(2)
    col1.markdown("""
In this section an overview of the explicit data modelling requirements is specified.
* The assumption made provides us with the **information on a per flight basis**. A single flight likely has the following properties:
    * A unique numeric identifier (for reference)
    * A flight number (e.g., BA1234)
    * A departure airport
    * A destination or arrival airport
    * A date of flight (i.e. the arrival date, the departure date can be derived)
    * A departure time (e.g., off-blocks time)
    * An arrival time (e.g., on-blocks time)
    * An ASMA entry (i.e. the flight will be entering the ASMA upon reaching the destination airport)
* Flights will enter the **Arrival Sequencing and Metering Area (ASMA)** upon arrival at the destination. These events will be called **ASMA entries** throughout the remainder of the proposed solution. An ASMA entry has the following properties:
    * A unique numeric identifier (for reference)
    * ASMA entry time
    * Additional ASMA time
* The flights depart at a **departure airport** and arrive at a **destination/arrival airport**. An **airport** has the following properties:
    * A unique numeric identifier (for reference)
    * An airport name
    * An airport ICAO code
    * Unimpeded ASMA time
    * An ASMA radius
    * An ASMA PRU monitoring flag (boolean) 
        * Note: If the ASMA time is being monitored for this specific airport by the Performance Review Unit (PRU) then the boolean will be set to `True`. If not then the boolean will be set to `False`.  
        * **Disclaimer:** This solution is for demonstration purposes only as this is a simplification of the actual situation. The database ideally captures time periods in which the respective airport is observed by the PRU. The current solution relies on someone actively updating the database when a specific airport is observed or not observed.
* The airports are located in a **state** (i.e., a country). A **state** has the following properties:
    * A unique numeric identifier (for reference)
    * A state name""")
    col2.image('resources/flight_phase.png',caption='Outbound and Inbound Traffic Queues from a Flight Phase Perspective (Source: EUROCONTROL (PRU))',use_column_width=True)
    
    st.markdown("""
### Entity-relationship diagram
The following entity-relationship (ER) diagram represents the underlying data tables assuming that you have information on a per flight basis.
    """)
    st.image('resources/ER-Diagramdrawio.png',caption='Entity Relationship Diagram',use_column_width=False)
    st.markdown("""
### Design choice motivations
**Four entities are defined** (`IFR Flight`, `Airport`, `ASMA Entry`, `State`) as they represent the underlying core concepts. The attributes are allocated to the entities based on the data modelling requirements. Note that `State` (more specifically the name of the state) could have been an attribute of `Airport`. However, it is more correct to add it as a seperate entity as one wants to normalize the data according to the normal forms when proceeding with data modelling.
""")

    with st.expander("About normal forms"):
        st.markdown("""
To normalize the data, the following normal forms are achieved:
* First Normal Form (1NF)
    * Atomic values: each cell contains unique and single values
    * Be able to add data without altering tables
    * Separate different relations into different tables
    * Keep relationships between tables together with foreign keys
* Second Normal Form (2NF)
    * Have reached 1NF
    * All columns in the table must rely on the Primary Key
* Third Normal Form (3NF)
    * Have reached 2NF
    * No transitive dependencies (you have transitive dependencies if to get from A-> C, you need to go through B)

In our example, the state is not directly related to the primary key of the airport table. It is related to the airport and thus is a transitive dependency. Therefore we made it its' own entity to achieve 3NF.""") 

    st.markdown("""
**There are four destinct relationships:** 
* **IFR Flight - ASMA Entry: `Has`**
    * Cardinality: 1:1 
        * Each flight has exactly one ASMA entry and each ASMA entry belongs to exactly one flight. 
    * Participation: Full participation on both sides
        * Each IFR flight must have an ASMA entry and each ASMA entry must be linked to an IFR flight.
* **IFR Flight - Airport: `Departs at`**
    * Cardinality: N:1
        * Each IFR flight can depart from only one airport but each airport can be departed from by multiple IFR flights.
    * Participation: Full participation on IFR flight side, partial participation on airport side.
        * Each IFR flight must have a departure airport but not each airport must have a departure flight.
* **IFR Flight - Airport: `Arrives at`**
    * Cardinality: N:1
        * Each IFR flight can arrive only at one airport but each airport can be arrived to by multiple IFR flights.
    * Participation: Full participation on IFR flight side, partial participation on airport side.
        * Each IFR flight must have an arrival airport but not each airport must have an arriving flight.
* **Airport - State: `Located in`**
    * Cardinality: N:1
        * Each airport can be located in only one state but each state can have multiple airports.
    * Participation: Full participation on airport side, partial participation on state side.
        * Each airport must have a state but not each state must have an airport.

### Additional comments:
* If it is so that the attribute `airport_icoa` is fully unique for each airport in Europe then this can be used as the primary key for the `Airport` entity.
* It is noted that the relationship `Departs at` is not in full participation at the side of the `Airport` entity. This is so because when setting up the table for the (limited amount of) airports one can import them all and they do not have to be used in a relationship.
* The boolean attribute `pru_asma_monitoring` of the `Airport` entity will allow to filter the database down to the provided ASMA time dataset. This dataset only contains the airports monitored by the Performance Review Unit (PRU).""")