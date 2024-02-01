from datetime import datetime, timedelta

import requests


class SonarQubeAPI:
    def __init__(self, base_url, token):
        """
        Initializes the SonarQubeAPI instance with the base URL and API token.
        """
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {token}'}

    def bulk_delete_projects(self, project_keys):
        """
        Deletes multiple projects in bulk in SonarQube.

        Parameters:
        - project_keys: Comma-separated list of project keys.

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/projects/bulk_delete'
        data = {'projects': project_keys}
        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def create_project(self, project_key, project_name, visibility='private', main_branch=None):
        """
        Creates a new project in SonarQube.

        Parameters:
        - project_key: Key for the new project.
        - project_name: Name of the new project.
        - visibility: Visibility of the new project (default is 'private').
        - main_branch: Main branch for the project.

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/projects/create'
        data = {
            'project': project_key,
            'name': project_name,
            'visibility': visibility,
            'mainBranch': main_branch
        }
        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def delete_project(self, project_key):
        """
        Deletes a project in SonarQube.

        Parameters:
        - project_key: Key of the project to be deleted.

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/projects/delete'
        data = {'project': project_key}
        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def create_tag(self, tag_name):
        """
        Creates a new tag in SonarQube.

        Parameters:
        - tag_name: Name of the new tag.

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/project_tags/create'
        data = {'name': tag_name}
        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def delete_tag(self, tag_name):
        """
        Deletes a tag in SonarQube.

        Parameters:
        - tag_name: Name of the tag to be deleted.

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/project_tags/delete'
        data = {'name': tag_name}
        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def associate_tag_with_project(self, project_key, tags):
        """
        Associates tags with a project in SonarQube.

        Parameters:
        - project_key: Key of the project.
        - tags: Comma-separated string of tags.

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/project_tags/set'
        data = {'project': project_key, 'tags': tags}
        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def create_permission_template(self, template_name, description):
        """
        Creates a new permission template in SonarQube.

        Parameters:
        - template_name: Name of the new permission template.
        - description: Description for the new permission template.

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/permissions/create_template'
        data = {'name': template_name, 'description': description}
        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def delete_permission_template(self, template_name):
        """
        Deletes a permission template in SonarQube.

        Parameters:
        - template_name: Name of the permission template to be deleted.

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/permissions/delete_template'
        data = {'templateName': template_name}
        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def add_ad_group_to_template(self, template_name, group_name, permission):
        """
        Adds an AD group to a permission template in SonarQube.

        Parameters:
        - template_name: Name of the permission template.
        - group_name: Name of the AD group to be added.
        - permission: Permission to be granted to the AD group.

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/permissions/add_group_to_template'
        data = {'templateName': template_name, 'groupName': group_name, 'permission': permission}
        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def remove_ad_group_from_template(self, template_name, group_name, permission):
        """
        Removes an AD group from a permission template in SonarQube.

        Parameters:
        - template_name: Name of the permission template.
        - group_name: Name of the AD group to be removed.
        - permission: Permission to be revoked from the AD group.

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/permissions/remove_group_from_template'
        data = {'templateName': template_name, 'groupName': group_name, 'permission': permission}
        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def apply_permission_template_to_project(self, template_name, project_key):
        """
        Applies a permission template to a project in SonarQube.

        Parameters:
        - template_name: Name of the permission template.
        - project_key: Key of the project.

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/permissions/apply_template'
        data = {'templateName': template_name, 'projectKey': project_key}
        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def create_user_group(self, name=None, description=None):
        """
        Creates a new user group in SonarQube.

        Parameters:
        - name: (Optional) Name of the new user group.
        - description: (Optional) Description for the new user group.

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/user_groups/create'
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description

        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def delete_user_group(self, name):
        """
        Deletes a user group in SonarQube.

        Parameters:
        - name: Name of the user group to be deleted.

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/user_groups/delete'
        data = {'name': name}
        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def _handle_response(self, response):
        """
        Handles the response from the SonarQube API and raises an exception if the status code is not in the 2xx range.

        Parameters:
        - response: The response object from the requests library.
        """
        if not (200 <= response.status_code < 300):
            return(f"SonarQube API request failed with status code {response.status_code}: {response.text}")
        # if response has json return, return it, else return the response text
        return response.json() if response.headers.get('content-type') == 'application/json' else response.text

    def get_projects_analyzed_before(self, days_ago):
        """
        Retrieves projects analyzed before a specified date.

        Parameters:
        - days_ago: Number of days ago to consider as the cutoff date.

        Returns:
        - JSON response from the SonarQube server containing projects analyzed before the specified date.
        """
        cutoff_date = datetime.now() - timedelta(days=days_ago)
        formatted_date = cutoff_date.strftime('%Y-%m-%dT%H:%M:%S%z')

        endpoint = f'{self.base_url}/api/projects/search'
        params = {'analyzedBefore': formatted_date}
        response = requests.get(endpoint, params=params, headers=self.headers)
        return self._handle_response(response)


    def remove_group_from_template(self, template_name, group_name, permission):
        """
        Removes a specified group (or 'anyone') from a permission template in SonarQube.

        Parameters:
        - template_name: Name of the permission template.
        - group_name: Group name or 'anyone' (case insensitive).
        - permission: Permission to be revoked from the group.

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/permissions/remove_group_from_template'
        data = {'templateName': template_name, 'groupName': group_name, 'permission': permission}
        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def update_project_key(self, from_key, to_key):
        """
        Updates the key of a project in SonarQube.

        Parameters:
        - from_key: Old key of the project to be updated.
        - to_key: New key for the project.

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/projects/update_key'
        data = {'from': from_key, 'to': to_key}
        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def update_project_visibility(self, project, visibility='private'):
        """
        Updates the visibility of a project in SonarQube.

        Parameters:
        - project: ID or key of the project to be updated.
        - visibility: New visibility for the project (default is 'private').

        Returns:
        - JSON response from the SonarQube server.
        """
        endpoint = f'{self.base_url}/api/projects/update_visibility'
        data = {'id': project, 'visibility': visibility}
        response = requests.post(endpoint, data=data, headers=self.headers)
        return self._handle_response(response)

    def get_user_groups(self, q=None, f=None):
        """
        Retrieves user groups from SonarQube based on search parameters.

        Parameters:
        - q: (Optional) String to limit search to names that contain the supplied string.
        - f: (Optional) Flag to limit search to name only.

        Returns:
        - JSON response from the SonarQube server containing user groups based on the search parameters.
        """
        endpoint = f'{self.base_url}/api/user_groups/search'
        params = {}
        if q:
            params['q'] = q
        if f:
            params['f'] = f

        response = requests.get(endpoint, params=params, headers=self.headers)
        return self._handle_response(response)
# # Example usage:
# sonarqube_url = 'http://localhost:9999'
# api_token = 'squ_ae8525e3c50ac5e108e36fc800084b86cb37bfaa'
# sonarqube_api = SonarQubeAPI(sonarqube_url, api_token)
#
# # Create a new permission template
# template_response = sonarqube_api.create_permission_template('my_template', 'My Template Description')
# print(f"Permission template created: {template_response}")
#
# # Create a new AD group
# group_response = sonarqube_api.create_user_group('my_ad_group', 'My AD Group Description')
# # Add an AD group to the permission template
# add_group_response = sonarqube_api.add_ad_group_to_template('my_template', 'my_ad_group', 'admin')
# print(f"AD group added to permission template: {add_group_response}")
#
# # Remove the AD group from the permission template
# remove_group_response = sonarqube_api.remove_ad_group_from_template('my_template', 'my_ad_group', 'admin')
# print(f"AD group removed from permission template: {remove_group_response}")
#
# # Create a new project with default visibility set to private
# project_response = sonarqube_api.create_project('my_project_key', 'My_Project', main_branch='main')
# print(f"Project created: {project_response}")
#
# # ssociate tags with the project using a comma-separated string
# tags = 'tag1,tag2,tag3'
# associate_tags_response = sonarqube_api.associate_tag_with_project('my_project_key', tags)
# print(f"Tags associated with project: {associate_tags_response}")
#
# # Apply the permission template to the project
# apply_template_response = sonarqube_api.apply_permission_template_to_project('my_template', 'my_project_key')
# print(f"Permission template applied to project: {apply_template_response}")
#
# # Delete a project
# delete_response = sonarqube_api.delete_project('my_project_key')
# print(f"Project deleted: {delete_response}")
#
# # Delete permission template
# delete_template_response = sonarqube_api.delete_permission_template('my_template')
# print(f"Permission template deleted: {delete_template_response}")
