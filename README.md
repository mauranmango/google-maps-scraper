# Google Maps Scraper


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the libraries below to successfully  run the scraper.

```bash
pip install selenium
pip install bs4
pip install pandas
pip install lxml
```

## Usage
Change the path of the chromedriver.exe
```python
driver = webdriver.Chrome("..\\chromedriver.exe", options=options)  # FIXME locate chromedriver
```

Change the URL of the business

```python
if __name__ == "__main__":
    scraper = GoogleMapsScraper()
    url = "https://www.google.com/maps/place/Aspria+Berlin+Ku%E2%80%99damm/@52.5003887,13.2941771,17z/data=!4m20!1m11!3m10!1s0x47a850c4b634ef93:0x2faf0f02eacd864e!2sAspria+Berlin+Ku%E2%80%99damm!5m2!4m1!1i2!8m2!3d52.5003887!4d13.2941771!9m1!1b1!3m7!1s0x47a850c4b634ef93:0x2faf0f02eacd864e!5m2!4m1!1i2!8m2!3d52.5003887!4d13.2941771"  # TODO change to the url you want
    driver = scraper.create_driver()
```

## Notes


