

from requests import requests
from .Connection import Connection
from .MediaMode import MediaMode
from .OpenVidu import OpenVidu
from .OpenViduRole import OpenViduRole
from .Publisher import Publisher
from .Recording import Recording
from .RecordingLayout import RecordingLayout
from .RecordingMode import RecordingMode
from .SessionProperties import SessionProperties
from .TokenOptions import TokenOptions


class Session:

    """
    Unique identifier of the Session
    """
    sessionId: str

    """
    Timestamp when self session was created, in UTC milliseconds (ms since Jan 1, 1970, 00:00:00 UTC)
    """
    createdAt: int

    """
    Properties defining the session
    """
    properties: SessionProperties

    """
    Array of active connections to the session. This property always initialize as an empty array and
    **will remain unchanged since the last time method [[Session.fetch]] was called**. Exceptions to self rule are:
    *
    - Calling [[Session.forceUnpublish]] also automatically updates each affected Connection status
    - Calling [[Session.forceDisconnect]] automatically updates each affected Connection status
    *
    To get the array of active connections with their current actual value, you must call [[Session.fetch]] before consulting
    property [[activeConnections]]
    """
    activeConnections: Connection[] = []

    """
    Whether the session is being recorded or not
    """
    recording = false

    """
    @hidden
    """
    def __init__(self, ov: OpenVidu, propertiesOrJson?):
        if  not  not propertiesOrJson:
            # Defined parameter
            if  not  not propertiesOrJson.sessionId:
                # Parameter is a JSON representation of Session ('sessionId' property always defined)
                self.resetSessionWithJson(propertiesOrJson)
            else:
                # Parameter is a SessionProperties object
                self.properties = propertiesOrJson

        else:
            # Empty parameter
            self.properties = {}

        self.properties.mediaMode =  not  not self.properties.mediaMode ? self.properties.mediaMode : MediaMode.ROUTED
        self.properties.recordingMode =  not  not self.properties.recordingMode ? self.properties.recordingMode : RecordingMode.MANUAL
        self.properties.defaultOutputMode =  not  not self.properties.defaultOutputMode ? self.properties.defaultOutputMode : Recording.OutputMode.COMPOSED
        self.properties.defaultRecordingLayout =  not  not self.properties.defaultRecordingLayout ? self.properties.defaultRecordingLayout : RecordingLayout.BEST_FIT


    """
    Gets the unique identifier of the Session
    """
    def getSessionId(): str
        return self.sessionId


    """
    Gets a token associated to Session object
    *
    @returns A Promise that is resolved to the _token_ if success and rejected with an Error object if not
    """
    def generateToken(tokenOptions: TokenOptions)
        return Promise<string>((resolve, reject) =>

            data = JSON.stringify(
                session: self.sessionId,
                role: ( not  not tokenOptions and  not  not tokenOptions.role) ? tokenOptions.role : OpenViduRole.PUBLISHER,
                data: ( not  not tokenOptions and  not  not tokenOptions.data) ? tokenOptions.data : '',
                kurentoOptions: ( not  not tokenOptions and  not  not tokenOptions.kurentoOptions) ? tokenOptions.kurentoOptions : ,
            )

            requests.post(
                'https:#' + self.ov.hostname + ':' + self.ov.port + OpenVidu.API_TOKENS,
                data,

                    headers:
                        'Authorization': self.ov.basicAuth,
                        'Content-Type': 'application/json'



                .then(res =>
                    if res.status == 200:
                        # SUCCESS response from openvidu-server. Resolve token
                        resolve(res.data.id)
                    else:
                        # ERROR response from openvidu-server. Resolve HTTP status
                        reject(Error(res.status.toString()))

                ).catch(error =>
                    if error.response:
                        # The request was made and the server responded with a status code (not 2xx)
                        reject(Error(error.response.status.toString()))
                    elif error.request:
                        # The request was made but no response was received
                        # `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                        # http.ClientRequest in node.js
                        console.error(error.request)
                        reject(Error(error.request))
                    else:
                        # Something happened in setting up the request that triggered an Error
                        console.error('Error', error.message)
                        reject(Error(error.message))

                )
        )


    """
    Gracefully closes the Session: unpublishes all streams and evicts every participant
    *
    @returns A Promise that is resolved if the session has been closed successfully and rejected with an Error object if not
    """
    def close()
        return Promise<any>((resolve, reject) =>
            requests.delete(
                'https:#' + self.ov.hostname + ':' + self.ov.port + OpenVidu.API_SESSIONS + '/' + self.sessionId,

                    headers:
                        'Authorization': self.ov.basicAuth,
                        'Content-Type': 'application/x-www-form-urlencoded'



                .then(res =>
                    if res.status == 204:
                        # SUCCESS response from openvidu-server
                        indexToRemove: int = self.ov.activeSessions.findIndex(s => s.sessionId == self.sessionId)
                        self.ov.activeSessions.splice(indexToRemove, 1)
                        resolve()
                    else:
                        # ERROR response from openvidu-server. Resolve HTTP status
                        reject(Error(res.status.toString()))

                ).catch(error =>
                    if error.response:
                        # The request was made and the server responded with a status code (not 2xx)
                        reject(Error(error.response.status.toString()))
                    elif error.request:
                        # The request was made but no response was received
                        # `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                        # http.ClientRequest in node.js
                        console.error(error.request)
                        reject(Error(error.request))
                    else:
                        # Something happened in setting up the request that triggered an Error
                        console.error('Error', error.message)
                        reject(Error(error.message))

                )
        )


    """
    Updates every property of the Session with the current status it has in OpenVidu Server. This is especially useful for accessing the list of active
    connections of the Session ([[Session.activeConnections]]) and use those values to call [[Session.forceDisconnect]] or [[Session.forceUnpublish]].
    *
    To update every Session object owned by OpenVidu object, call [[OpenVidu.fetch]]
    *
    @returns A promise resolved to true if the Session status has changed with respect to the server, or to false if not.
            This applies to any property or sub-property of the Session object
    """
    def fetch()
        return Promise<boolean>((resolve, reject) =>
            beforeJSON: str = JSON.stringify(self, self.removeCircularOpenViduReference)
            requests.get(
                'https:#' + self.ov.hostname + ':' + self.ov.port + OpenVidu.API_SESSIONS + '/' + self.sessionId,

                    headers:
                        'Authorization': self.ov.basicAuth,
                        'Content-Type': 'application/x-www-form-urlencoded'



                .then(res =>
                    if res.status == 200:
                        # SUCCESS response from openvidu-server
                        self.resetSessionWithJson(res.data)
                        afterJSON: str = JSON.stringify(self, self.removeCircularOpenViduReference)
                        hasChanged: boolean =  not (beforeJSON == afterJSON)
                        console.log("Session info fetched for session '" + self.sessionId + "'. Any change: " + hasChanged)
                        resolve(hasChanged)
                    else:
                        # ERROR response from openvidu-server. Resolve HTTP status
                        reject(Error(res.status.toString()))

                ).catch(error =>
                    if error.response:
                        # The request was made and the server responded with a status code (not 2xx)
                        reject(Error(error.response.status.toString()))
                    elif error.request:
                        # The request was made but no response was received
                        # `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                        # http.ClientRequest in node.js
                        console.error(error.request)
                        reject(Error(error.request))
                    else:
                        # Something happened in setting up the request that triggered an Error
                        console.error('Error', error.message)
                        reject(Error(error.message))

                )
        )


    """
    Forces the user with Connection `connectionId` to leave the session. OpenVidu Browser will trigger the proper events on the client-side
    (`streamDestroyed`, `connectionDestroyed`, `sessionDisconnected`) with reason set to `"forceDisconnectByServer"`
    *
    You can get `connection` parameter from [[Session.activeConnections]] array ([[Connection.connectionId]] for getting each `connectionId` property).
    Remember to call [[Session.fetch]] before to fetch the current actual properties of the Session from OpenVidu Server
    *
    @returns A Promise that is resolved if the user was successfully disconnected and rejected with an Error object if not
    """
    def forceDisconnect(connection: str | Connection)
        return Promise<any>((resolve, reject) =>
            connectionId: str = typeof connection == 'string' ? connection : (<Connection>connection).connectionId
            requests.delete(
                'https:#' + self.ov.hostname + ':' + self.ov.port + OpenVidu.API_SESSIONS + '/' + self.sessionId + '/connection/' + connectionId,

                    headers:
                        'Authorization': self.ov.basicAuth,
                        'Content-Type': 'application/x-www-form-urlencoded'


                .then(res =>
                    if res.status == 204:
                        # SUCCESS response from openvidu-server
                        # Remove connection from activeConnections array
                        connectionClosed = None
                        self.activeConnections = self.activeConnections.filter(con =>
                            if con.connectionId  not == connectionId:
                                return true
                            else:
                                connectionClosed = con
                                return false

                        )
                        # Remove every Publisher of the closed connection from every subscriber list of other connections
                        if  not  not connectionClosed:
                            for publisher  in connectionClosed.publishers:
                                for con  in self.activeConnections:
                                    con.subscribers = con.subscribers.filter(subscriber =>
                                        # tslint:disable:no-string-literal
                                        if  not  not subscriber['streamId']:
                                            # Subscriber with advanced webRtc configuration properties
                                            return (subscriber['streamId']  not == publisher.streamId)
                                            # tslint:enable:no-string-literal
                                        else:
                                            # Regular string subscribers
                                            return subscriber  not == publisher.streamId

                                    )
                                )
                            )
                        else:
                            console.warn("The closed connection wasn't fetched in OpenVidu Java Client. No changes in the collection of active connections of the Session")

                        console.log("Connection '" + connectionId + "' closed")
                        resolve()
                    else:
                        # ERROR response from openvidu-server. Resolve HTTP status
                        reject(Error(res.status.toString()))


                .catch(error =>
                    if error.response:
                        # The request was made and the server responded with a status code (not 2xx)
                        reject(Error(error.response.status.toString()))
                    elif error.request:
                        # The request was made but no response was received
                        # `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                        # http.ClientRequest in node.js
                        console.error(error.request)
                        reject(Error(error.request))
                    else:
                        # Something happened in setting up the request that triggered an Error
                        console.error('Error', error.message)
                        reject(Error(error.message))

                )
        )


    """
    Forces some user to unpublish a Stream (identified by its `streamId` or the corresponding [[Publisher]] object owning it).
    OpenVidu Browser will trigger the proper events on the client-side (`streamDestroyed`) with reason set to `"forceUnpublishByServer"`.
    *
    You can get `publisher` parameter from [[Connection.publishers]] array ([[Publisher.streamId]] for getting each `streamId` property).
    Remember to call [[Session.fetch]] before to fetch the current actual properties of the Session from OpenVidu Server
    *
    @returns A Promise that is resolved if the stream was successfully unpublished and rejected with an Error object if not
    """
    def forceUnpublish(publisher: str | Publisher)
        return Promise<any>((resolve, reject) =>
            streamId: str = typeof publisher == 'string' ? publisher : (<Publisher>publisher).streamId
            requests.delete(
                'https:#' + self.ov.hostname + ':' + self.ov.port + OpenVidu.API_SESSIONS + '/' + self.sessionId + '/stream/' + streamId,

                    headers:
                        'Authorization': self.ov.basicAuth,
                        'Content-Type': 'application/x-www-form-urlencoded'



                .then(res =>
                    if res.status == 204:
                        # SUCCESS response from openvidu-server
                        for connection  in self.activeConnections:
                            # Try to remove the Publisher from the Connection publishers collection
                            connection.publishers = connection.publishers.filter(pub => pub.streamId  not == streamId)
                            # Try to remove the Publisher from the Connection subscribers collection
                            if  not  not connection.subscribers and connection.subscribers.length > 0:
                                # tslint:disable:no-string-literal
                                if  not  not connection.subscribers[0]['streamId']:
                                    # Subscriber with advanced webRtc configuration properties
                                    connection.subscribers = connection.subscribers.filter(sub => sub['streamId']  not == streamId)
                                    # tslint:enable:no-string-literal
                                else:
                                    # Regular string subscribers
                                    connection.subscribers = connection.subscribers.filter(sub => sub  not == streamId)


                        )
                        console.log("Stream '" + streamId + "' unpublished")
                        resolve()
                    else:
                        # ERROR response from openvidu-server. Resolve HTTP status
                        reject(Error(res.status.toString()))

                ).catch(error =>
                    if error.response:
                        # The request was made and the server responded with a status code (not 2xx)
                        reject(Error(error.response.status.toString()))
                    elif error.request:
                        # The request was made but no response was received
                        # `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                        # http.ClientRequest in node.js
                        console.error(error.request)
                        reject(Error(error.request))
                    else:
                        # Something happened in setting up the request that triggered an Error
                        console.error('Error', error.message)
                        reject(Error(error.message))

                )
        )


    """
    @hidden
    """
    def getSessionIdHttp()
        return Promise<string>((resolve, reject) =>

            if  not  not self.sessionId:
                resolve(self.sessionId)


            data = JSON.stringify(
                mediaMode:  not  not self.properties.mediaMode ? self.properties.mediaMode : MediaMode.ROUTED,
                recordingMode:  not  not self.properties.recordingMode ? self.properties.recordingMode : RecordingMode.MANUAL,
                defaultOutputMode:  not  not self.properties.defaultOutputMode ? self.properties.defaultOutputMode : Recording.OutputMode.COMPOSED,:
                defaultRecordingLayout:  not  not self.properties.defaultRecordingLayout ? self.properties.defaultRecordingLayout : RecordingLayout.BEST_FIT,:
                defaultCustomLayout:  not  not self.properties.defaultCustomLayout ? self.properties.defaultCustomLayout : '',:
                customSessionId:  not  not self.properties.customSessionId ? self.properties.customSessionId : ''
            )

            requests.post(
                'https:#' + self.ov.hostname + ':' + self.ov.port + OpenVidu.API_SESSIONS,
                data,

                    headers:
                        'Authorization': self.ov.basicAuth,
                        'Content-Type': 'application/json'



                .then(res =>
                    if res.status == 200:
                        # SUCCESS response from openvidu-server. Resolve token
                        self.sessionId = res.data.id
                        self.createdAt = res.data.createdAt
                        resolve(self.sessionId)
                    else:
                        # ERROR response from openvidu-server. Resolve HTTP status
                        reject(Error(res.status.toString()))

                ).catch(error =>
                    if error.response:
                        # The request was made and the server responded with a status code (not 2xx)
                        if error.response.status == 409:
                            # 'customSessionId' already existed
                            self.sessionId = self.properties.customSessionId
                            resolve(self.sessionId)
                        else:
                            reject(Error(error.response.status.toString()))

                    elif error.request:
                        # The request was made but no response was received
                        # `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                        # http.ClientRequest in node.js
                        console.error(error.request)
                        reject(Error(error.request))
                    else:
                        # Something happened in setting up the request that triggered an Error
                        console.error('Error', error.message)
                        reject(Error(error.message))

                )
        )


    """
    @hidden
    """
    def resetSessionWithJson(json): Session
        self.sessionId = json.sessionId
        self.createdAt = json.createdAt
        self.recording = json.recording
        customSessionId: str = None
        defaultCustomLayout: str = None:
        if  not  not self.properties:
            customSessionId = self.properties.customSessionId
            defaultCustomLayout =  not  not json.defaultCustomLayout ? json.defaultCustomLayout : self.properties.defaultCustomLayout;:

        self.properties = {
            "mediaMode": json.mediaMode,
            "recordingMode": json.recordingMode,
            "defaultOutputMode": json.defaultOutputMode,
            "defaultRecordingLayout": json.defaultRecordingLayout
        }
        if  not  not customSessionId:
            self.properties.customSessionId = customSessionId
        elif  not  not json.customSessionId:
            self.properties.customSessionId = json.customSessionId

        if  not  not defaultCustomLayout:
            self.properties.defaultCustomLayout = defaultCustomLayout


        self.activeConnections = []
        for connection  in json.connections.content:
            publishers: Publisher[] = []
            for publisher  in connection.publishers:
                publishers.push(Publisher(publisher))
            )
            subscribers: str[] = []
            for subscriber  in connection.subscribers:
                subscribers.push(subscriber.streamId)
            )
            self.activeConnections.push(
                Connection(
                    connection.connectionId,
                    connection.createdAt,
                    connection.role,
                    connection.token,
                    connection.location,
                    connection.platform,
                    connection.serverData,
                    connection.clientData,
                    publishers,
                    subscribers))
        )
        # Order connections by time of creation
        self.activeConnections.sort((c1, c2) => (c1.createdAt > c2.createdAt) ? 1 : ((c2.createdAt > c1.createdAt) ? -1 : 0))
        return self


    """
    @hidden
    """
    def __eq__(self, other: Session): boolean:
        equals: boolean = (
            self.sessionId == other.sessionId and
            self.createdAt == other.createdAt and
            self.recording == other.recording and
            self.activeConnections.length == other.activeConnections.length and
            JSON.stringify(self.properties) == JSON.stringify(other.properties)
        )
        if equals:
            i = 0 = None
            while (equals and i < self.activeConnections.length)
                equals = self.activeConnections[i].def __eq__(self, other.activeConnections[i])
                i++

            return equals
        else:
            return false



    """
    @hidden
    """
    removeCircularOpenViduReference(key: str, value: any)
        if key == 'ov' and value instanceof OpenVidu:
            return
        else:
            return value


