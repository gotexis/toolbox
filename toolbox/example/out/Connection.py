

from .OpenViduRole import OpenViduRole
from .Publisher import Publisher

"""
See [[Session.activeConnections]]
"""
class Connection:

    """
    Identifier of the connection. You can call [[Session.forceDisconnect]] passing self property as parameter
    """
    connectionId: str

    """
    Timestamp when self connection was established, in UTC milliseconds (ms since Jan 1, 1970, 00:00:00 UTC)
    """
    createdAt: int

    """
    Role of the connection
    """
    role: OpenViduRole

    """
    Token associated to the connection
    """
    token: str

    """
    <a href="/docs/openvidu-pro/" target="_blank" style="display: inline-block; background-color: rgb(0, 136, 170); color: white; font-weight: bold; padding: 0px 5px; margin-right: 5px; border-radius: 3px; font-size: 13px; line-height:21px; font-family: Montserrat, sans-serif">PRO</a>
    Geo location of the connection, with the following format: `"CITY, COUNTRY"` (`"unknown"` if it wasn't possible to locate it)
    """
    location: str

    """
    A complete description of the platform used by the participant to connect to the session
    """
    platform: str

    """
    Data associated to the connection on the server-side. This value is set with property [[TokenOptions.data]] when calling [[Session.generateToken]]
    """
    serverData: str

    """
    Data associated to the connection on the client-side. This value is set with second parameter of method
    [Session.connect](/api/openvidu-browser/classes/session.html#connect) in OpenVidu Browser
    """
    clientData: str

    """
    Array of Publisher objects self particular Connection is publishing to the Session (each Publisher object has one Stream, uniquely
    identified by its `streamId`). You can call [[Session.forceUnpublish]] passing any of self values as parameter
    """
    publishers: Publisher[] = []

    """
    Array of streams (their `streamId` properties) self particular Connection is subscribed to. Each one always corresponds to one
    Publisher of some other Connection: each string of self array must be equal to one [[Publisher.streamId]] of other Connection
    """
    subscribers: str[] = []

    """
    @hidden
    """
    def __init__(self, connectionId: str, createdAt: int, role: OpenViduRole, token: str, location: str, platform: str, serverData: str, clientData: str,:
        publishers: Publisher[], subscribers: str[])
        self.connectionId = connectionId
        self.createdAt = createdAt
        self.role = role
        self.token = token
        self.location = location
        self.platform = platform
        self.serverData = serverData
        self.clientData = clientData
        self.publishers = publishers
        self.subscribers = subscribers


    """
    @hidden
    """
    def __eq__(self, other: Connection): boolean:
        equals: boolean = (
            self.connectionId == other.connectionId and
            self.createdAt == other.createdAt and
            self.role == other.role and
            self.token == other.token and
            self.location == other.location and
            self.platform == other.platform and
            self.serverData == other.serverData and
            self.clientData == other.clientData and
            self.subscribers.length == other.subscribers.length and
            self.publishers.length == other.publishers.length)
        if equals:
            equals = JSON.stringify(self.subscribers) == JSON.stringify(other.subscribers)
            if equals:
                i = 0 = None
                while (equals and i < self.publishers.length)
                    equals = self.publishers[i].def __eq__(self, other.publishers[i])
                    i++

                return equals
            else:
                return false

        else:
            return false

