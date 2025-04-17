"""
Client API for Payler payment system.
"""

import json
from dataclasses import asdict
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from payler_sdk.exceptions import (
    PaylerApiError,
    PaylerSessionError,
    handle_payler_error_code,
)
from payler_sdk.models import (
    PaylerCustomerCardListResponse,
    PaylerCustomerUpdateOrCreateRequest,
    PaylerCustomerUpdateOrCreateResponse,
    PaylerPaymentResponse,
    PaylerPaymentStatusResponse,
    PaylerTemplateRequest,
    PaylerTemplateResponse,
    RemoveSavedCardResponse,
    StartSaveCardSessionResponse,
    PaylerGetStatusSaveCardRequest,
    PaylerGetStatusSaveCardResponse
)
from payler_sdk.utils import format_amount_for_payler


class PaylerEndpoints(Enum):
    """Enum containing all Payler API endpoints."""

    START_SAVE_CARD_SESSION = "gapi/StartSaveCardSession"
    SAVE_CARD = "gapi/Save"
    GET_CARD_LIST = "gapi/GetCardList"
    REMOVE_CARD = "gapi/RemoveCard"
    CUSTOMER_REGISTER = "gapi/CustomerRegister"
    REPEAT_PAY = "gapi/RepeatPay"
    GET_STATUS = "gapi/GetStatus"
    GET_TEMPLATE = "gapi/GetTemplate"
    GET_STATUS_SAVE_CARD = "gapi/GetStatusSaveCard"


