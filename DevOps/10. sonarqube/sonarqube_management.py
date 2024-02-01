from datetime import datetime, timedelta
import requests

from sonarqube_api import SonarQubeAPI


class SonarQubeAPIException(Exception):
    pass


class SonarQubeManagement():
    def __init__(self, sonarqube_api):
        self.sonarqube_api = sonarqube_api
        self.groups_added_to_template = set()

    def create_project(self, name, lob, malcode, visibility='private', repo_type='github'):
        """
        Creates a new project in SonarQube.
        and then associates tags with the project.
        Parameters:
        - name: Name of the new project.
        - lob: Line of Business for the new project.
        - malcode: Malcode identifier for the new project.
        - visibility: Visibility of the new project (default is 'private').
        - repo_type: Type of repository ('github', 'bitbucket', etc.). Default is 'github'.

        Returns:
        - JSON response from the SonarQube server.
        """
        # Generate project key using lob and malcode
        project_name = f"{lob}-{malcode}-{name}"
        project_name = project_name.lower()
        project_key = project_name
        project_info = dict(lob=lob, malcode=malcode, project_key=project_key, repo_type=repo_type,
                            visibility=visibility)
        # Determine main branch based on repo_type
        main_branch = 'main' if repo_type == 'github' else 'master'
        # Tagging the project
        tags = f"{lob},{malcode},{repo_type}"  # Add more tags if needed
        # Create a new project using SonarQubeAPI
        project_response = self.sonarqube_api.create_project(project_key, project_name, visibility, main_branch)
        # Associate tags with the project
        tags_response = self.sonarqube_api.associate_tag_with_project(project_key, tags)
        return project_response, tags_response, project_info

    def delete_project(self, project_key):
        """
        Deletes a project in SonarQube.

        Parameters:
        - project_key: Key of the project to be deleted.

        Returns:
        - JSON response from the SonarQube server.
        """
        # Delete project using SonarQubeAPI
        delete_response = self.sonarqube_api.delete_project(project_key)

        return delete_response, dict(project_key=project_key, deleted_at=datetime.now().isoformat())

    def create_permission_template_for_non_edp_users_and_add_groups(self, malcode, lob, ad_groups):
        """
        Creates a permission template and adds AD groups to it in SonarQube.

        Parameters:
        - malcode: Malcode identifier.
        - lob: Line of Business.
        - ad_groups: List of AD groups separated by commas.

        Returns:
        - JSON response from the SonarQube server.
        """
        # Generate template name using malcode and lob
        template_name = f"{malcode}-{lob}"

        # Check if the template already exists
        existing_templates = self.sonarqube_api.get_permission_templates()
        if template_name in existing_templates:
            return {"message": "Permission template already exists."}

        # Create a new permission template
        create_template_response = self.sonarqube_api.create_permission_template(template_name,
                                                                                 f"Template for {malcode}-{lob}")
        if "errors" in create_template_response:
            return create_template_response  # Return if an error occurs during template creation

        # Add AD groups to the template with individual permissions
        for ad_group in ad_groups.split(','):
            # Check if the AD group already exists
            existing_groups = self.sonarqube_api.get_user_groups()
            if ad_group not in existing_groups:
                return {"message": f"AD group '{ad_group}' does not exist. Permission template creation aborted."}

            # Check if the AD group is already added to the template
            groups_in_template = self.sonarqube_api.get_groups_in_template(template_name)
            if ad_group not in groups_in_template:
                # Add the AD group with 'scan' permission
                add_scan_permission_response = self.sonarqube_api.add_ad_group_to_template(template_name, ad_group,
                                                                                           'scan')
                if "errors" in add_scan_permission_response:
                    return add_scan_permission_response  # Return if an error occurs during permission addition

                # Add the AD group with 'user' permission
                add_user_permission_response = self.sonarqube_api.add_ad_group_to_template(template_name, ad_group,
                                                                                           'user')
                if "errors" in add_user_permission_response:
                    return add_user_permission_response  # Return if an error occurs during permission addition

        return {"message": "Permission template created and AD groups added successfully."}, dict(
            template_name=template_name, ad_groups=ad_groups.split(','))

    def remove_groups_from_template_and_delete_if_empty(self, template_name, groups_to_remove):
        """
        Removes specified AD groups from a permission template in SonarQube.
        If the template doesn't contain any AD groups after removal, the template is deleted.

        Parameters:
        - template_name: Name of the permission template.
        - groups_to_remove: List of AD groups to be removed from the template.

        Returns:
        - JSON response from the SonarQube server.
        """
        # Retrieve existing AD groups from the template
        existing_groups_response = self.sonarqube_api.get_template_ad_groups(template_name)

        if 'groups' in existing_groups_response:
            existing_groups = existing_groups_response['groups']

            # Remove the specified AD groups from the template
            for group_to_remove in groups_to_remove:
                self.sonarqube_api.remove_group_from_template(template_name, group_to_remove)

            # After removal, check if the template has no AD groups left
            updated_groups_response = self.sonarqube_api.get_template_ad_groups(template_name)
            updated_groups = updated_groups_response.get('groups', [])

            # If no AD groups are left, delete the template
            if not updated_groups:
                self.sonarqube_api.delete_permission_template(template_name)

        return existing_groups_response

    def transfer_projects(self, project_id, malcode, lob_name, new_project_name, update_visibility=True):
        """
        Transfers a project to the correct format in lob-malcode-name.

        Parameters:
        - project_id: ID of the existing project to be transferred.
        - malcode: Malcode to be included in the new project format.
        - lob_name: Name of the line of business to be included in the new project format.
        - new_project_name: New project name to be used in the correct format.
        - update_visibility: Flag to update project visibility (default is True).

        Returns:
        - JSON response from the SonarQube server.
        """
        # Get information about the existing project
        project_info = self.sonarqube_api.get_project_info(project_id)

        # Extract existing project details
        existing_project_key = project_info.get('key')

        # Construct the new project key
        new_project_key = f'{lob_name}-{malcode}-{new_project_name}'

        # Update the project key
        result = self.sonarqube_api.update_project_key(existing_project_key, new_project_key)

        # Update project visibility if specified
        if update_visibility:
            self.sonarqube_api.update_project_visibility(existing_project_key)

        return result
