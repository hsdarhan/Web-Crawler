import requests
import csv
import os
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://coinmarketcap.com/all/views/all'
COIN_COUNT=12
folder_name="coin_info"

class crawler:

  def create_folder(nameFolder):
    os.mkdir(nameFolder)

  def folder_exists(nameFolder):
    return os.path.exists(nameFolder)

  def create_file_name():
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
    var1 = folder_name+'/coin-data ' + dt_string + '.csv'
    return var1

  def get_info(fileName):

    source_code = requests.get(url)
    plain=source_code.text
    soup = BeautifulSoup(plain, 'html.parser')
    x = 0
    file = open(fileName, 'w', newline='', encoding='utf8')
    writer = csv.writer(file)
    writer.writerow(['Rank','Name','Symbol', 'Market Cap', 'Price', 'Supply', 'Volume', '1 Hr Change', '24 Hr Change', '7 Day Change'])

    table=soup.find('tbody')

    for tr in table.find_all('tr'):
      nameHolder=tr.find('a', {'class': 'currency-name-container link-secondary'}).text.strip()
      symbolHolder=tr.find('td', {'class': 'text-left col-symbol'}).text.strip()
      marketCapHolder=tr.find('td', class_='no-wrap market-cap text-right').get('data-sort')
      supplyHolder = tr.find('td', class_='no-wrap text-right circulating-supply').get('data-sort')
      priceHolder = tr.find('a', {'class': 'price'}).text.strip()
      volumeHolder=tr.find('a', {'class': 'volume'}).text.strip()
      try:
        twenty_four_hr_change= tr.find('td', {'data-timespan': '24h'}).text.strip()
      except:
        twenty_four_hr_change= "None"
      try:
        one_hr_change= tr.find('td', {'data-timespan': '1h'}).text.strip()
      except:
        one_hr_change= "None"
      try:
        seven_day_change= tr.find('td', {'data-timespan': '7d'}).text.strip()
      except:
        seven_day_change= "None"

      x+=1
      print(x,"   ",nameHolder,symbolHolder,marketCapHolder,priceHolder,supplyHolder,volumeHolder, twenty_four_hr_change)
      writer.writerow([x, nameHolder, symbolHolder,marketCapHolder,priceHolder,supplyHolder,volumeHolder, one_hr_change, twenty_four_hr_change,seven_day_change])
      if x==COIN_COUNT:
        file.close()
        break

  def run():

    if(not crawler.folder_exists(folder_name)):
      crawler.create_folder(folder_name)
    crawler.get_info(crawler.create_file_name())
    print ('Data Export Successful!')

if __name__ == "__main__":
  crawler.run();