class PaylerClient:
    """
    Client for working with Payler API.

    Args:
        base_url: Base URL for Payler API
        auth_key: Authorization key
    """

    HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    def __init__(
        self,
        base_url: str,
        auth_key: str,
        timeout: Optional[float] = None,
    ):
        """
        Initialize Payler client.

        Args:
            base_url: Base URL for Payler API
            auth_key: Authorization key
        """
        self.base_url = base_url
        self.auth_key = auth_key
        self.timeout = timeout
        self.session = requests.Session()

    def close(self) -> None:
        """Close HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _make_post_request(
        self,
        route_path: str,
        data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """
        Make POST request to Payler API.

        Args:
            route_path: Path to API method
            data: Data to send
            headers: Additional headers

        Returns:
            Response from API

        Raises:
            PaylerApiError: If request is not successful
        """
        url = urljoin(self.base_url, route_path)
        request_headers = self.HEADERS.copy()

        if headers:
            request_headers.update(headers)

        try:
            response = self.session.post(
                url,
                data=data,
                headers=request_headers,
                timeout=self.timeout,
            )
            response.raise_for_status()

        except requests.HTTPError as e:
            try:
                error_data = json.loads(e.response.text)
                error_code = error_data.get("error", {}).get("code")
                error_message = error_data.get("error", {}).get("message")

                exception = handle_payler_error_code(
                    error_code,
                    error_message,
                    response=e.response
                )

                raise exception
            except json.JSONDecodeError:
                raise PaylerApiError(
                    f"Invalid response: {str(e)}",
                    status_code=e.response.status_code
                    if hasattr(e, 'response') else None
                )
            except Exception as ex:
                if isinstance(ex, PaylerApiError):
                    raise
                raise PaylerApiError(f"Unexpected error: {str(ex)}")

        return response

    def initialize_save_card_session(
        self,
        customer_id: str,
        currency: str,
        template: Optional[str] = None,
        lang: str = "ru",
        pay_page_params: Optional[Dict[str, str]] = None,
        lifetime: Optional[int] = None,
        return_url_success: Optional[str] = None,
    ) -> StartSaveCardSessionResponse:
        """
        Initialize save card session.

        Args:
            customer_id: Customer ID
            template: Used payment page template
            lang: Preferred payment page language (en/ru)
            currency: Payment currency
            pay_page_params: Parameters for payment page display
            lifetime: Session lifetime in minutes
            return_url_success: URL for redirect after card saving
        Returns:
            StartSaveCardSessionResponse

        Raises:
            PaylerSessionError: If session is not created
        """

        # Form data for request
        session_data = {
            "key": self.auth_key,
            "customer_id": customer_id,
            "currency": currency,
        }

        # Add optional parameters
        if template:
            session_data["template"] = template
        if lang:
            session_data["lang"] = lang
        if lifetime:
            session_data["lifetime"] = lifetime
        if return_url_success:
            session_data["return_url_success"] = return_url_success

        # Add payment page parameters
        if pay_page_params:
            for key, value in pay_page_params.items():
                session_data[f"pay_page_param_{key}"] = value

        try:
            response = self._make_post_request(
                PaylerEndpoints.START_SAVE_CARD_SESSION.value,
                data=session_data,
                headers=self.HEADERS,
            )
            response_data = response.json()

            session_id = response_data.get("session_id")
            order_id = response_data.get("order_id")
            if not session_id:
                raise PaylerSessionError(
                    "Failed to get session_id from Payler response"
                )

            return StartSaveCardSessionResponse(
                session_id=session_id,
                order_id=order_id,
                save_card_url=(
                    f"{self.base_url}/"
                    f"{PaylerEndpoints.SAVE_CARD.value}"
                    f"?session_id={session_id}"
                ),
            )
        except Exception as e:
            if isinstance(e, PaylerApiError):
                raise
            raise PaylerApiError(
                f"Error initializing save card session: {str(e)}"
            )

    def fetch_customer_cards(
        self,
        customer_id: str,
    ) -> PaylerCustomerCardListResponse:
        """
        Get list of saved customer cards.

        Args:
            customer_id: Customer ID in merchant system

        Returns:
            List of saved customer cards

        Raises:
            PaylerApiError: If there is an error in Payler API
        """
        try:
            response = self._make_post_request(
                PaylerEndpoints.GET_CARD_LIST.value,
                data={
                    "key": self.auth_key,
                    "customer_id": customer_id,
                },
                headers=self.HEADERS,
            )

            return PaylerCustomerCardListResponse(**response.json())
        except Exception as e:
            if isinstance(e, PaylerApiError):
                raise
            error_message = f"Error getting customer cards: {str(e)}"
            raise PaylerApiError(error_message)

    def remove_saved_card(self, card_id: str) -> RemoveSavedCardResponse:
        """
        Delete saved customer card.

        Args:
            card_id: Card ID in Payler system

        Returns:
            Information about changes (literal True or False)

        Raises:
            PaylerApiError: If there is an error in Payler API
        """
        try:
            data = {
                "key": self.auth_key,
                "card_id": card_id,
            }

            response = self._make_post_request(
                PaylerEndpoints.REMOVE_CARD.value,
                data=data,
                headers=self.HEADERS,
            )

            response_data = response.json()

            return RemoveSavedCardResponse(
                changed=bool(response_data.get("changed", False)),
            )
        except Exception as e:
            if isinstance(e, PaylerApiError):
                raise
            error_message = f"Error deleting card: {str(e)}"
            raise PaylerApiError(error_message)

    def register_new_customer(
        self,
        customer: PaylerCustomerUpdateOrCreateRequest,
    ) -> PaylerCustomerUpdateOrCreateResponse:
        """
        Register new customer in Payler system.

        Args:
            **kwargs: Additional parameters for registration

        Returns:
            Information about created customer

        Raises:
            PaylerApiError: If there is an error in Payler API
        """
        try:
            data = {
                "key": self.auth_key,
                **customer.to_dict(),
            }

            response = self._make_post_request(
                PaylerEndpoints.CUSTOMER_REGISTER.value,
                data=data,
                headers=self.HEADERS,
            )

            return PaylerCustomerUpdateOrCreateResponse(**response.json())
        except Exception as e:
            if isinstance(e, PaylerApiError):
                raise
            error_message = f"Error registering customer: {str(e)}"
            raise PaylerApiError(error_message)

    def charge_saved_card(
        self,
        amount: Decimal,
        order_id: str,
        currency: str,
        recurrent_template_id: str,
    ) -> PaylerPaymentResponse:
        """
        Charge funds from saved customer card.

        Args:
            amount: Amount to charge
            order_id: Unique ID of new payment
            recurrent_template_id: ID of recurrent payment template,
                received when card is saved
            currency: Payment currency

        Returns:
            Information about charge

        Raises:
            PaylerApiError: If there is an error in Payler API
        """
        try:
            data = {
                "key": self.auth_key,
                "order_id": order_id,
                "amount": format_amount_for_payler(amount),
                "recurrent_template_id": recurrent_template_id,
                "currency": currency,
            }

            response = self._make_post_request(
                PaylerEndpoints.REPEAT_PAY.value,
                data=data,
                headers=self.HEADERS,
            )

            response_data = response.json()

            return PaylerPaymentResponse(
                order_id=order_id,
                status=response_data.get("status", "Unknown"),
                amount=amount,
            )
        except Exception as e:
            if isinstance(e, PaylerApiError):
                raise
            error_message = f"Error charging saved card: {str(e)}"
            raise PaylerApiError(error_message)

    def get_payment_status(self, order_id: str) -> PaylerPaymentStatusResponse:
        """
        Get payment status.

        Args:
            order_id: Unique ID of payment

        Returns:
            Payment status
        """
        try:
            data = {
                "key": self.auth_key,
                "order_id": order_id,
            }

            response = self._make_post_request(
                PaylerEndpoints.GET_STATUS.value,
                data=data,
                headers=self.HEADERS,
            )

            return PaylerPaymentStatusResponse(**response.json())
        except Exception as e:
            if isinstance(e, PaylerApiError):
                raise
            error_message = f"Error getting payment status: {str(e)}"
            raise PaylerApiError(error_message)

    def get_template(
        self,
        data: PaylerTemplateRequest,
    ) -> PaylerTemplateResponse:
        """
        Get recurrent payment template.
        Args:
            data: Recurrent payment template request
        Returns:
            Recurrent payment template response
        Raises:
            PaylerApiError: If there is an error in Payler API
        """
        try:
            response = self._make_post_request(
                PaylerEndpoints.GET_TEMPLATE.value,
                data={
                    "key": self.auth_key,
                    **asdict(data)
                },
                headers=self.HEADERS,
            )

            return PaylerTemplateResponse(**response.json())
        except Exception as e:
            if isinstance(e, PaylerApiError):
                raise
            error_message = f"Error getting template: {str(e)}"
            raise PaylerApiError(error_message)

    def get_status_save_card(
        self,
        data: PaylerGetStatusSaveCardRequest,
    ) -> PaylerGetStatusSaveCardResponse:
        """
        Get status of save card.

        Args:
            data: PaylerGetStatusSaveCardRequest

        Returns:
            PaylerGetStatusSaveCardResponse
        Raises:
            PaylerApiError: If there is an error in Payler API
        """
        try:
            response = self._make_post_request(
                PaylerEndpoints.GET_STATUS_SAVE_CARD.value,
                data={
                    "key": self.auth_key,
                    **asdict(data)
                },
                headers=self.HEADERS,
            )

            return PaylerGetStatusSaveCardResponse(**response.json())
        except Exception as e:
            if isinstance(e, PaylerApiError):
                raise
            error_message = f"Error getting status of save card: {str(e)}"
            raise PaylerApiError(error_message)
