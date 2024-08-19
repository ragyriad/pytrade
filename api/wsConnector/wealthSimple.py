from .requestor import APIRequestor
import cloudscraper
import json
from typing import Optional, Union
from requests.exceptions import HTTPError

class wealthSimple:
    """
    Wealthsimple Trade API wrapper

    Attributes
    ----------
    session : session
        A requests Session object to be associated with the class
    APIMainURL : str
        Main URL endpoint for API
    TradeAPI : APIRequester
        APIRequester object to handle API calls

    Methods
    -------
    login(email=None, password=None, two_factor_callback=None)
        Login to Wealthsimple Trade account
    get_accounts()
        Get Wealthsimple Trade accounts
    get_account_ids()
        Get Wealthsimple Trade account ids
    get_account(id)
        Get a Wealthsimple Trade account given an id
    get_account_history(id, time="all")
        Get Wealthsimple Trade account history
    get_activities()
        Get Wealthsimple Trade activities
    get_orders(symbol=None)
        Get Wealthsimple Trade orders 
    get_security(symbol)
        Get information about a security
    get_positions(id)
        Get positions
    get_person()
        Get Wealthsimple Trade person object
    get_me()
        Get Wealthsimple Trade user object
    get_bank_accounts():
        Get list of bank accounts tied to Wealthsimple Trade account
    get_deposits()
        Get list of deposits
    get_forex()
        Get foreign exchange rate
    """

    def __init__(self, email: str, password: str, refresh_token: str = None, mfa_code: str = None, two_factor_callback: callable = None):
        """
        Parameters
        ----------
        email : str
            Wealthsimple Trade login email
        password : str
            Wealthsimple Trade login password
        two_factor_callback: function
            Callback function that returns user input for 2FA code
        """
        self.session = cloudscraper.create_scraper()
        self.session.headers["Authorization"] = refresh_token
        self.APIMAIN = "https://trade-service.wealthsimple.com/"
        self.TradeAPI = APIRequestor(self.session, self.APIMAIN)
        if not refresh_token:
            self.login(email, password, mfa_code, two_factor_callback=two_factor_callback)

    def login(
        self,
        email: str = None,
        password: str = None,
        mfa_code: str = None,
        two_factor_callback: callable = None,
    ) -> None:
        # """Login to Wealthsimple Trade account

        # Parameters
        # ----------
        # email : str
        #     Wealthsimple Trade account email
        # password : str
        #     Wealthsimple Trade account password
        # two_factor_callback: function
        #     Callback function that returns user input for 2FA code

        # Returns
        # -------
        # None
        # """
        # if email and password:

        #     # Login credentials to pass in request
        #     data = [
        #         ("email", email),
        #         ("password", password),
        #     ]

        #     response = self.TradeAPI.makeRequest("POST", "auth/login", data)
        #     # Check if account requires 2FA
        #     if "x-wealthsimple-otp" in response.headers:
        #         if mfa_code == None and  two_factor_callback == None:
        #             raise Exception(
        #                 "This account requires 2FA. A 2FA callback function or MFA Code must be provided"
        #             )
        #         else:
        #             otp_value = None
        #             if mfa_code:
        #                 otp_value = mfa_code
        #             elif hasattr(two_factor_callback, '__call__') and mfa_code == None:
        #                 # Obtain 2FA code using callback function
        #                 otp_value = two_factor_callback()
        #                 # Add the 2FA code to the body of the login request
        #             else:
        #                 otp_value = two_factor_callback()
        #             data.append(("otp", otp_value))
        #             # Make a second login request using the 2FA code
        #             response = self.TradeAPI.makeRequest(
        #                 "POST", "auth/login", data)

        #     if response.status_code == 401:
        #         raise Exception("Invalid Login")

        #     # Update session headers with the API access token
        #     self.session.headers.update(
        #         {"Authorization": response.headers["X-Access-Token"]}
        #     )
        # else:
        #     raise Exception("Missing login credentials")
        """Login to Wealthsimple Trade account

        Parameters
        ----------
        email : str
            Wealthsimple Trade account email
        password : str
            Wealthsimple Trade account password
        two_factor_callback: callable
            Callback function that returns user input for 2FA code

        Returns
        -------
        dict
            A dictionary containing the status of the login attempt and any error messages
        """
        if not email or not password:
            return {"status": 400, "error": "Missing login credentials"}

        # Login credentials to pass in request
        data = [("email", email), ("password", password)]

        try:
            # Initial login request
            response = self.TradeAPI.makeRequest("POST", "auth/login", data)

            # Handle potential MFA requirement
            if "x-wealthsimple-otp" in response.headers:
                if not mfa_code and not two_factor_callback:
                    return {
                        "status": 403,
                        "error": "This account requires 2FA. Provide MFA code or a callback function.",
                    }

                otp_value = mfa_code or two_factor_callback()

                if not otp_value:
                    return {"status": 403, "error": "MFA code is required but not provided."}

                data.append(("otp", otp_value))
                response = self.TradeAPI.makeRequest("POST", "auth/login", data)

            # Check for invalid login
            if response.status_code == 401:
                return {"status": 401, "error": "Invalid login credentials."}

            # Raise any other potential HTTP errors
            response.raise_for_status()

            # Update session headers with the API access token
            self.session.headers.update({"Authorization": response.headers["X-Access-Token"]})

            return {"status": 200, "message": "Wealthsimple Login successful"}

        except HTTPError as http_err:
            # Handle HTTP errors explicitly
            return {"status": response.status_code, "error": str(http_err)}

        except Exception as err:
            # Handle general errors
            return {"status": 500, "error": str(err)}

    def get_accounts(self) -> list:
        """Get Wealthsimple Trade accounts

        Returns
        -------
        list
            A list of Wealthsimple Trade account dictionary objects
        """
        response = self.TradeAPI.makeRequest("GET", "account/list")
        response = response.json()
        response = response["results"]
        return response
    
    def get_security_groups(self,
        limit: int = 98,
        sec_id: Optional[str] = None) -> list:
        """Get Wealthsimple Trade accounts

        Returns
        -------
        list
            A list of Wealthsimple Trade account dictionary objects
        """

        callParams = {}
        
        if limit is not None:
            callParams["limit"] = limit
        if sec_id is not None:
            callParams["security_id"] = sec_id

        response = self.TradeAPI.makeRequest("GET", "security-groups", params=callParams)
        response = response.json()
        response = response["results"]
        return response

    def get_account_ids(self) -> list:
        """Get Wealthsimple Trade account ids

        Returns
        -------
        list
            A list of Wealthsimple Trade account ids
        """
        userAccounts = self.get_accounts()
        accountIDList = []
        for account in userAccounts:
            accountIDList.append(account["id"])
        return accountIDList

    def get_account(self, id: str) -> dict:
        """Get a Wealthsimple Trade account given an id

        Parameters
        ----------
        id : str
            Wealthsimple Trade account id

        Returns
        -------
        dict
            A dictionary containing the Wealthsimple Trade account
        """
        userAccounts = self.get_accounts()
        for account in userAccounts:
            if account["id"] == id:
                return account
        raise NameError(f"{id} does not correspond to any account")

    def get_account_history(self, id: str, time: str = "all") -> dict:
        """Get Wealthsimple Trade account history

        Parameters
        ----------
        id : str
            Wealthsimple Trade account id
        time : str
            String containing time interval for history

        Returns
        -------
        dict
            A dictionary containing the historical Trade account data
        """
        response = self.TradeAPI.makeRequest(
            "GET", f"account/history/{time}?account_id={id}"
        )
        response = response.json()
        if "error" in response:
            if response["error"] == "Record not found":
                raise NameError(f"{id} does not correspond to any account")

        return response

    def get_activities(
        self,
        tokens=None,
        limit: int = 99,
        type: Union[str, list] = "all",
        sec_id: Optional[str] = None,
        account_id: Union[str, list] = None,
    ) -> list:
        """Get Wealthsimple Trade activities
        
        Returns
        -------
        list
            A list of dictionaries containing Wealthsimple Trade activities
        """
        callParams = {}
        
        if not limit is None:
            callParams["limit"] = limit
        if not account_id is None:
            callParams["account_id"] = account_id
        if not type == "all":
            callParams["type"] = type
        if not sec_id is None:
            callParams["security_id"] = sec_id
        try:    
            response = self.TradeAPI.makeRequest("GET", "account/activities", params=callParams)
            response.raise_for_status()
            response_data = response.json()
            print("###Response Data###")
            print(response_data)
            return {"status": response.status_code, "data": response_data["results"]}
        except HTTPError as http_err:
            print("HTTP ERROR")
            return {"status": response.status_code, "error": str(http_err)}
        
        except Exception as error:
            print("OBJECT ERROR")
            print(error)
            return {"status": 500, "error": str(error)}


    def get_orders(self, symbol: str = None) -> list:
        """Get Wealthsimple Trade orders

        Parameters
        ----------
        symbol : str
            Symbol for security to filter orders on

        Returns
        -------
        list
            A list containing Wealthsimple Trade order dictionaries
        """
        response = self.TradeAPI.makeRequest("GET", "orders")
        response = response.json()
        # Check if order must be filtered:
        if symbol:
            filteredOrders = []
            for order in response["results"]:
                if order["symbol"] == symbol:
                    filteredOrders.append(order)
            return filteredOrders
        else:
            return response

    def get_security(self, id: str) -> dict:
        """Get information about a security

        Parameters
        ----------
        id : str
            Wealthsimple Security ID to search on

        Returns
        -------
        dict
            Dictionary containing information for security
        """

        response = self.TradeAPI.makeRequest("GET", f"securities/{id}")
        response = response.json()
        return response

    def get_securities_from_ticker(self, symbol: str) -> list:
        """Get information about a securitys with matching ticker symbols

        Parameters
        ----------
        symbol : str
            Symbol for security to search on

        Returns
        -------
        list
            A list containing matching securities
        """
        response = self.TradeAPI.makeRequest(
            "GET", f"securities?query={symbol}")
        response = response.json()
        return response["results"]

    def get_positions(self, id: str) -> list:
        """Get positions

        Parameters
        ----------
        id : str
            Wealthsimple Trade account id

        Returns
        -------
        list
            A list containing positions
        """
        response = self.TradeAPI.makeRequest(
            "GET", f"account/positions?account_id={id}"
        )
        response = response.json()
        return response["results"]

    def get_person(self) -> dict:
        """Get Wealthsimple Trade person object

        Returns
        -------
        dict
            A dictionary containing a person object
        """
        response = self.TradeAPI.makeRequest("GET", "person")
        return response.json()

    def get_me(self) -> dict:
        """Get Wealthsimple Trade user object

        Returns
        -------
        dict
            A dictionary containing a user object
        """
        response = self.TradeAPI.makeRequest("GET", "me")
        return response.json()

    def get_bank_accounts(self) -> list:
        """Get list of bank accounts tied to Wealthsimple Trade account

        Returns
        -------
        list
            A list of dictionaries containing bank account objects
        """
        response = self.TradeAPI.makeRequest("GET", "bank-accounts")
        response = response.json()
        return response["results"]

    def get_deposits(self) -> list:
        """Get list of deposits

        Returns
        -------
        list
            A list of dictionaries containing deposit objects
        """
        response = self.TradeAPI.makeRequest("GET", "deposits")
        response = response.json()
        return response["results"]

    def get_forex(self) -> dict:
        """Get foreign exchange rate

        Returns
        -------
        dict
            A dictionary containing foreign exchange rates
        """
        response = self.TradeAPI.makeRequest("GET", "forex")
        return response.json()