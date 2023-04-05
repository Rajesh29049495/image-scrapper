import os
import time
import requests                         ##to get requests from a particular URL
from selenium import webdriver          ##selenium with python is used to carry out automated test cases for browsers or web applications. You can easily use it to simulate tests such as tapping on a button, entering content to the structures, skimming the entire site, etc.
                                        ##webdriver class of selenium will be used to hit the web browser using that web browser specific web driver, like to hit google chrome we will use the cromedriver that we have installed earlier{that we have placed out in the current working directory}

def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 2):       ##provided input variables with datatyping,,,,,,,and "wd" is an instance of webdriver class{using datatyping this could be done}
    ##function that will be called later to scroll the web page from top to the end{jha tak ki scroll kia ja sakta hai i.e., jab tak li load more button na aa jae }
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")      ###execute_script method of wendriver is used to run a javascript code on the current web page. The javascript code is "window.scrollTo(0,document.body.scrollHeight)" which scrolls to the bottom of the page. The execute_script method can also return a value from the javascript code if it has a return statement.... it was used in a python script because the script was using webdriver to automate some web browsing tasks. Sometimes, it is easier or necessary to use JavaScript code to perform some actions on a web page that webdriver cannot do by itself. For example, scrolling to a specific element or clicking a hidden button. In those cases, execute_script can be useful to run JavaScript code from Python.
        time.sleep(sleep_between_interactions)

        # build the google query

    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"    ###this is a common url that will search for images of 'q'{the placeholder for the search query/ search term,,,,,,,,,basically whatever serach result on google chrome for any king images, the url will be same except the q term will be the serach term whose images haev been searched}

    # load the page
    wd.get(search_url.format(q=query))      ##it is the same format that is used with a string to format the placeholder in the string, so here using format we foramtted the "q" placeholder and assigned it "query" varable, which will be the search term that will be used in the search url to get images w.r.t. the search term
                                            ##the above code will load the very first page, once its done, the below mentioned will be created
    image_urls = set()                      ##this variable will hold on to distinct urls{as variabel is of type set} of the images
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")  ##"find_elements_by_css_selector()" method, which is a part of Selenium Python, a web automation framework. This method returns a list of elements that match a given CSS selector. A CSS selector is an attribute which is used as a locator for finding elements on a web page based on their style properties, in this line, css selector is "img.Q4LuWd" which means it will look for all image tag {<img>} elements w.r.t. thumbnails of the images{which we found by hovering over the thumbnials uisng inspect feature of the browser}that has a jsname as "Q4LuWd" {this can be seen by using the "inspect" feature of the webpage, and note it is same for all the images's thumbnails on google chrome}. the variable "thumnail_results" will store the list of all the elements w.r.t. thumbnails of the images found w.r.t. the search term
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]:
            #iterate over every thumnail element found one by one
            try:
                img.click()                                                       ##clicking on one of the thumnail will open a bigger version of it on teh right side, which we will locate using webdriver uisng css_selector as locator and for that we will use common class name{which we get by hovering over the image } in case of google chrome for this version of image {that opens on teh right side}
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):     ##{a line of code uisng selenium mpython}, it checks if an element "actual_image" has an attribute called "src" and if that attribute contains the string "http". if both conditions are true, then code will execute the next statement
                    image_urls.add(actual_image.get_attribute('src'))                                     ##this will add  the "src" attribute of the "actual_iamge" element, which is basically a url of the image

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:                                                                                             ##if the length of image_urls set is greater than the max_links_to_fetch then the for loop will break and else statement also will not run and simply as the condition of while loop{the outer loop} is no more true, the while loop will also end and teh function fetch_image_urls will return the image_urls set. BUT if the length of image_urls is still less than max_links_to_fetch then and the whole for loop is exhausted whiout any break then the else statement will run{which basically will find the element using css_selector ".mye4qd", which is genrally used for an element, which is a button to load more, if the load more button's element found then using webdriver will execute a script which perform a function of clicking on the button}, then the code floe will check the while loop condition which is obviously still True, then whole while loop willl run again but this time on the extended web page which would have opened after clicking on teh load more button
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)
            return
            load_more_button = wd.find_elements_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")
            else:
                print("Could not find 'Load More' button")
    return image_urls


def persist_image(folder_path:str,url:str, counter):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images=10):     ##hardcoded the folder "images", that will be made in the current working directory, when the search and download operation will be done, and images will b e stored inisde thi sfolder inside location that will be created in this function,,,,,,,,,,,and "number_images" parameter will tell how many images to be downloaded, by default we have set it as 10, which we can change during the call, i.e., when the function will be called
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))                    ##this will form a path of sub folder in "images" folder, an dthat sub folder will formed using the search term {by lowering it then splitting on the basis of space then joining them with "_"}

    if not os.path.exists(target_folder):                                                                  ##this create the target folder, basically all that "images" folder and that sub folder inside it
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:                                              ##this webdriver.chrome() is a class that allows you to use google.chrome as a web browser for your python scripts. You can use it with the with statement to automatically close the browser after performing some actions,,,,,,,,,,otherwise using webdriver.chrome will start the chrome, using chromedriver like "driver = webdriver.Chrome('/path/to/chromedriver')", then perform certain actions like "driver.get('http://www.google.com/')" etc etc  then closing the initiated driver using "driver.quit()"
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)          ##calling "fetch_image_urls" function, ,, "wd" is the chromedriver that was initiated using erbdriver.chrome(),,,,,,"sleep_between_interactions=0.5" provode 0.5 sec of gap in between th esearch, so that the system does not crashes/hang

    counter = 0
    for elem in res:
        persist_image(target_folder, elem, counter)
        counter += 1


# How to execute this code
# Step 1 : pip install selenium, pillow, requests
# Step 2 : make sure you have chrome installed on your machine
# Step 3 : Check your chrome version ( go to three dot then help then about google chrome )
# Step 4 : Download the same chrome driver from here  " https://chromedriver.storage.googleapis.com/index.html "
# Step 5 : put it inside the same folder of this code


DRIVER_PATH = r'chromedriver.exe'       ##mentioned the path of the chrome driver{just mentioned the name because it is present in my current working directry}
search_term = 'car'
# num of images you can pass it from here  by default it's 10 if you are not passing
#number_images = 50
search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_images=10)