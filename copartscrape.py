import time

# Scrape the data for a Copart search accounting for the paginated datatable.
def scrape(driver):
        driver.get("https://www.copart.com/lotSearchResults/?free=true&query=&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22FETI%22:%5B%22lot_features_code:LOTFEATURE_0%22%5D,%22LOC%22:%5B%22yard_name:%5C%22NC%20-%20CHINA%20GROVE%5C%22%22,%22yard_name:%5C%22NC%20-%20LUMBERTON%5C%22%22,%22yard_name:%5C%22NC%20-%20MOCKSVILLE%5C%22%22,%22yard_name:%5C%22NC%20-%20RALEIGH%5C%22%22%5D,%22NLTS%22:%5B%22expected_sale_assigned_ts_utc:%5BNOW%2FDAY-7DAY%20TO%20NOW%2FDAY%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5C%221999%5C%22%22,%22lot_year:%5C%222000%5C%22%22,%22lot_year:%5C%221998%5C%22%22,%22lot_year:%5C%221997%5C%22%22,%22lot_year:%5C%222001%5C%22%22%5D%7D,%22sort%22:%5B%22auction_date_type%20desc%22,%22auction_date_utc%20asc%22%5D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:false%7D")
        driver.implicitly_wait(10)

        print(driver.find_element_by_css_selector('#serverSideDataTable_info').text)

        copartData = []
        
        # Get the intial pages data.
        copartRecords = getTableData(driver, False)
        copartData.extend(copartRecords)

        # Loop by clicking the Next button on the datatable. Loop will break when the page has gathered
        # data on last page and Next button is disabled. There is also a 1000 page limit to prevent an endless loop.
        i = 0
        while i < 1000:
            driver.find_element_by_css_selector('#serverSideDataTable_next a').click()
            time.sleep(2)
            try:
                print(driver.find_element_by_css_selector('#serverSideDataTable_info').text)
                copartRecords = getTableData(driver, False)
                copartData.extend(copartRecords)
                nextBtnClasses = driver.find_element_by_css_selector('#serverSideDataTable_next').get_attribute("class")
                if "disabled" in nextBtnClasses:
                    print("Reached end of data")
                    break
            except:
                print('Page not loading after Next click!')

            i += 1
            if (i == 1000):
                print('Ending loop since 1000 page limit was reached!')
        
        # Print the output to validate the data TODO next step, store data in db
        for cr in copartData:
            print('Make ' + cr.make)

# Loop through data table on screen to return a list of Copart Records.
def getTableData(driver, printData):
    copartRecords = []

    mytable = driver.find_element_by_css_selector('table#serverSideDataTable')
    skipFirstRow = True
    for row in mytable.find_elements_by_css_selector('tr'):
        if skipFirstRow:
            skipFirstRow = False
            continue
        column = 0
        # Store the data in a Copart Record object
        copartRecord = CopartRecord()
        # Must loop through all cells in row since list[index] notation does not work.
        for cell in row.find_elements_by_tag_name('td'):
            if (column == 2):
                copartRecord.id = cell.text.replace('\n', '').replace('\r', '').replace('Watch', '')
            elif (column == 3):
                copartRecord.year = cell.text
            elif (column == 4):
                copartRecord.make = cell.text
            elif (column == 5):
                copartRecord.model = cell.text
            elif (column == 7):
                copartRecord.location = cell.text.replace('\n', ' ').replace('\r', '')
            elif (column == 8):
                copartRecord.saledate = cell.text.replace('\n', ' ').replace('\r', '')
            elif (column == 9):
                copartRecord.odometer = cell.text

            column+=1
        copartRecords.append(copartRecord)
        if(printData):
            print("id " + copartRecord.id)
            print("year " + copartRecord.year)
            print("make " + copartRecord.make)
            print("model " + copartRecord.model)
            print("location " + copartRecord.location)
            print("saledate " + copartRecord.saledate)
            print("odometer " + copartRecord.odometer)
    
    return copartRecords

# Object defining a Copart Record
class CopartRecord: 
    id = ''
    year = ''
    make = ''
    model = ''
    location = ''
    saledate = ''
    odometer = ''