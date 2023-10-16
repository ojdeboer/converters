import os
import xml.etree.ElementTree as ET
from geojson import Feature, FeatureCollection, dump

# path = "C:\\Users\\Onno\\data\\data\\pancreas"
path = "D:\\qupath\\"

classes = {"roi": [130, 76, 157],
           "cancer_ducts": [218, 115, 235],
           "normal_ducts": [192, 91, 8],
           "islets": [9, 118, 25],
           "nerves": [116, 96, 249],
           "lyfocytic_infiltrate": [106, 236, 190],
           "vessels": [240, 205, 62],
           "fat":[211, 49, 153],
           "atrophic_metaplastic_parenchyma": [222, 50, 123],
           "acinic_tissue": [194, 24, 92],
           "mucinious_dissection": [113, 29, 84],
           "uncertain": [87, 230, 174],
           "duodenum": [120, 150, 241],
           "ignore": [180, 57, 18],
           "in_situ_neoplasia": [226, 34, 198]
            }

for file in os.listdir(path):
    if file.endswith(".xml"):
        tree = ET.parse(os.path.join(path, file))
        root = tree.getroot()

        features = []

        for key, value in classes.items():

            roi_elements = root.findall(f'.//Annotation[@PartOfGroup="{key}"]')
            for roi_element in roi_elements:
                coords = []
                for coordinate in roi_element.findall('.//Coordinate'):
                    x = float(coordinate.get('X'))  # Convert to float if needed
                    y = float(coordinate.get('Y'))
                    coords.append([x, y])

                coords.append(coords[0])  # Close the polygon by adding the first point again
                feature = Feature(geometry={"type": "Polygon", "coordinates": [coords]},
                                  properties={"objectType": "annotation",
                                  "classification": {"name": key, "color": value}})
                features.append(feature)

        feature_collection = FeatureCollection(features)

        with open(os.path.join(path, file[:-4] + ".geojson"), 'w') as f:
            dump(feature_collection, f)
