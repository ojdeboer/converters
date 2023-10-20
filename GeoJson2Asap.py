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
    {"Color": "0000ff", "Name": "nucleus_normal", "PartOfGroup": "None"},
    {"Color": "0000ff", "Name": "nucleus_islets", "PartOfGroup": "None"},
    {"Color": "0000ff", "Name": "nucleus_acinic_tissue", "PartOfGroup": "None"},
    {"Color": "0000ff", "Name": "nucleus_lymfocyte", "PartOfGroup": "None"}
]

def set_color(color):
    if color == [130, 76, 157]:  # roi
        return "#ffff00"
    elif color == [218, 115, 235]:  # cancer_ducts
        return "#ff0000"
    elif color == [192, 91, 8]:  # normal_ducts
        return "#1100fe"
    elif color == [9, 118, 25]:  # islets
        return "#00fefe"
    elif color == [116, 96, 249]:  # nerves
        return "#ffff00"
    elif color == [106, 236, 190]:  # lymfocytic_infiltrates
        return "#fe60fc"
    elif color == [240, 205, 62]:  # vessels
        return "#fe8083"
    elif color == [211, 49, 153]:  # fat
        return "#6ca4ff"
    elif color == [222, 50, 123]:  # atrophic_metaplastic_parenchyma
        return "#34781c"
    elif color == [194, 24, 92]:  # acinic_tissue
        return "#7d7344"
    elif color == [113, 29, 84]:  # mucinous_dissection
        return "#2e6666"
    elif color == [87, 230, 174]:  # uncertain
        return "#818181"
    elif color == [120, 150, 241]:  # duodenum
        return "#aa5500"
    elif color == [180, 57, 18]:  # ignore
        return "#000000"
    elif color == [226, 34, 198]:  # in_situ_neoplasia
        return "#ffffff"
    elif color == []:  # lumen
        return "#64fe2e"
    else:
        return "#ffffff"



for file in os.listdir(geojson_path):
    if file.endswith(".geojson"):
        with open(os.path.join(geojson_path, file), 'r') as f:

            root = ET.Element("ASAP_Annotations")  # create xml file
            annotation_groups = ET.SubElement(root, "AnnotationGroups")  # add annotation group subelements
            for group_data in groups_data:
                group = ET.SubElement(annotation_groups, "Group", attrib=group_data)
                ET.SubElement(group, "Attributes")
            annotations = ET.SubElement(root, "Annotations")

            data = geojson.load(f)
            if data['type'] == 'FeatureCollection':
                # iterate over features of the FeatureCollection
                annotation_counter = 0
                for feature in data['features']:
                    properties = feature['properties']
                    try:
                        name = properties["classification"]['name']
                        color = set_color(properties["classification"]['color'])
                    except:
                        name = "None"
                        color = "#ffffff"
                    annotation = ET.SubElement(annotations, "Annotation")
                    annotation.set("Color", color)
                    annotation.set("Name", "Annotation " + str(annotation_counter))
                    annotation.set("PartOfGroup", name)
                    annotation.set("Type", "Polygon")
                    # Access properties and geometry of each feature

                    geometry = feature['geometry']
                    if geometry['type'] == "Polygon":
                        coordinates = geometry['coordinates'][0]
                        coordinate_counter = 0
                        asap_coordinates = ET.SubElement(annotation, "Coordinates")
                        for coordinate in coordinates:
                            asap_coordinate = ET.SubElement(asap_coordinates, "Coordinate")
                            asap_coordinate.set("Order", str(coordinate_counter))
                            asap_coordinate.set("X", str(coordinate[0]))
                            asap_coordinate.set("Y", str(coordinate[1]))
                            coordinate_counter+=1
                    annotation_counter+=1
        tree = ET.ElementTree(root)
        tree.write(os.path.join(geojson_path, file[:-8] + "_geojson.xml"))





