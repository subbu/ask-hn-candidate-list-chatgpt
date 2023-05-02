import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url = "https://news.ycombinator.com/item?id=35773705"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)
driver.get(url)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

comments = soup.find_all("td", class_="default")
result = []

for comment in comments:
    comment_section = comment.find("div", class_="comment")

    if comment_section:
        data = comment_section.find_all("p")
        data_dict = {}

        for line in data:
            line_text = line.get_text().strip()
            if line_text.startswith("Location:"):
                data_dict["Location"] = line_text.split("Location:")[1].strip()
            elif line_text.startswith("Remote:"):
                data_dict["Remote"] = line_text.split("Remote:")[1].strip()
            elif line_text.startswith("Willing to relocate:"):
                data_dict["Willing to relocate"] = line_text.split("Willing to relocate:")[1].strip()
            elif line_text.startswith("Technologies:"):
                data_dict["Technologies"] = line_text.split("Technologies:")[1].strip()
            elif line_text.startswith("Résumé/CV:"):
                resume_link = line.find("a")
                if resume_link:
                    data_dict["Résumé/CV"] = resume_link["href"].strip()
                else:
                    data_dict["Résumé/CV"] = line_text.split("Résumé/CV:")[1].strip()
            elif line_text.startswith("Email:"):
                data_dict["Email"] = line_text.split("Email:")[1].strip()

        result.append(data_dict)

output = json.dumps(result, indent=2)
print(output)

