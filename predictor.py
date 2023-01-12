

import numpy as np
import joblib
from nltk.tokenize import RegexpTokenizer
import tldextract
import pandas as pd
from urllib.parse import urlparse
from typing import *

# predict


def predict(url):

    def parse_url(url: str) -> Optional[Dict[str, str]]:

        try:
            no_scheme = not url.startswith(
                'https://') and not url.startswith('http://')
            if no_scheme:
                parsed_url = urlparse(f"http://{url}")

                return {
                    "scheme": [None],  # not established a value for this
                    "netloc": [parsed_url.netloc],
                    "path": [parsed_url.path],
                    "params": [parsed_url.params],
                    "query": [parsed_url.query],
                    "fragment": [parsed_url.fragment],
                }
            else:
                parsed_url = urlparse(url)
                return {
                    "scheme": [parsed_url.scheme],
                    "netloc": [parsed_url.netloc],
                    "path": [parsed_url.path],
                    "params": [parsed_url.params],
                    "query": [parsed_url.query],
                    "fragment": [parsed_url.fragment],
                }
        except:
            return None

    df = pd.DataFrame(parse_url(url))
    df
    df["length"] = len(url)
    df["tld"] = df.netloc.apply(lambda nl: tldextract.extract(nl).suffix)
    df['tld'] = df['tld'].replace('', 'None')
    df["is_ip"] = df.netloc.str.fullmatch(r"\d+\.\d+\.\d+\.\d+")
    df['domain_hyphens'] = df.netloc.str.count('-')
    df['domain_underscores'] = df.netloc.str.count('_')
    df['path_hyphens'] = df.path.str.count('-')
    df['path_underscores'] = df.path.str.count('_')
    df['slashes'] = df.path.str.count('/')
    df['full_stops'] = df.path.str.count('.')

    def get_num_subdomains(netloc: str) -> int:
        subdomain = tldextract.extract(netloc).subdomain
        if subdomain == "":
            return 0
        return subdomain.count('.') + 1

    df['num_subdomains'] = df['netloc'].apply(
        lambda net: get_num_subdomains(net))
    tokenizer = RegexpTokenizer(r'[A-Za-z]+')

    def tokenize_domain(netloc: str) -> str:
        split_domain = tldextract.extract(netloc)
        no_tld = str(split_domain.subdomain + '.' + split_domain.domain)
        return " ".join(map(str, tokenizer.tokenize(no_tld)))

    df['domain_tokens'] = df['netloc'].apply(lambda net: tokenize_domain(net))
    df['path_tokens'] = df['path'].apply(
        lambda path: " ".join(map(str, tokenizer.tokenize(path))))
    df.drop(df.columns[:6], axis=1, inplace=True)
    df = df.select_dtypes(include=[np.number])

    loaded_model = joblib.load("xgb.pkl")
    return loaded_model.predict(df)[0]
