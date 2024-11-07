import re
from locustio.common_utils import init_logger, confluence_measure, run_as_specific_user  # noqa F401

logger = init_logger(app_type='confluence')


@confluence_measure("locust_app_specific_action")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    r = locust.get('/rest/api/content?title=SourceEditor1', catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')   # decode response content

    id_pattern_example = '"id":"(.+?)"'
    id = re.findall(id_pattern_example, content)    # get ID from response using regexp

    logger.info(f'page id: {id}')  # log info for debug when verbose is true in confluence.yml file
    if '"id":' not in content:
        logger.error(f"'id' was not found in {content}")
    assert '"id":' in content  # assert specific string in response content

    # Test API: POST toStorageFormat
    expected_format = "<p>toStorageFormat</p>"
    data = {"pageId": id, "editorFormat": expected_format}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = locust.post('/rest/sourceeditor/1.0/convert/toStorageFormat', data=data, headers=headers, catch_response=True)  # call app-specific POST endpoint
    content = r.content.decode('utf-8')
    if expected_format not in content:
        logger.error(f"'{expected_format}' was not found in {content}")
    assert expected_format in content  # assertion after POST request

    # Test API: POST toEditorFormat
    expected_format = "<div>toEditorFormat</div>"
    data = {"pageId": id, "storageFormat": expected_format}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = locust.post('/rest/sourceeditor/1.0/convert/toEditorFormat', data=data, headers=headers, catch_response=True)  # call app-specific POST endpoint
    content = r.content.decode('utf-8')
    if expected_format not in content:
        logger.error(f"'{expected_format}' was not found in {content}")
    assert expected_format in content  # assertion after POST request
