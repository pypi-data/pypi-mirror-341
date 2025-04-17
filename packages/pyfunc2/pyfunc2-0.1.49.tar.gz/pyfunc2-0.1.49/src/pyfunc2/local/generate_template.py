import os

def generate_template(words, template_path, target_project_folder):
    if not os.path.exists(target_project_folder):
        os.makedirs(target_project_folder)
    # get list of file from path
    files = os.listdir(template_path)
    print(files)
    print(words)
    if not words:
        print(f"!!!!!! words {words} does not exist")
        exit(1)

    for template_file in files:
        # if file is not a directory, create a new file in target project folder and replace each words from array by names and values {domain: value, organization: value}
        # if file is a directory, create a new directory in target project folder and copy all files and subdirectories from the template folder to the new directory
        if os.path.isdir(template_file):
            #template_path_file = template_path + "/" + template_file
            project_path_file = target_project_folder + "/" + template_file
            # Create the directory if it doesn't exist.
            if not os.path.exists(project_path_file):
                os.makedirs(project_path_file)

            #print(f"Template {template_path_file}: {template}")
            # save the template
        if os.path.isfile(template_file):
            template_path_file = template_path + "/" + template_file
            project_path_file = target_project_folder + "/" + template_file
            print('template_path_file', template_path_file)

            # get file and replace in the template each words from array by names and values {domain: value, organization: value}
            with open(template_path_file, 'r') as file:
                template = file.read()

            # list in for loop value and name from array elements
            for key, value in words.items():
                template = template.replace("{" + key + "}", value)

            #print(f"Template {template_path_file}: {template}")
            # save the template in path
            with open(project_path_file, 'x') as file:
                file.write(template)