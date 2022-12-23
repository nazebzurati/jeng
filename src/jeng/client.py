import requests
import urllib3
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client, proxy, xsd
from zeep.transports import Transport

# disabling urllib warnings
urllib3.disable_warnings()


# exception
class JengClientNoneException(AttributeError):
    def __init__(self):
        super().__init__("Client is None. Probably client not yet connected / disconnected.")


# witsml client
class WitsmlClient:
    "A WITSML client that handles WITSML authentication and communication."

    def __init__(self):
        self.__client = None
        self.__session = Session()

    def __test(self):
        try:
            return (
                self.__client.service.WMLS_GetBaseMsg(
                    ReturnValueIn=1,
                )
            ).strip() == "Function completed successfully"
        except Exception:
            return False

    def connect(
        self,
        url: str,
        username: str,
        password: str,
    ) -> bool:
        """
        Connect to WITSML Server.

        Parameters
        ----------
        url : str
            WSDL from a WITSML Store web service URL (usually ends with '?wsdl')
        username : str
            Username for user authentication
        password : str
            Password for user authentication

        Returns
        -------
        bool
            Status of the connection (True is OK)
        """
        self.__session.auth = HTTPBasicAuth(username, password)
        try:
            self.__client = Client(url, transport=Transport(session=self.__session))
        except requests.exceptions.SSLError:
            self.__session.verify = False
            self.__client = Client(url, transport=Transport(session=self.__session))
        except Exception:
            return False
        return self.__test()

    def service(self) -> proxy.ServiceProxy:
        """
        Get connected client's service for non-common API function call and custom operation.

        Returns
        -------
        zeep.proxy.ServiceProxy
            Service proxy for calling API functions
        """
        return self.__client.service

    def get_from_store(
        self,
        wml_type_in: str,
        xml_in: str,
        return_element: str,
    ):
        """
        WMLS_GetFromStore wrapper.

        Parameters
        ----------
        wml_type_in : str
            WITSML data-object type (see the specific WITSML data schema for the objectType).
        xml_in : str
            A query template that specifies the data-object to be returned.
        return_element : str
            Indicates which elements and attributes are requested to be returned in addition to data-object selection items.

        Returns
        -------
        Any
            API call reply
        """
        try:
            return self.__client.service.WMLS_GetFromStore(
                WMLtypeIn=wml_type_in,
                QueryIn=xml_in,
                OptionsIn=f"returnElements={return_element}",
                CapabilitiesIn=xsd.SkipValue,
            )
        except AttributeError:
            raise JengClientNoneException

    def add_to_store(
        self,
        wml_type_in: str,
        xml_in: str,
    ):
        """
        WMLS_AddToStore wrapper.

        Parameters
        ----------
        wml_type_in : str
            WITSML data-object type (see the specific WITSML data schema for the objectType).
        xml_in : str
            A query template that specifies WITSML data-object to be added.

        Returns
        -------
        Any
            API call reply
        """
        try:
            return self.__client.service.WMLS_AddToStore(
                WMLtypeIn=wml_type_in,
                XMLin=xml_in,
                OptionsIn=xsd.SkipValue,
                CapabilitiesIn=xsd.SkipValue,
            )
        except AttributeError:
            raise JengClientNoneException

    def update_in_store(
        self,
        wml_type_in,
        xml_in,
    ):
        """
        WMLS_UpdateInStore wrapper.

        Parameters
        ----------
        wml_type_in : str
            WITSML data-object type (see the specific WITSML data schema for the objectType).
        xml_in : str
            A query template that specifies WITSML data-object to be updated.

        Returns
        -------
        Any
            API call reply.
        """
        try:
            return self.__client.service.WMLS_UpdateInStore(
                WMLtypeIn=wml_type_in,
                XMLin=xml_in,
                OptionsIn=xsd.SkipValue,
                CapabilitiesIn=xsd.SkipValue,
            )
        except AttributeError:
            raise JengClientNoneException

    def delete_from_store(
        self,
        wml_type_in,
        xml_in,
    ):
        """
        WMLS_DeleteFromStore wrapper.

        Parameters
        ----------
        wml_type_in : str
            WITSML data-object type (see the specific WITSML data schema for the objectType).
        xml_in : str
            A query template that specifies WITSML data-object to be deleted.

        Returns
        -------
        Any
            API call reply.
        """
        try:
            return self.__client.service.WMLS_DeleteFromStore(
                WMLtypeIn=wml_type_in,
                QueryIn=xml_in,
                OptionsIn=xsd.SkipValue,
                CapabilitiesIn=xsd.SkipValue,
            )
        except AttributeError:
            raise JengClientNoneException
