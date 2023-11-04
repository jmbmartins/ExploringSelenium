import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

os.environ['PATH'] += r"C:\SeleniumDrivers"
driver = webdriver.Chrome()

driver.get('http://localhost:8080/')


# Test 1: Make a reservation for a Pet
def make_reservation():
    try:
        # Login
        driver.get('http://localhost:8080/')

        email_input = driver.find_element(By.NAME, 'email')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.ID, 'btnSub')

        email_input.send_keys('user1@example.com')
        password_input.send_keys('password1')
        login_button.click()

        time.sleep(2)

        driver.implicitly_wait(10)

        # Home Page
        btnBooking = driver.find_element(By.ID, 'btnbooking')
        btnBooking.click()

        # Booking Page
        btnReserve = driver.find_element(By.CLASS_NAME, "reserve_link")
        btnReserve.click()

        # Locate the form elements and interact with them
        check_in_date = driver.find_element(By.CLASS_NAME, "checkInDate")
        check_out_date = driver.find_element(By.CLASS_NAME, "checkOutDate")

        # Clear any existing date values in the input fields
        check_in_date.clear()
        check_out_date.clear()

        # Values to insert
        checkInDate = "2023-11-19"
        checkOutDate = "2023-11-29"
        petName = "Thor"
        roomType = "standard"

        check_in_date.send_keys(datetime.strptime(checkInDate, "%Y-%m-%d").strftime("%d-%m-%Y"))
        check_out_date.send_keys(datetime.strptime(checkOutDate, "%Y-%m-%d").strftime("%d-%m-%Y"))

        pet_dropdown = Select(driver.find_element(By.ID, "petId"))
        pet_dropdown.select_by_index(1)  # Replace with the desired pet name "Thor"

        room_type_select = Select(driver.find_element(By.ID,"roomTypeSelect"))
        room_type_select.select_by_value(roomType)  # Replace with your desired room type

        time.sleep(10)

        # Submit the form
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        time.sleep(10)
        driver.implicitly_wait(1000)

        # Locate the table rows
        table_rows = driver.find_elements(By.TAG_NAME, "tr")

        # Flag to indicate whether the record is found
        record_found = False

        # Iterate through the rows and check for the specified values
        for row in table_rows:
            # Get the values from the table cells
            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) == 5:  # Assuming there are 5 cells in each row
                row_checkInDate = cells[0].text
                row_checkOutDate = cells[1].text
                row_roomType = cells[2].text
                row_petName = cells[4].text  # Assuming pet name is in the 5th cell

                if (
                        row_checkInDate == checkInDate
                        and row_checkOutDate == checkOutDate
                        and row_roomType == roomType
                        and row_petName == petName
                ):
                    record_found = True
                    break

        # Assert that the record is found
        if record_found:
            print("Test new lodging register succeeded.")
        else:
            print("Record not found in the table.")

    except Exception as e:
        print("Test new lodging register failed:", str(e))


def delete_reservation():
    pass


def checkIn_after_checkOut():
    pass


def checkIn_before_currentDate():
    pass


# Main test scenario
try:
    make_reservation()
    # delete_reservation()
    # checkIn_after_checkOut()
    # checkIn_before_currentDate()
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    driver.quit()  # Close the browser