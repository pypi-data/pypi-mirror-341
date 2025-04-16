
import logging
import httpx
from y360_orglib.audit.models import MailEventsPage
from y360_orglib.common.exceptions import APIError, MailAuditError
from y360_orglib.common.http import make_request
from y360_orglib.logging.config import configure_logger


class AuditMail():
    __url = 'https://api360.yandex.net/security/v1/org/'
    __per_page = 100
    
    def __init__(self, api_key: str, org_id: str, ssl_verify=True, log_level=logging.INFO):
        self._api_key = api_key
        self._org_id = org_id
        self.log = configure_logger(logger_name=__name__, level=log_level)
        self.session = httpx.Client(verify=ssl_verify)
        self._headers = {
            "Authorization": f"OAuth {api_key}",
            "content-type": "application/json",
        }
        self.session.headers.update(self._headers)

        
    def get_logs_page(self, page: int, per_page: int = 10, page_token: str = '') -> MailEventsPage:
        """
        Get a page of mail audit log events.

        Args:
            page (int): The page number.
            per_page (int, optional): The number of events per page. Defaults to 10.
            page_token (str, optional): The page token. Defaults to ''.

        Returns:
            MailEventsPage: The page of MailEvent events.
        """
        

        if len(page_token) == 0:
            page_token = f'{page * per_page - per_page}'


        path = f'{self.__url}{self._org_id}/audit_log/mail?pageSize={per_page}&pageToken={page_token}'

        try:
            response_json = response_json = make_request(session=self.session, url=path, method='GET')
            return MailEventsPage(**response_json)
        except APIError as e:
            self.log.error(f"Error getting events page: {e}")
            raise MailAuditError(e)
    

