import re
from typing import List, Union, Dict
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def get_driver(driver='chrome'):
    option = Options()
    option.add_argument('--headless')

    if driver == 'chrome':
        try: driver = webdriver.Chrome(options=option)
        except Exception as e: print(f"Error happened when initializing a {driver} web driver:\n{e}")
    else: raise ValueError(f'The driver {driver} is not supported')
    
    return driver


def search_hf_hub_page_for_id_list(
        page: Union[int, tuple, list] = 1, 
        type: str = "model",
        driver: str = 'chrome',
        verbose: bool = False) -> List[str]:
    """Searches the Hugging Face {Model / Dataset} Hub list to get the id list at certain page with the index `page_idx`
    and return a webpage string list.
    """
    def search_single_page(page_idx):
        hub_page = f"https://huggingface.co/{type}s?p={page_idx-1}&sort=trending"
        model_ids = []
        
        try:
            driver.get(hub_page)
            model_list = driver.find_element(By.CSS_SELECTOR, "div.grid") # find the model hub
            model_id_refs = model_list.find_elements(By.CSS_SELECTOR, "article.overview-card-wrapper a.block.p-2")
            
            if verbose: print(f"Found {len(model_id_refs)} {type} ids at page {page_idx}")
            
            for model_id_ref in model_id_refs:
                model_ids.append(model_id_ref.get_attribute('href'))
                
        except Exception as e: 
            print(f"Error happened on page {page_idx}")
            if verbose: print(e)
        finally:
            return model_ids
        
    if isinstance(page, int):
        page_idxs = [page]
    elif isinstance(page, tuple) and len(page) == 2:
        page_idxs = list(range(page[0], page[1]+1))
    elif isinstance(page, tuple) or isinstance(page, list):
        page_idxs = page
    else: raise ValueError(f"Page {page} is not valid")

    driver = get_driver(driver)
    model_ids_all, failed_pages = [], []
    
    for page_idx in tqdm(page_idxs):
        model_ids = search_single_page(page_idx)
        if model_ids == []: failed_pages.append(page_idx)
        else: model_ids_all.extend(model_ids)
        
    driver.quit() # Close the WebDriver

    return model_ids_all, failed_pages


def search_hf_hub_repo_for_card(
        repo: Union[str, List[str]],
        type: str = "model",
        driver: str = 'chrome', 
        search_type: str = 'simple',
        verbose: bool = False,
    ) -> Dict[str,str]:
        
    def collect_text_from_element(element):
        texts = []
        for sub_elem in element.find_elements(By.XPATH, ".//*"):
            if sub_elem.text != "":
                match = re.match(r"h(\d+)", sub_elem.tag_name)
                header_level = int(match.group(1)) if match else 0
                texts.append(f"{'#'*header_level}{' ' if header_level > 0 else ''}{sub_elem.text}")
        return "\n\n".join(texts)
    
    def search_single_repo(repo_addr):
        try:
            driver.get(repo_addr)
            model_card = driver.find_element(By.CSS_SELECTOR, "div.prose")
            if search_type == "simple":
                model_card_text = model_card.text
            else: model_card_text = collect_text_from_element(model_card)
        except Exception as e:
            print(f"Error happened on {repo_addr}")
            if verbose: print(e)
        finally:
            return model_card_text

    if isinstance(repo, str):
        repo_addrs = [repo]
    elif isinstance(repo, list):
        repo_addrs = repo
    else: raise ValueError(f"Repo {repo} is not valid")

    driver = get_driver(driver)
    model_cards, failed_repos = {}, []

    for repo_addr in tqdm(repo_addrs):
        model_card = search_single_repo(repo_addr)
        if model_card == "": failed_repos.append(repo_addr)
        model_cards[repo_addr] = model_card
    
    driver.quit() # Close the WebDriver

    return model_cards, failed_repos
        
    