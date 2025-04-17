import base64

def img_to_base64(path_to_file):
    #mage_folder = app.config['OFFICE_FOLDER']
    #ath_to_file = image_folder + filename

    with open(path_to_file, 'rb') as binary_file:
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_message = base64_encoded_data.decode('utf-8')
        return base64_message
    return 0