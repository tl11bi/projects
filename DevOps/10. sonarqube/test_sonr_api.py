from unittest import TestCase


import unittest
from unittest.mock import MagicMock, patch
from sonarqube_api import SonarQubeAPI
from sonarqube_management import SonarQubeAPIException


class TestSonarQubeAPI(unittest.TestCase):
    def setUp(self):
        self.sonarqube_url = 'http://localhost:9999'
        self.api_token = 'squ_ae8525e3c50ac5e108e36fc800084b86cb37bfaa'
        self.sonarqube_api = SonarQubeAPI(self.sonarqube_url, self.api_token)

    def mock_response(self, status_code, json_data=None, text_data=None):
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.json.return_value = json_data
        mock_resp.text = text_data
        return mock_resp

    def test_bulk_delete_projects(self):
        project_keys = 'project_key_1,project_key_2,project_key_3'
        expected_response = {'success': True}
        mock_response = self.mock_response(200, json_data=expected_response)
        self.sonarqube_api._handle_response = MagicMock(return_value=expected_response)
        self.sonarqube_api._handle_response.side_effect = None
        self.sonarqube_api._handle_response.return_value = expected_response
        self.sonarqube_api._handle_response.assert_not_called()

        with unittest.mock.patch('requests.post', return_value=mock_response):
            response = self.sonarqube_api.bulk_delete_projects(project_keys)

        self.sonarqube_api._handle_response.assert_called_once_with(mock_response)
        self.assertEqual(response, expected_response)

    def test_create_project(self):
        project_key = 'my_project_key'
        project_name = 'My_Project'
        main_branch = 'main'
        expected_response = {'success': True}
        mock_response = self.mock_response(200, json_data=expected_response)
        self.sonarqube_api._handle_response = MagicMock(return_value=expected_response)
        self.sonarqube_api._handle_response.side_effect = None
        self.sonarqube_api._handle_response.return_value = expected_response
        self.sonarqube_api._handle_response.assert_not_called()

        with unittest.mock.patch('requests.post', return_value=mock_response):
            response = self.sonarqube_api.create_project(project_key, project_name, main_branch=main_branch)

        self.sonarqube_api._handle_response.assert_called_once_with(mock_response)
        self.assertEqual(response, expected_response)

    def test_delete_project(self):
        project_key = 'my_project_key'
        expected_response = {'success': True}
        mock_response = self.mock_response(200, json_data=expected_response)
        self.sonarqube_api._handle_response = MagicMock(return_value=expected_response)
        self.sonarqube_api._handle_response.side_effect = None
        self.sonarqube_api._handle_response.return_value = expected_response
        self.sonarqube_api._handle_response.assert_not_called()

        with unittest.mock.patch('requests.post', return_value=mock_response):
            response = self.sonarqube_api.delete_project(project_key)

        self.sonarqube_api._handle_response.assert_called_once_with(mock_response)
        self.assertEqual(response, expected_response)

    def test_create_tag(self):
        tag_name = 'my_tag'
        expected_response = {'success': True}
        mock_response = self.mock_response(200, json_data=expected_response)
        self.sonarqube_api._handle_response = MagicMock(return_value=expected_response)
        self.sonarqube_api._handle_response.side_effect = None
        self.sonarqube_api._handle_response.return_value = expected_response
        self.sonarqube_api._handle_response.assert_not_called()

        with unittest.mock.patch('requests.post', return_value=mock_response):
            response = self.sonarqube_api.create_tag(tag_name)

        self.sonarqube_api._handle_response.assert_called_once_with(mock_response)
        self.assertEqual(response, expected_response)

    def test_delete_tag(self):
        tag_name = 'my_tag'
        expected_response = {'success': True}
        mock_response = self.mock_response(200, json_data=expected_response)
        self.sonarqube_api._handle_response = MagicMock(return_value=expected_response)
        self.sonarqube_api._handle_response.side_effect = None
        self.sonarqube_api._handle_response.return_value = expected_response
        self.sonarqube_api._handle_response.assert_not_called()

        with unittest.mock.patch('requests.post', return_value=mock_response):
            response = self.sonarqube_api.delete_tag(tag_name)

        self.sonarqube_api._handle_response.assert_called_once_with(mock_response)
        self.assertEqual(response, expected_response)

    def test_associate_tag_with_project(self):
        project_key = 'my_project_key'
        tags = 'tag1,tag2,tag3'
        expected_response = {'success': True}
        mock_response = self.mock_response(200, json_data=expected_response)
        self.sonarqube_api._handle_response = MagicMock(return_value=expected_response)
        self.sonarqube_api._handle_response.side_effect = None
        self.sonarqube_api._handle_response.return_value = expected_response
        self.sonarqube_api._handle_response.assert_not_called()

        with unittest.mock.patch('requests.post', return_value=mock_response):
            response = self.sonarqube_api.associate_tag_with_project(project_key, tags)

        self.sonarqube_api._handle_response.assert_called_once_with(mock_response)
        self.assertEqual(response, expected_response)

    def test_create_permission_template(self):
        template_name = 'my_template'
        description = 'My Template Description'
        expected_response = {'success': True}
        mock_response = self.mock_response(200, json_data=expected_response)
        self.sonarqube_api._handle_response = MagicMock(return_value=expected_response)
        self.sonarqube_api._handle_response.side_effect = None
        self.sonarqube_api._handle_response.return_value = expected_response
        self.sonarqube_api._handle_response.assert_not_called()

        with unittest.mock.patch('requests.post', return_value=mock_response):
            response = self.sonarqube_api.create_permission_template(template_name, description)

        self.sonarqube_api._handle_response.assert_called_once_with(mock_response)
        self.assertEqual(response, expected_response)

    def test_delete_permission_template(self):
        template_name = 'my_template'
        expected_response = {'success': True}
        mock_response = self.mock_response(200, json_data=expected_response)
        self.sonarqube_api._handle_response = MagicMock(return_value=expected_response)
        self.sonarqube_api._handle_response.side_effect = None
        self.sonarqube_api._handle_response.return_value = expected_response
        self.sonarqube_api._handle_response.assert_not_called()

        with unittest.mock.patch('requests.post', return_value=mock_response):
            response = self.sonarqube_api.delete_permission_template(template_name)

        self.sonarqube_api._handle_response.assert_called_once_with(mock_response)
        self.assertEqual(response, expected_response)

    def test_add_ad_group_to_template(self):
        template_name = 'my_template'
        group_name = 'my_ad_group'
        permission = 'admin'
        expected_response = {'success': True}
        mock_response = self.mock_response(200, json_data=expected_response)
        self.sonarqube_api._handle_response = MagicMock(return_value=expected_response)
        self.sonarqube_api._handle_response.side_effect = None
        self.sonarqube_api._handle_response.return_value = expected_response
        self.sonarqube_api._handle_response.assert_not_called()

        with unittest.mock.patch('requests.post', return_value=mock_response):
            response = self.sonarqube_api.add_ad_group_to_template(template_name, group_name, permission)

        self.sonarqube_api._handle_response.assert_called_once_with(mock_response)
        self.assertEqual(response, expected_response)

    def test_remove_ad_group_from_template(self):
        template_name = 'my_template'
        group_name = 'my_ad_group'
        permission = 'admin'
        expected_response = {'success': True}
        mock_response = self.mock_response(200, json_data=expected_response)
        self.sonarqube_api._handle_response = MagicMock(return_value=expected_response)
        self.sonarqube_api._handle_response.side_effect = None
        self.sonarqube_api._handle_response.return_value = expected_response
        self.sonarqube_api._handle_response.assert_not_called()

        with unittest.mock.patch('requests.post', return_value=mock_response):
            response = self.sonarqube_api.remove_ad_group_from_template(template_name, group_name, permission)

        self.sonarqube_api._handle_response.assert_called_once_with(mock_response)
        self.assertEqual(response, expected_response)

    def test_apply_permission_template_to_project(self):
        template_name = 'my_template'
        project_key = 'my_project_key'
        expected_response = {'success': True}
        mock_response = self.mock_response(200, json_data=expected_response)
        self.sonarqube_api._handle_response = MagicMock(return_value=expected_response)
        self.sonarqube_api._handle_response.side_effect = None
        self.sonarqube_api._handle_response.return_value = expected_response
        self.sonarqube_api._handle_response.assert_not_called()

        with unittest.mock.patch('requests.post', return_value=mock_response):
            response = self.sonarqube_api.apply_permission_template_to_project(template_name, project_key)

        self.sonarqube_api._handle_response.assert_called_once_with(mock_response)
        self.assertEqual(response, expected_response)

    def test_create_user_group(self):
        group_name = 'my_user_group'
        description = 'My User Group Description'
        expected_response = {'success': True}
        mock_response = self.mock_response(200, json_data=expected_response)
        self.sonarqube_api._handle_response = MagicMock(return_value=expected_response)
        self.sonarqube_api._handle_response.side_effect = None
        self.sonarqube_api._handle_response.return_value = expected_response
        self.sonarqube_api._handle_response.assert_not_called()

        with unittest.mock.patch('requests.post', return_value=mock_response):
            response = self.sonarqube_api.create_user_group(group_name, description)

        self.sonarqube_api._handle_response.assert_called_once_with(mock_response)
        self.assertEqual(response, expected_response)

    def test_delete_user_group(self):
        group_name = 'my_user_group'
        expected_response = {'success': True}
        mock_response = self.mock_response(200, json_data=expected_response)
        self.sonarqube_api._handle_response = MagicMock(return_value=expected_response)
        self.sonarqube_api._handle_response.side_effect = None
        self.sonarqube_api._handle_response.return_value = expected_response
        self.sonarqube_api._handle_response.assert_not_called()

        with unittest.mock.patch('requests.post', return_value=mock_response):
            response = self.sonarqube_api.delete_user_group(group_name)

        self.sonarqube_api._handle_response.assert_called_once_with(mock_response)
        self.assertEqual(response, expected_response)

    def test_get_projects_analyzed_before(self):
        days_ago = 30
        expected_response = {'projects': ['project1', 'project2']}
        mock_response = self.mock_response(200, json_data=expected_response)
        self.sonarqube_api._handle_response = MagicMock(return_value=expected_response)
        self.sonarqube_api._handle_response.side_effect = None
        self.sonarqube_api._handle_response.return_value = expected_response
        self.sonarqube_api._handle_response.assert_not_called()

        with unittest.mock.patch('requests.get', return_value=mock_response):
            response = self.sonarqube_api.get_projects_analyzed_before(days_ago)

        self.sonarqube_api._handle_response.assert_called_once_with(mock_response)
        self.assertEqual(response, expected_response)


    @patch('requests.get')
    def test_search_user_groups(self, mock_get):
        # Mocking a successful response
        response_data = [{'name': 'group1'}, {'name': 'group2'}]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = response_data

        # Creating SonarQubeAPI instance
        sonarqube_api = SonarQubeAPI(base_url='http://localhost:9999', token='fake_token')

        # Testing with a search query
        result = sonarqube_api.get_user_groups(q='test')
        mock_get.assert_called_once_with('http://localhost:9999/api/user_groups/search', params={'q': 'test'}, headers={'Authorization': 'Bearer fake_token'})
        self.assertEqual(result, response_data)

        # Testing without a search query
        result_without_query = sonarqube_api.get_user_groups()
        mock_get.assert_called_with('http://localhost:9999/api/user_groups/search', params={}, headers={'Authorization': 'Bearer fake_token'})
        self.assertEqual(result_without_query, response_data)

    @patch('requests.get')
    def test_search_user_groups_failure(self, mock_get):
        # Mocking a failed response
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = 'Not Found'

        # Creating SonarQubeAPI instance
        sonarqube_api = SonarQubeAPI(base_url='http://localhost:9999', token='fake_token')

        # Testing with a search query
        with self.assertRaises(SonarQubeAPIException) as context:
            sonarqube_api.get_user_groups(q='test')
        self.assertEqual(str(context.exception), 'SonarQube API request failed with status code 404: Not Found')
