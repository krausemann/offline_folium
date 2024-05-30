from urllib.request import urlopen
import os

import folium
import folium.plugins
from folium.elements import JSCSSMixin
from .paths import dest_path
from inspect import getmembers, isclass, ismodule

def download_all_files():
    filelist = []
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    for _, js_url in folium.folium._default_js:
        filelist.append(js_url)
    for _, js_url in folium.folium._default_css:
        filelist.append(js_url)
    for name, module in getmembers(folium.plugins, predicate=ismodule):
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            if isclass(attribute) and issubclass(attribute, JSCSSMixin):
                if attribute.default_js:
                    for _, js_url in attribute.default_js:
                        filelist.append(js_url)
                if attribute.default_css:
                    for _, js_url in attribute.default_css:
                        filelist.append(js_url)
    filelist = set(filelist)
    for link in filelist:
        download_url(link)


def download_url(url):
    output_path = os.path.join(dest_path, os.path.basename(url))
    print(f"Downloading {output_path}")
    contents = urlopen(url).read().decode("utf8")
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(contents)

if __name__ == "__main__":
    print(f"Downloading files to {dest_path}")
    download_all_files()
