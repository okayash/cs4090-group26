# CS4090 - Group 26: CLIO

Team Members: Ashley Fong (Developer), Abigail Fletcher (Team Lead), Reagan Randolph (Documentation Lead)

Project Description: Clio is a museum and attractions recommender that provides a user with new locations based on their selected interests and demographics.


To run in MacOS:

``python3 -m venv .venv``

``source .venv/bin/activate``

``pip install -r requirements.txt``

``streamlit run backend/src/clio/app.py``


mysql -u root -p clio < backend/db/schema/tables.sql;