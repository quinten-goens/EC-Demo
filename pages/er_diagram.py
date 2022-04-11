import streamlit as st
import lorem

def app():

    # Use the full page instead of a narrow central column
    st.markdown("<h1 style='text-align: left; color: black;'>Entity Relationship Diagram</h1>", unsafe_allow_html=True)
    st.markdown("""
### Question one
Using the ASMA additional time dataset from the AIU Portal define an Entity-Relationship that best represents the underlying data tables assuming that you have information on a per flight basis.
Please consider that some/all airports from a state may be present or may be removed from the dataset over time due to changes of the monitored set. Please provide a rationale for your design choices.""")
    st.markdown("""
### ASMA time data modelling requirements""")
    col1,col2 = st.columns(2)
    col1.markdown("""
In this section an overview of the explicit data modelling requirements is given.
* The assumption made provides us with the information on a per flight basis. A single flight likely has the following properties:
    * A unique numeric identifier (for reference)
    * A flight number (e.g., BA1234)
    * A departure airport
    * A destination airport
    * A date of flight (i.e. the arrival date, the departure date can be derived)
    * A departure time (e.g., off-blocks time)
    * An arrival time (e.g., on-blocks time)
    * An ASMA entry (i.e. the flight will be entering an ASMA upon reaching the destination airport)
* Flights will enter the Arrival Sequencing and Metering Area (ASMA) upon arrival at the destination. These events will be called ASMA entries throughout the remainder of the proposed solution. An ASMA entry has the following properties:
    * A unique numeric identifier (for reference)
    * ASMA entry time
    * Unimpeded ASMA time
    * Additional ASMA time
* The flights have a departure airport and land at a destination airport. An airport has the following properties:
    * A unique numeric identifier (for reference)
    * An airport name
    * An airport ICAO code
    * An ASMA radius
    * An ASMA PRU monitoring flag (boolean) 
        * Note: If the ASMA time is being monitored for this specific airport by the Performance Review Unit (PRU) then the boolean will be set to True. If not then the boolean will be set to False.  
    * A state in which they are located.""")
    col2.image('resources/flight_phase.png',caption='Outbound and Inbound Traffic Queues from a Flight Phase Perspective (Source: EUROCONTROL (PRU))',use_column_width=True)
    
    st.markdown("""
### Entity Relationship Diagram
The following Entity Relationship diagram represents the underlying data tables assuming that you have information on a per flight basis.
    """)
    st.image('resources/ER-Diagramdrawio.png',caption='Entity Relationship Diagram',use_column_width=False)
    st.markdown("""
### Design choice motivations
Three entities are defined (IFR Flight, Airport, ASMA Entry) as they represent the underlying code concepts. The attributes are allocated to the entities based on the data modelling requirements.

There are four destinct relationships: 
* **IFR Flight - ASMA Entry: Has**
    * Cardinality: 1:1 
        * Each flight has exactly one ASMA entry and each ASMA entry belongs to exactly one flight. 
    * Participation: Full participation on both sides
        * Each IFR flight must have an ASMA entry and each ASMA entry must have an IFR flight.
* **IFR Flight - Airport: Departs at**
    * Cardinality: N:1
        * Each IFR flight can depart from only one airport but each airport can be departed from by multiple IFR flights.
    * Participation: Full participation on IFR flight side, partial participation on airport side.
        * Each IFR flight must have a departure airport but not each airport must have a departure flight.
* **IFR Flight - Airport: Arrives at**
    * Cardinality: N:1
        * Each IFR flight can arrive only at one airport but each airport can be arrived to by multiple IFR flights.
    * Participation: Full participation on IFR flight side, partial participation on airport side.
        * Each IFR flight must have an arrival airport but not each airport must have an arriving flight.
* **Airport - State: Located in**
    * Cardinality: N:1
        * Each airport can be located in only one state but each state can have multiple airports.
    * Participation: Full participation on airport side, partial participation on state side.
        * Each airport must have a state but not each state must have an airport.

### Additional comments:
* If it is so that airport_icoa is fully unique for each airport in Europe then this can be used as the primary key for the Airport entity.
* It is noted that the relationship "Departs at" is not in full participation at the side of the airport. This is so because when setting up the table for the (limited amount of) airports one only needs to import them all and they do not have to be used in a relationship.
* The boolean pru_asma_monitoring will allow to filter the database down to an ASMA time dataset which only contains the airports monitored by the Performance Review Unit (PRU).""")

#with st.expander('Table view ER Diagram'):
    #st.markdown("""For query designing purposes.""")
    #st.image("resources/tableview.drawio.png",caption='Table view ER Diagram',#=False)