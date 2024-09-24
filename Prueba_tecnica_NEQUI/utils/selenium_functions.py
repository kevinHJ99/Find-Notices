from Prueba_tecnica_NEQUI.utils.imports import *


class AutomationFunctions:

    @staticmethod
    def set_up_Edge(url, options):
        """
        Set up the WebDriver for Edge and open the specified URL.
        
        Args:
            url (str): The URL of the website to open.
            
        Returns:
            webdriver.Edge: The initialized WebDriver object.
        """
        driver = webdriver.Edge(options=options)
        # open the website
        driver.get(url)
        # maximize in the Chrome browser window 
        driver.maximize_window()
        
        return driver
        
        
    @staticmethod
    def set_up_Chrome(url, options):
        """
        Set up the WebDriver for Chrome and open the specified URL.
        
        Args:
            url (str): The URL of the website to open.
            
        Returns:
            webdriver.Chrome: The initialized WebDriver object.
        """
        # initialize the WebDriver of Chrome
        driver = webdriver.Chrome(options=options)
        # open the website
        driver.get(url)
        # maximize in the Chrome browser window 
        driver.maximize_window()
        
        return driver
        
        
    
    @staticmethod
    def do_clickByXpath(driver, xpath):
        """
        Perform a click action on an element found by XPath.
        
        Args:
            driver (webdriver.Chrome): The WebDriver object.
            xpath (str): The XPath expression to locate the element.
        """
        element = driver.find_element(By.XPATH, xpath)
        actions = ActionChains(driver)
        actions.move_to_element(element)
        WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, xpath))
        ).click()
            
    
    @staticmethod
    def do_clickByName(driver, name):
        """
        Perform a click action on an element found by name attribute.
        
        Args:
            driver (webdriver.Chrome): The WebDriver object.
            name (str): The value of the name attribute to locate the element.
        """
        element = driver.find_element(By.NAME, name)
        actions = ActionChains(driver)
        actions.move_to_element(element)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, name))
            ).click()
        except:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.NAME, name))
            ).click()

    
    @staticmethod
    def do_clickById(driver, id):
        """
        Perform a click action on an element found by id attribute.
        
        Args:
            driver (webdriver.Chrome): The WebDriver object.
            id (str): The value of the id attribute to locate the element.
        """
        element = driver.find_element(By.ID, id)
        actions = ActionChains(driver)
        actions.move_to_element(element)
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, id))
            ).click()
        
    

    @staticmethod
    def do_stringByXpath(driver, xpath, string):
        """
        Type a string into an input element found by XPath.
        
        Args:
            driver (webdriver.Chrome): The WebDriver object.
            xpath (str): The XPath expression to locate the input element.
            string (str): The string to type into the input element.
        """
        element = driver.find_element(By.XPATH, xpath)
        actions = ActionChains(driver)
        actions.move_to_element(element)
        try:
            input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            input.send_keys(string)
        except:
            input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            input.send_keys(string) 
    

    @staticmethod
    def do_stringByName(driver, name, string):
        """
        Type a string into an input element found by name attribute.
        
        Args:
            driver (webdriver.Chrome): The WebDriver object.
            name (str): The value of the name attribute to locate the input element.
            string (str): The string to type into the input element.
        """
        element = driver.find_element(By.NAME, name)
        actions = ActionChains(driver)
        actions.move_to_element(element)
        try:
            input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, name))
            )
            input.send_keys(string)
        except:
            input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.NAME, name))
            )
            input.send_keys(string)  
    

    @staticmethod
    def do_stringById(driver, id, string):
        """
        Type a string into an input element found by id attribute.
        
        Args:
            driver (webdriver.Chrome): The WebDriver object.
            id (str): The value of the id attribute to locate the input element.
            string (str): The string to type into the input element.
        """
        element = driver.find_element(By.ID, id)
        actions = ActionChains(driver)
        actions.move_to_element(element)
        try:
            input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, id))
            )
            input.send_keys(string)
        except:
            input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, id))
            )
            input.send_keys(string) 
            
    
    def do_login(driver, name, user, password):
        """
        Perform a login action by typing username and password.
        
        Args:
            driver (webdriver.Chrome): The WebDriver object.
            name (str): The value of the name attribute to locate the input elements.
            user (str): The username to type into the username input element.
            password (str): The password to type into the password input element.
        
        Returns:
            webdriver.Chrome: The WebDriver object after performing the login action.
        """
        user_name = AutomationFunctions.do_stringByName(driver, name, user)
        user_password = AutomationFunctions.do_stringByName(driver, name, password+Keys.ENTER)
    
        return driver
    
    
    def do_get_items(driver, xpath):
        """
        Get items based on XPath expression.
        
        Args:
            driver (webdriver.Chrome): The WebDriver object.
            xpath (str): The XPath expression to locate the items.
        """
        try:
            tag_item = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except:
            raise Exception("TimeoutError: Tag Item not found")
        
        return tag_item
    
    @staticmethod
    def do_get_response(url, headers):
        """
        Get the response of a HTTP request.
        
        Args:
            url (str): The URL to send the request.
        
        Returns:
            requests.Response: The response object.
        
        Raises:
            Exception: If the status code of the response is not 200.
        """
        response = rq.get(url, headers=headers)
        ## =============//=============
        if response.status_code == 200:
            return response.status_code, response
        else: 
            return reponse.status_code
            
    
    def do_get_dom_bs4(response):
        """
        Extracts DOM tree from HTML response using BeautifulSoup and etree.
    
        Args:
            response: Response object containing HTML content.
    
        Returns:
            DOM tree extracted from HTML.
        """
        # Parse HTML content with BeautifulSoup
        soup = bs(response.text, 'lxml')
        # Convert BeautifulSoup object to string and parse it with etree
        dom = etree.HTML(str(soup))
        
        return dom
        

    def do_get_dom_html(html):
        """
        Extracts DOM tree from HTML response using BeautifulSoup and etree.
    
        Args:
            response: Response object containing HTML content.
    
        Returns:
            DOM tree extracted from HTML.
        """
        # Parse HTML content with BeautifulSoup
        soup = bs(html, features="lxml")
        # Convert BeautifulSoup object to string and parse it with etree
        dom = etree.HTML(str(soup))
        
        return dom

    def do_get_dom_requests(response):
        """
        Extracts DOM tree from HTML response using BeautifulSoup and etree.
    
        Args:
            response: Response object containing HTML content.
    
        Returns:
            DOM tree extracted from HTML.
        """
        # get HTML content with requests
        html_content = response.content
        # parser content with lxml
        parser = etree.HTMLParser()
        dom = etree.fromstring(html_content, parser)
        
        return dom

    
    def get_cookies(driver):
        """
        Extracts cookies from Selenium WebDriver and creates a requests session.
    
        Args:
            driver: Selenium WebDriver instance.
    
        Returns:
            Session object with extracted cookies.
        """
        # Get cookies from WebDriver
        cookies = driver.get_cookies()
        # Create a requests session
        session = requests.Session()
        
        # Set cookies in the session
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
    
        return session
    
    def do_download_image(image_url):
        """
        Downloads an image from the specified URL.
    
        Args:
            image_url: URL of the image to download.
        """
        # Make a GET request to the image URL
        response = rq.urlopen(image_url)
        
        # Check if the request was successful (status code 200)
        if response.status == 200:
            # Save the image to a file
            with open('image.jpg', 'wb') as file:
                file.write(response.read())
            print("Image downloaded successfully.")
        else:
            print("Failed to download the image. Status code:", response.status)

    
    def do_download_pdf(pdf_url):         
        """
        Downloads a PDF file from the specified URL.
    
        Args:
            pdf_url: URL of the PDF to download.
        """
        # Make a GET request to the PDF URL
        response = requests.get(pdf_url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Save the PDF to a file
            with open('document.pdf', 'wb') as f:
                f.write(response.content)
            print("PDF downloaded successfully.")
        else:
            print("Failed to download the PDF. Status code:", response.status_code)

    
    def do_load_element(driver, path): 
        """
        Loads a file element on a webpage using Selenium WebDriver.
    
        Args:
            driver: Selenium WebDriver instance.
            path: Path to the file to upload.
        """
        # Path to the PDF file you want to upload
        pdf_file_path = path
        
        # Find the file input element on the webpage
        input_file_element = driver.find_element(By.XPATH, '//input[@type="file"]')
        
        # Send the PDF file path to the file input element
        input_file_element.send_keys(pdf_file_path)
        
        # Wait for a few seconds to allow the file upload to process
        time.sleep(5)

    
    def json_load(path):
        """
        Loads JSON data from a file.
    
        Args:
            path: Path to the JSON file.
    
        Returns:
            JSON data loaded from the file.
        """
        with open(path, 'r') as file:
            data = json.load(file)
        
        return data

    
    def install_libraries():
        """
        Installs Python libraries listed in requirements.txt file.
        """
        # Command to install requirements using pip
        pip_command = ['pip', 'install', '-r', 'requirements.txt']
        
        # Execute the command
        result = subprocess.run(pip_command, capture_output=True, text=True)
        
        # Check if the command was successful
        if result.returncode == 0:
            print("Requirements installation successful")
        else:
            print("Requirements installation failed:", result.stderr)

    
    def read_pdf(path):
        """
        Reads the text from a PDF file.
    
        Args:
            path: Path to the PDF file.
    
        Returns:
            Text extracted from the PDF.
        """
        # Path to the PDF file
        pdf_path = path
        
        # Open the PDF file
        with pp.open(pdf_path) as file_pdf:
            # Initialize an empty string to store the full text
            full_text = ""
            
            # Iterate over each page
            for page in file_pdf.pages:
                # Extract text from the current page
                page_text = page.extract_text()
                # Concatenate the text from the current page to the full text
                full_text += page_text
    
            return full_text