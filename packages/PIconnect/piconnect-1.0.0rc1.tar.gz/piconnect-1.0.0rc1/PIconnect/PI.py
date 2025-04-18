"""PI - Core containers for connections to PI databases."""

import enum
import warnings
from typing import Any, cast

import PIconnect._typing.AF as _AFtyping
from PIconnect import Data, Time, dotnet

__all__ = ["PIServer", "PIPoint"]


class InitialisationWarning(UserWarning):
    pass


class AuthenticationMode(enum.IntEnum):
    """AuthenticationMode indicates how a user authenticates to a PI Server.

    Detailed information is available at
    :afsdk:`AF.PI.PIAuthenticationMode <T_OSIsoft_AF_PI_PIAuthenticationMode.htm>`.
    """

    #: Use Windows authentication when making a connection
    WINDOWS_AUTHENTICATION = 0
    #: Use the PI User authentication mode when making a connection
    PI_USER_AUTHENTICATION = 1


_DEFAULT_AUTH_MODE = AuthenticationMode.PI_USER_AUTHENTICATION


def _lookup_servers() -> dict[str, dotnet.AF.PI.PIServer]:
    servers: dict[str, dotnet.AF.PI.PIServer] = {}

    for server in dotnet.lib.AF.PI.PIServers():
        try:
            servers[server.Name] = server
        except ImportError as e:
            raise e
        except (Exception, dotnet.lib.System.Exception) as e:  # type: ignore
            warnings.warn(
                f"Failed loading server data for {server.Name} "
                f"with error {type(cast(Exception, e)).__qualname__}",
                InitialisationWarning,
                stacklevel=2,
            )
    return servers


def _lookup_default_server() -> dotnet.AF.PI.PIServer | None:
    default_server = None
    try:
        default_server = dotnet.lib.AF.PI.PIServers().DefaultPIServer
    except ImportError as e:
        raise e
    except Exception:
        warnings.warn("Could not load the default PI Server", ResourceWarning, stacklevel=2)
    return default_server


