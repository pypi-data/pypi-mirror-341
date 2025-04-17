#  Copyright (c) 2023.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import subprocess
import os
from .folder_exist import folder_exist


def clone_repo(clone_url, repo_name, clone_path):
    # Create the directory if it doesn't exist.
    if not os.path.exists(clone_path):
        os.makedirs(clone_path)

    # Run git clone within the specified path.
    if folder_exist(clone_path + "/" + repo_name):
        result = subprocess.run(['git', 'pull'], cwd=clone_path + "/" + repo_name)
        print(f"Pull {repo_name} with exit code {result.returncode}")
    else:
        result = subprocess.run(['git', 'clone', clone_url], cwd=clone_path)
        print(f"Cloned {repo_name} with exit code {result.returncode}")