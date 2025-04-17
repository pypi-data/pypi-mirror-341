import pandas as pd
import numpy as np
import requests
from .data_download import download_data


class OpenDataSet:
    def __init__(self, url:str, headers=None):
        self.url = url
        self.id = url.split('/')[-1]
        # self.metadata = {}
        ## based on https://stackoverflow.com/questions/41946166/requests-get-returns-403-while-the-same-url-works-in-browser
        if headers == True:
            self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        elif type(headers) == dict or headers is None:
            self.headers = headers
        else:
            raise ValueError("headers param must be True, None, or a dictionary")
    
    def __repr__(self):
        return f"OpenDataSet('{self.id}')"
    
    @property    
    def metadata(self):
        # Fetch metadata from the API
        response = requests.get(f"http://datos.gob.es/apidata/catalog/dataset/{self.id}",
                                headers=self.headers)
        return response.json()["result"]["items"][0]
        

    @property
    def publisher_data_url(self):
        return self.metadata.get('identifier')

    @property
    def title(self):
        # Extract all title values based on language code
        titles = {d['_lang']: d['_value'] for d in self.metadata.get('title', [])}
        return titles

    @property
    def description(self):
        # Extract the first description value for each language
        descriptions = {d['_lang']: d['_value'] for d in self.metadata.get('description', [])}
        return descriptions

    @property
    def keywords(self):
        # Group keywords by language and remove duplicates
        keywords = {}
        for entry in self.metadata.get('keyword', []):
            lang_code = entry['_lang']
            keyword = entry['_value']
            keywords.setdefault(lang_code, set()).add(keyword)
        return {lang: list(values) for lang, values in keywords.items()}

    @property
    def distributions(self):
        """
        Returns a list of Distribution objects, each containing information for a single distribution.
        """
        distributions = self.metadata.get('distribution', [])
        distribution_objects = []
        for distribution_data in distributions:
            distribution_objects.append(Distribution(distribution_data))
        return distribution_objects

    def get_distribution_by_format(self, format):
        """
        Returns the distribution information for a specific format (e.g., text/csv).
        """
        matched_distributions = []
        for distribution in self.distributions:
            if distribution.format == format:
                matched_distributions.append(distribution)
        return matched_distributions
    
    
class Distribution:
    def __init__(self, metadata):
        self.metadata = metadata
    
    def __repr__(self):
        return f"Distribution(accessURL={self.access_url}, format={self.format}, byte_size={self.byte_size}, titles={self.titles})"


    @property
    def access_url(self):
        return self.metadata.get('accessURL')

    @property
    def byte_size(self):
        return self.metadata.get('byteSize')

    @property
    def format(self):
        return self.metadata.get('format')['value']

    @property
    def titles(self):
        # Extract title information for all languages efficiently
        return {d['_lang']: d['_value'] for d in self.metadata.get('title', [])}
    
    def download_data(self, output_file=None):
        """
        Downloads the data from the distribution URL and optionally saves it to a file or attempts to load it as a pandas DataFrame.

        This method utilizes the download_data function from the data_download module.

        Args:
            output_file (str, optional): Path to the file where downloaded data should be saved.
                Defaults to None.

        Returns:
            pandas.DataFrame | bytes | None: The loaded DataFrame on success, raw bytes on unknown format, or None on errors.
        """
        return download_data(self.access_url, output_file)
    
    @property
    def data(self):
        """
        Returns the downloaded data as a pandas DataFrame, raw bytes, or None if not downloaded yet.
        """
        if self.access_url:
            return self.download_data()  # Download data if not already downloaded
        return None
