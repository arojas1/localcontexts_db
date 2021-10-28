from helpers.utils import get_labels_json

# fetch data from Labels.json
data = get_labels_json()

def check_bclabel_type(label):
    for key, values in data.items():
        if key == 'bcLabels':
            if(isinstance(values, list)):
                for value in values:
                    if label == value['labelCode']:
                        return value['labelType']
                    elif label == 'placeholder':
                        return False

def assign_bclabel_img(label_type):
    baseURL = 'https://storage.googleapis.com/anth-ja77-local-contexts-8985.appspot.com/labels/bclabels/'

    for key, values in data.items():
        if key == 'bcLabels':
            if(isinstance(values, list)):
                for value in values:
                    if label_type == value['labelCode']:
                        return baseURL + value['imgFileName']
                    elif label_type == 'placeholder':
                        return None
