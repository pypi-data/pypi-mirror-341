"""
notifications.py

This module provides a `Notifications` class for sending structured messages and alerts
to external communication tools such as Microsoft Teams and Zenduty. It is used to
inform stakeholders or developers about system events, including errors and general logs.
"""

import json
import logging
import requests

from bw_essentials.notifications.teams_notification_schemas import get_notification_schema, get_error_schema

logger = logging.getLogger(__name__)


class Notifications:
    """
    Notification module to send alerts and warnings via Microsoft Teams and Zenduty.

    Args:
        title (str): The title or service name triggering the notification.
        summary (str, optional): A brief summary of the message or error.
        message (str, optional): The main body of the message.
        webhook_url (str, optional): Teams webhook URL to send the notification.
        zenduty_url (str, optional): Zenduty endpoint to create incidents.
        alert (bool, optional): If True, it's treated as an error; otherwise as a log. Defaults to False.
        trace (str, optional): Optional traceback or detailed error string.
        request_id (str, optional): Optional correlation ID for tracing logs.
        notify_teams (bool, optional): Whether to send notification to Teams. Defaults to True.
        notify_calls (bool, optional): Whether to send alert to Zenduty. Defaults to False.
        api_timeout (int, optional): Timeout in seconds for external API requests. Defaults to 5.
    """

    def __init__(self, title, summary=None, message=None, webhook_url=None, zenduty_url=None, alert=False, trace=None,
                 request_id=None, notify_teams=True, notify_calls=False, api_timeout=5):
        self.message = message
        self.title = title
        self.summary = summary
        self.alert = alert
        self.trace = trace
        self.request_id = request_id
        self.notify_on_teams = notify_teams
        self.notify_on_calls = notify_calls
        self.webhook_url = webhook_url
        self.zenduty_url = zenduty_url
        self.api_timeout = api_timeout

    def __notify_teams_workflow(self):
        """
        Sends a notification to Microsoft Teams using Adaptive Cards.

        Uses either the error schema or the log schema based on whether the notification
        is an alert or not. This function posts the generated card payload to the configured
        Teams webhook URL.

        Returns:
            None
        """
        logger.info("In __notify_teams_workflow")
        try:
            if self.notify_on_teams:
                workflow_schema = get_notification_schema(self.title, self.message)
                if self.alert:
                    workflow_schema = get_error_schema(
                        service_url=self.title,
                        message=self.message,
                        summary=self.summary,
                        error_trace=self.trace,
                        request_id=self.request_id
                    )

                headers = {'Content-Type': 'application/json'}
                response = requests.post(
                    self.webhook_url,
                    data=json.dumps(workflow_schema),
                    headers=headers
                )
                logger.info(f"{response =}")
            else:
                logger.info(f"Notification for teams is {self.notify_on_teams}. Message: {self.message}")
        except Exception as exc:
            logger.info("Error while notifying error to teams.")
            logger.exception(exc)

    def __notify_zenduty(self):
        """
        Sends a critical alert to Zenduty via its API endpoint.

        Posts a payload including alert type, message, and summary. Primarily used for error alerts.

        Returns:
            None
        """
        if self.notify_on_calls:
            payload = {
                "alert_type": "critical",
                "message": self.message,
                "summary": self.summary
            }
            payload_json = json.dumps(payload)
            response = requests.post(
                self.zenduty_url,
                data=payload_json,
                timeout=float(self.api_timeout)
            )
            logger.info(response)
            logger.info("Response from Zenduty Call API: An incident has been created")

    def notify_message(self, message=None, summary=None, alert=False):
        """
        Sends a general log or information notification.

        Args:
            message (str, optional): The content of the message. Overrides initial message if provided.
            summary (str, optional): Optional summary for the message.
            alert (bool, optional): If True, message is sent as an alert.

        Returns:
            None
        """
        try:
            self.alert = alert
            if message:
                self.message = message
            if summary:
                self.summary = summary
            self.__notify_teams_workflow()
        except Exception as exc:
            logger.info("Error while notifying message to teams")
            logger.exception(exc)

    def notify_error(self, message=None, summary=None, alert=True, trace=None, request_id=None):
        """
        Sends an error notification to Microsoft Teams and Zenduty.

        Args:
            message (str, optional): Error message to be sent.
            summary (str, optional): Summary or context for the error.
            alert (bool, optional): Flag to indicate it's an error. Defaults to True.
            trace (str, optional): Detailed traceback or stack trace of the error.
            request_id (str, optional): Optional request ID for tracking.

        Returns:
            None
        """
        self.alert = alert
        if summary:
            self.summary = summary
        if message:
            self.message = message
        if trace:
            self.trace = trace
        if request_id:
            self.request_id = request_id
        self.__notify_zenduty()
        self.__notify_teams_workflow()
