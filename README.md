# DigiKala-Scraper
This is Scraper For Digikala with Selenium and Bs4 for Scrap and SqlArhemy for save data in database

# Installation
- clone the project
```
git clone https://github.com/Cmatrix1/DigiKala-Scraper
```

- install selenium
```
pip install selenium
```
- install bs4 
```
pip install bs4
```
- install sqlalchemy
```
pip install SQLAlchemy
```
- run the project
```
python DigiKala-Scraper.py
```

# Usage

- after run the project Enter Your Url Here
```bash
Enter The List Of Product Like This Link:
[https://www.digikala.com/search/category-notebook-netbook-ultrabook/]
Link: https://www.digikala.com/search/category-men-clothing/
```
- and Press Enter

# Configuration

- Enter Your DataBase Name in line 9 in File DataBase.html
```python
engine = create_engine('sqlite:///digikala.db', echo=True)
```
- Enter Your Table DataBase Name in line 15 in File DataBase.html
```python
__tablename__ = 'Digikala'
```