class PIPoint(Data.DataContainer):
    """Reference to a PI Point to get data and corresponding metadata from the server.

    Parameters
    ----------
    pi_point : :afsdk:`AF.PI.PIPoint <T_OSIsoft_AF_PI_PIPoint.htm>`
        Reference to a PIPoint as returned by the SDK
    """

    version = "0.3.0"

    def __init__(self, pi_point: dotnet.AF.PI.PIPoint) -> None:
        super().__init__()
        self.pi_point = pi_point
        self.tag = pi_point.Name
        self.__attributes_loaded = False
        self.__raw_attributes = {}

    def __repr__(self):
        """Return the string representation of the PI Point."""
        return (
            f"{self.__class__.__qualname__}({self.tag}, {self.description}; "
            f"Current Value: {self.current_value} {self.units_of_measurement})"
        )

    @property
    def created(self):
        """Return the creation datetime of a point."""
        return Time.timestamp_to_index(self.raw_attributes["creationdate"])

    @property
    def description(self):
        """Return the description of the PI Point.

        .. todo::

            Add setter to alter displayed description
        """
        return self.raw_attributes["descriptor"]

    @property
    def last_update(self):
        """Return the time at which the last value for this PI Point was recorded."""
        return Time.timestamp_to_index(self.pi_point.CurrentValue().Timestamp.UtcTime)

    @property
    def name(self) -> str:
        """Return the name of the PI Point."""
        return self.tag

    @property
    def raw_attributes(self) -> dict[str, Any]:
        """Return a dictionary of the raw attributes of the PI Point."""
        self.__load_attributes()
        return self.__raw_attributes

    @property
    def units_of_measurement(self) -> str | None:
        """Return the units of measument in which values for this PI Point are reported."""
        return self.raw_attributes["engunits"]

    @property
    def stepped_data(self) -> bool:
        """Return False when the PIPoint contains continuous data or True when stepped data."""
        return self.pi_point.Step

    def __load_attributes(self) -> None:
        """Load the raw attributes of the PI Point from the server."""
        if not self.__attributes_loaded:
            self.pi_point.LoadAttributes([])
            self.__attributes_loaded = True
        self.__raw_attributes = {att.Key: att.Value for att in self.pi_point.GetAttributes([])}

    def _current_value(self) -> Any:
        """Return the last recorded value for this PI Point (internal use only)."""
        return self.pi_point.CurrentValue().Value

    def _filtered_summaries(
        self,
        time_range: dotnet.AF.Time.AFTimeRange,
        interval: dotnet.AF.Time.AFTimeSpan,
        filter_expression: str,
        summary_types: dotnet.AF.Data.AFSummaryTypes,
        calculation_basis: dotnet.AF.Data.AFCalculationBasis,
        filter_evaluation: dotnet.AF.Data.AFSampleType,
        filter_interval: dotnet.AF.Time.AFTimeSpan,
        time_type: dotnet.AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummariesDict:
        return self.pi_point.FilteredSummaries(
            time_range,
            interval,
            filter_expression,
            summary_types,
            calculation_basis,
            filter_evaluation,
            filter_interval,
            time_type,
        )

    def _interpolated_value(self, time: dotnet.AF.Time.AFTime) -> dotnet.AF.Asset.AFValue:
        """Return a single value for this PI Point."""
        return self.pi_point.InterpolatedValue(time)

    def _interpolated_values(
        self,
        time_range: dotnet.AF.Time.AFTimeRange,
        interval: dotnet.AF.Time.AFTimeSpan,
        filter_expression: str,
    ) -> dotnet.AF.Asset.AFValues:
        include_filtered_values = False
        return self.pi_point.InterpolatedValues(
            time_range, interval, filter_expression, include_filtered_values
        )

    def _normalize_filter_expression(self, filter_expression: str) -> str:
        return filter_expression.replace("%tag%", self.tag)

    def _recorded_value(
        self, time: dotnet.AF.Time.AFTime, retrieval_mode: dotnet.AF.Data.AFRetrievalMode
    ) -> dotnet.AF.Asset.AFValue:
        """Return a single recorded value for this PI Point."""
        return self.pi_point.RecordedValue(
            time, dotnet.lib.AF.Data.AFRetrievalMode(int(retrieval_mode))
        )

    def _recorded_values(
        self,
        time_range: dotnet.AF.Time.AFTimeRange,
        boundary_type: dotnet.AF.Data.AFBoundaryType,
        filter_expression: str,
    ) -> dotnet.AF.Asset.AFValues:
        include_filtered_values = False
        return self.pi_point.RecordedValues(
            time_range, boundary_type, filter_expression, include_filtered_values
        )

    def _summary(
        self,
        time_range: dotnet.AF.Time.AFTimeRange,
        summary_types: dotnet.AF.Data.AFSummaryTypes,
        calculation_basis: dotnet.AF.Data.AFCalculationBasis,
        time_type: dotnet.AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummaryDict:
        return self.pi_point.Summary(time_range, summary_types, calculation_basis, time_type)

    def _summaries(
        self,
        time_range: dotnet.AF.Time.AFTimeRange,
        interval: dotnet.AF.Time.AFTimeSpan,
        summary_types: dotnet.AF.Data.AFSummaryTypes,
        calculation_basis: dotnet.AF.Data.AFCalculationBasis,
        time_type: dotnet.AF.Data.AFTimestampCalculation,
    ) -> _AFtyping.Data.SummariesDict:
        return self.pi_point.Summaries(
            time_range, interval, summary_types, calculation_basis, time_type
        )

    def _update_value(
        self,
        value: dotnet.AF.Asset.AFValue,
        update_mode: dotnet.AF.Data.AFUpdateOption,
        buffer_mode: dotnet.AF.Data.AFBufferOption,
    ) -> None:
        return self.pi_point.UpdateValue(value, update_mode, buffer_mode)


class PIServer:
    """PIServer is a connection to an OSIsoft PI Server.

    Parameters
    ----------
    server : str, optional
        Name of the server to connect to, defaults to None
    username : str, optional
        Username to connect to the server, defaults to None
    password : str, optional
        Password for the username, defaults to None
    domain : str, optional
        Domain of the username, defaults to None
    authentication_mode : AuthenticationMode, optional
        Authentication mode to use, defaults to PI_USER_AUTHENTICATION
    timeout : int, optional
        the maximum seconds an operation can take


    .. note::
        If the specified `server` is unknown a warning is thrown and the connection
        is redirected to the default server, as if no server was passed. The list
        of known servers is available in the `PIServer.servers` dictionary.
    """

    _servers: dict[str, dotnet.AF.PI.PIServer] | None = None
    _default_server: dotnet.AF.PI.PIServer | None = None

    @classmethod
    def servers(cls) -> dict[str, dotnet.AF.PI.PIServer]:
        """Return a dictionary of the known servers."""
        if cls._servers is None:
            cls._servers = _lookup_servers()
        return cls._servers

    @classmethod
    def default_server(cls) -> dotnet.AF.PI.PIServer | None:
        """Return the default server."""
        if cls._default_server is None:
            cls._default_server = _lookup_default_server()
        return cls._default_server

    def __init__(
        self,
        server: str | None = None,
        username: str | None = None,
        password: str | None = None,
        domain: str | None = None,
        authentication_mode: AuthenticationMode = _DEFAULT_AUTH_MODE,
        timeout: int | None = None,
    ) -> None:
        default_server = self.default_server()
        if server is None:
            if default_server is None:
                raise ValueError("No server was specified and no default server was found.")
            self.connection = default_server
        else:
            if (_server := dotnet.lib.AF.PI.PIServers()[server]) is not None:
                self.connection = _server
            else:
                if default_server is None:
                    raise ValueError(
                        f"Server '{server}' not found and no default server was found."
                    ) from None
                message = 'Server "{server}" not found, using the default server.'
                warnings.warn(
                    message=message.format(server=server), category=UserWarning, stacklevel=1
                )
                self.connection = default_server

        if bool(username) != bool(password):
            raise ValueError(
                "When passing credentials both the username and password must be specified."
            )
        if domain and not username:
            raise ValueError(
                "A domain can only specified together with a username and password."
            )
        if username:
            secure_pass = dotnet.lib.System.Security.SecureString()
            if password is not None:
                for c in password:
                    secure_pass.AppendChar(c)
            cred = (username, secure_pass) + ((domain,) if domain else ())
            self._credentials = (
                dotnet.lib.System.Net.NetworkCredential(cred[0], cred[1], *cred[2:]),
                dotnet.lib.AF.PI.PIAuthenticationMode(int(authentication_mode)),
            )
        else:
            self._credentials = None

        if timeout:
            # System.TimeSpan(hours, minutes, seconds)
            self.connection.ConnectionInfo.OperationTimeOut = dotnet.lib.System.TimeSpan(
                0, 0, timeout
            )

    def __enter__(self):
        """Open connection context with the PI Server."""
        if self._credentials:
            self.connection.Connect(*self._credentials)
        else:
            # Don't force to retry connecting if previous attempt failed
            force_connection = False
            self.connection.Connect(force_connection)
        return self

    def __exit__(self, *args: Any):
        """Close connection context with the PI Server."""
        self.connection.Disconnect()

    def __repr__(self) -> str:
        """Representation of the PIServer object."""
        return f"{self.__class__.__qualname__}(\\\\{self.server_name})"

    @property
    def server_name(self):
        """Name of the connected server."""
        return self.connection.Name

    def search(
        self, query: str | list[str], source: str | None = None
    ) -> Data.DataContainerCollection[PIPoint]:
        """Search PIPoints on the PIServer.

        Parameters
        ----------
        query : str or [str]
            String or list of strings with queries
        source : str, optional
            Defaults to None. Point source to limit the results

        Returns
        -------
        Data.DataContainerCollection[PIPoint]
            A collection of :class:`PIPoint` objects as a result of the query.


        .. todo::

            Reject searches while not connected
        """
        if isinstance(query, list):
            return Data.DataContainerCollection(
                [y for x in query for y in self.search(x, source)]
            )
        return Data.DataContainerCollection(
            [
                PIPoint(pi_point)
                for pi_point in dotnet.lib.AF.PI.PIPoint.FindPIPoints(
                    self.connection, str(query), source, None
                )
            ]
        )
