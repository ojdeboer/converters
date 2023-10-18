import os
import xml.etree.ElementTree as ET
import geojson

geojson_path = "C:\\Users\\Onno\\QuPath\\Nuclear_segmentation\\"

groups_data = [
    {"Color": "#ffff00", "Name": "roi", "PartOfGroup": "None"},
    {"Color": "#55ff00", "Name": "tumor_area", "PartOfGroup": "None"},
    {"Color": "#ffaa00", "Name": "non_tumor_area", "PartOfGroup": "None"},
    {"Color": "#ff0000", "Name": "cancer_ducts", "PartOfGroup": "None"},
    {"Color": "#1100fe", "Name": "normal_ducts", "PartOfGroup": "None"},
    {"Color": "#00fefe", "Name": "islets", "PartOfGroup": "None"},
    {"Color": "#ffff00", "Name": "nerves", "PartOfGroup": "None"},
    {"Color": "#fe60fc", "Name": "lymfocytic_infiltrate", "PartOfGroup": "None"},
    {"Color": "#fe8083", "Name": "vessels", "PartOfGroup": "None"},
    {"Color": "#6ca4ff", "Name": "fat", "PartOfGroup": "None"},
    {"Color": "#34781c", "Name": "atrophic_metaplastic_parenchyma", "PartOfGroup": "None"},
    {"Color": "#7d7344", "Name": "acinic_tissue", "PartOfGroup": "None"},
    {"Color": "#2e6666", "Name": "mucinous_dissection", "PartOfGroup": "None"},
    {"Color": "#818181", "Name": "uncertain", "PartOfGroup": "None"},
    {"Color": "#aa5500", "Name": "duodenum", "PartOfGroup": "None"},
    {"Color": "#000000", "Name": "ignore", "PartOfGroup": "None"},
    {"Color": "#ffffff", "Name": "in_situ_neoplasia", "PartOfGroup": "None"},
    {"Color": "#64fe2e", "Name": "lumen", "PartOfGroup": "None"},
    {"Color": "0000ff", "Name": "nucleus_tumor", "PartOfGroup": "None"},
    {"Color": "0000ff", "Name": "nucleus_normal", "PartOfGroup": "None"}
]


for file in os.listdir(geojson_path):
    if file.endswith(".geojson"):
        with open(os.path.join(geojson_path, file), 'r') as file:

            root = ET.Element("ASAP_Annotations")
            annotation_groups = ET.SubElement(root, "AnnotationGroups")
            for group_data in groups_data:
                group = ET.SubElement(annotation_groups, "Group", attrib=group_data)
                ET.SubElement(group, "Attributes")
            annotations = ET.SubElement(root, "Annotations")

            data = geojson.load(file)
            if data['type'] == 'FeatureCollection':
                # iterate over features of the FeatureCollection
                for feature in data['features']:
                    # Access properties and geometry of each feature
                    properties = feature['properties']
                    geometry = feature['geometry']
                    if geometry['type'] == "Polygon":
                        coordinates = geometry['coordinates'][0][0]
                        try:
                            print(properties['objectType'], properties['classification'])
                        except:
                            print(properties['objectType'])
                        print(coordinates)
                        print('-' * 20)

                        tree = ET.ElementTree(root)
                        tree.write(os.path.join(geojson_path, "output.xml"))




