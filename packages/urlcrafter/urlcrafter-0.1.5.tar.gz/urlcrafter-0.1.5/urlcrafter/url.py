"""
URLCrafter URL class implementation
Created by Madhav Panchal (2025)
"""

import urllib.parse
import re
from typing import Dict, List, Union, Optional, Any


class URL:
    """
    A class for building and manipulating URLs with a chainable API.
    """
    
    def __init__(self, base_url: str = ""):
        """
        Initialize a URL object with an optional base URL.
        
        Args:
            base_url (str): The base URL to start with. Defaults to empty string.
        """
        self.parsed = urllib.parse.urlparse(base_url)
        self.scheme = self.parsed.scheme
        self.netloc = self.parsed.netloc
        self.path = self.parsed.path
        self.params = self.parsed.params
        self.query_params = dict(urllib.parse.parse_qsl(self.parsed.query))
        self.fragment = self.parsed.fragment
    
    def set_scheme(self, scheme: str) -> 'URL':
        """
        Set the URL scheme (http, https, etc.).
        
        Args:
            scheme (str): The scheme to set.
        
        Returns:
            URL: The URL object for chaining.
        """
        self.scheme = scheme
        return self
    
    def set_netloc(self, netloc: str) -> 'URL':
        """
        Set the network location (domain) part of the URL.
        
        Args:
            netloc (str): The network location to set.
        
        Returns:
            URL: The URL object for chaining.
        """
        self.netloc = netloc
        return self
    
    def set_path(self, path: str) -> 'URL':
        """
        Set the path of the URL.
        
        Args:
            path (str): The path to set.
        
        Returns:
            URL: The URL object for chaining.
        """
        self.path = path if path.startswith('/') else f"/{path}"
        return self
    
    def add_path(self, segment: str) -> 'URL':
        """
        Add a segment to the path of the URL.
        
        Args:
            segment (str): The path segment to add.
        
        Returns:
            URL: The URL object for chaining.
        """
        segment = segment.strip('/')
        if not self.path:
            self.path = f"/{segment}"
        else:
            self.path = f"{self.path.rstrip('/')}/{segment}"
        return self
    
    def add_param(self, key: str, value: Any) -> 'URL':
        """
        Add a query parameter to the URL.
        
        Args:
            key (str): The parameter key.
            value (Any): The parameter value.
        
        Returns:
            URL: The URL object for chaining.
        """
        self.query_params[key] = value
        return self
    
    def add_params(self, params: Dict[str, Any]) -> 'URL':
        """
        Add multiple query parameters to the URL.
        
        Args:
            params (Dict[str, Any]): A dictionary of parameters to add.
        
        Returns:
            URL: The URL object for chaining.
        """
        self.query_params.update(params)
        return self
    
    def remove_param(self, key: str) -> 'URL':
        """
        Remove a query parameter from the URL.
        
        Args:
            key (str): The parameter key to remove.
        
        Returns:
            URL: The URL object for chaining.
        """
        if key in self.query_params:
            del self.query_params[key]
        return self
    
    def set_fragment(self, fragment: str) -> 'URL':
        """
        Set the fragment (hash) part of the URL.
        
        Args:
            fragment (str): The fragment to set.
        
        Returns:
            URL: The URL object for chaining.
        """
        self.fragment = fragment.lstrip('#')
        return self
    
    @staticmethod
    def slugify(text: str) -> str:
        """
        Convert text to a URL-friendly slug.
        
        Args:
            text (str): The text to slugify.
        
        Returns:
            str: The slugified text.
        """
        # Convert to lowercase
        text = text.lower()
        # Remove special characters
        text = re.sub(r'[^\w\s-]', '', text)
        # Replace spaces with hyphens
        text = re.sub(r'\s+', '-', text)
        # Remove consecutive hyphens
        text = re.sub(r'-+', '-', text)
        # Remove leading/trailing hyphens
        text = text.strip('-')
        return text
    
    def add_slugified_path(self, text: str) -> 'URL':
        """
        Add a slugified version of the text to the path.
        
        Args:
            text (str): The text to slugify and add to the path.
        
        Returns:
            URL: The URL object for chaining.
        """
        return self.add_path(self.slugify(text))
    
    def build(self) -> str:
        """
        Build and return the complete URL string.
        
        Returns:
            str: The complete URL.
        """
        query = urllib.parse.urlencode(self.query_params)
        parts = urllib.parse.ParseResult(
            scheme=self.scheme,
            netloc=self.netloc,
            path=self.path,
            params=self.params,
            query=query,
            fragment=self.fragment
        )
        return urllib.parse.urlunparse(parts)
    
    @classmethod
    def parse(cls, url_string: str) -> 'URL':
        """
        Parse an existing URL string and return a URL object.
        
        Args:
            url_string (str): The URL string to parse.
        
        Returns:
            URL: A URL object representing the parsed URL.
        """
        return cls(url_string)
    
    def __str__(self) -> str:
        """
        Return the string representation of the URL.
        
        Returns:
            str: The URL string.
        """
        return self.build()
