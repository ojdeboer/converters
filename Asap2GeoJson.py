import os
import xml.etree.ElementTree as ET
from geojson import Feature, FeatureCollection, dump

# path = "C:\\Users\\Onno\\data\\data\\pancreas"
path = "D:\\qupath\\"

for file in os.listdir(path):
    if file.endswith(".xml"):
        tree = ET.parse(os.path.join(path, file))
        root = tree.getroot()

        features = []

        roi_elements = root.findall('.//Annotation[@PartOfGroup="roi"]')
        for roi_element in roi_elements:
            coords = []
            for coordinate in roi_element.findall('.//Coordinate'):
                x = float(coordinate.get('X'))  # Convert to float if needed
                y = float(coordinate.get('Y'))
                coords.append([x, y])

            coords.append(coords[0])  # Close the polygon by adding the first point again
            feature = Feature(geometry={"type": "Polygon", "coordinates": [coords]},
                              properties={"objectType": "annotation",
                              "classification": {"name": "roi", "color": [130, 76, 157]}})
            features.append(feature)

        roi_elements = root.findall('.//Annotation[@PartOfGroup="cancer_ducts"]')
        for roi_element in roi_elements:
            coords = []
            for coordinate in roi_element.findall('.//Coordinate'):
                x = float(coordinate.get('X'))  # Convert to float if needed
                y = float(coordinate.get('Y'))
                coords.append([x, y])

            coords.append(coords[0])  # Close the polygon by adding the first point again
            feature = Feature(geometry={"type": "Polygon", "coordinates": [coords]},
                              properties={"objectType": "annotation",
                                          "classification": {"name": "cancer_ducts", "color": [218, 115, 235]}})

            features.append(feature)


        feature_collection = FeatureCollection(features)

        with open(os.path.join(path, file[:-4] + ".geojson"), 'w') as f:
            dump(feature_collection, f)
