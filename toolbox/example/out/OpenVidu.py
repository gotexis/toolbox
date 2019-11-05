from requests import requests
from .Connection import Connection
from .Publisher import Publisher
from .Recording import Recording
from .RecordingProperties import RecordingProperties
from .Session import Session
from .SessionProperties import SessionProperties
from .RecordingLayout import RecordingLayout

"""
@hidden
"""



class OpenVidu:

    Buffer = require('buffer/').Buffer

    """
    @hidden
    """
    hostname: str
    """
    @hidden
    """
    port: int
    """
    @hidden
    """
    basicAuth: str

    """
    @hidden
    """
    API_RECORDINGS: str = '/api/recordings'
    """
    @hidden
    """
    API_RECORDINGS_START: str = '/start'
    """
    @hidden
    """
    API_RECORDINGS_STOP: str = '/stop'
    """
    @hidden
    """
    API_SESSIONS = '/api/sessions'
    """
    @hidden
    """
    API_TOKENS = '/api/tokens'


    """
    Array of active sessions. This value will remain unchanged since the last time method [[OpenVidu.fetch]]
    was called. Exceptions to self rule are:

    - Calling [[Session.fetch]] updates that specific Session status
    - Calling [[Session.close]] automatically removes the Session from the list of active Sessions
    - Calling [[Session.forceDisconnect]] automatically updates the inner affected connections for that specific Session
    - Calling [[Session.forceUnpublish]] also automatically updates the inner affected connections for that specific Session
    - Calling [[OpenVidu.startRecording]] and [[OpenVidu.stopRecording]] automatically updates the recording status of the
    Session ([[Session.recording]])

    To get the array of active sessions with their current actual value, you must call [[OpenVidu.fetch]] before consulting
    property [[activeSessions]]
    """
    activeSessions: Session[] = []

    """
    @param urlOpenViduServer Public accessible IP where your instance of OpenVidu Server is up an running
    @param secret Secret used on OpenVidu Server initialization
    """
    def __init__(urlOpenViduServer: str, secret: str):
        self.setHostnameAndPort()
        self.basicAuth = self.getBasicAuth(secret)


    """
    Creates an OpenVidu session. You can call [[Session.getSessionId]] inside the resolved promise to retrieve the `sessionId`

    @returns A Promise that is resolved to the [[Session]] if success and rejected with an Error object if not.
    """
    def createSession(properties: SessionProperties)
        return Promise<Session>((resolve, reject) =>
            session = Session(self, properties)
            session.getSessionIdHttp()
                .then(sessionId =>
                    self.activeSessions.push(session)
                    resolve(session)

                .catch(error =>
                    reject(error)
                )
        )


    startRecording(sessionId: str)
    startRecording(sessionId: str, name: str)
    startRecording(sessionId: str, properties: RecordingProperties)

    """
    Starts the recording of a [[Session]]

    @param sessionId The `sessionId` of the [[Session]] you want to start recording
    @param name The name you want to give to the video file. You can access self same value in your clients on recording events (`recordingStarted`, `recordingStopped`)

    @returns A Promise that is resolved to the [[Recording]] if it successfully started (the recording can be stopped with guarantees) and rejected with an Error
    object if not. This Error object has as `message` property with the following values:
    - `404`: no session exists for the passed `sessionId`
    - `406`: the session has no connected participants
    - `422`: when passing [[RecordingProperties]], `resolution` parameter exceeds acceptable values (for both width and height, min 100px and max 1999px) or trying
    to start a recording with both `hasAudio` and `hasVideo` to false
    - `409`: the session is not configured for using [[MediaMode.ROUTED]] or it is already being recorded
    - `501`: OpenVidu Server recording module is disabled (`openvidu.recording` property set to `false`)
    """
    def startRecording(sessionId: str, param2: str | RecordingProperties)
        return Promise<Recording>((resolve, reject) =>

            data = None

            if  not  not param2:
                if  not (typeof param2 == 'string'):
                    properties = <RecordingProperties>param2
                    data = {
                        "session": sessionId,
                        "name":  not  not properties.name ? properties.name "": '',
                        "outputMode":  not  not properties.outputMode ? properties.outputMode "": Recording.OutputMode.COMPOSED,
                        "hasAudio":  not  not (properties.hasAudio),
                        "hasVideo":  not  not (properties.hasVideo)
                    }
                    if data.outputMode.toString() == Recording.OutputMode[Recording.OutputMode.COMPOSED]:
                        data.resolution =  not  not properties.resolution ? properties.resolution : '1920x1080'
                        data.recordingLayout =  not  not properties.recordingLayout ? properties.recordingLayout : RecordingLayout.BEST_FIT
                        if data.recordingLayout.toString() == RecordingLayout[RecordingLayout.CUSTOM]:
                            data.customLayout =  not  not properties.customLayout ? properties.customLayout : ''


                    data = JSON.stringify(data)
                else:
                    data = JSON.stringify(
                        session: sessionId,
                        name: param2,
                        outputMode: Recording.OutputMode.COMPOSED
                    )

            else:
                data = JSON.stringify(
                    session: sessionId,
                    name: '',
                    outputMode: Recording.OutputMode.COMPOSED
                )


            requests.post(
                'https:#' + self.hostname + ':' + self.port + OpenVidu.API_RECORDINGS + OpenVidu.API_RECORDINGS_START,
                data,

                    headers:
                        'Authorization': self.basicAuth,
                        'Content-Type': 'application/json'



                .then(res =>
                    if res.status == 200:
                        # SUCCESS response from openvidu-server (Recording in JSON format). Resolve Recording
                        r: Recording = Recording(res.data)
                        activeSession = self.activeSessions.find(s => s.sessionId == r.sessionId)
                        if  not  not activeSession:
                            activeSession.recording = true
                        else:
                            console.warn("No active session found for sessionId '" + r.sessionId + "'. This instance of OpenVidu Node Client didn't create self session")

                        resolve(r)
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
                else:
                    # Something happened in setting up the request that triggered an Error
                    console.error('Error', error.message)

            )
        )


    """
    Stops the recording of a [[Session]]

    @param recordingId The `id` property of the [[Recording]] you want to stop

    @returns A Promise that is resolved to the [[Recording]] if it successfully stopped and rejected with an Error object if not. This Error object has as `message` property with the following values:
    - `404`: no recording exists for the passed `recordingId`
    - `406`: recording has `starting` status. Wait until `started` status before stopping the recording
    """
    def stopRecording(recordingId: str)
        return Promise<Recording>((resolve, reject) =>

            requests.post(
                'https:#' + self.hostname + ':' + self.port + OpenVidu.API_RECORDINGS + OpenVidu.API_RECORDINGS_STOP + '/' + recordingId,
                undefined,

                    headers:
                        'Authorization': self.basicAuth,
                        'Content-Type': 'application/x-www-form-urlencoded'



                .then(res =>
                    if res.status == 200:
                        # SUCCESS response from openvidu-server (Recording in JSON format). Resolve Recording
                        r: Recording = Recording(res.data)
                        activeSession = self.activeSessions.find(s => s.sessionId == r.sessionId)
                        if  not  not activeSession:
                            activeSession.recording = false
                        else:
                            console.warn("No active session found for sessionId '" + r.sessionId + "'. This instance of OpenVidu Node Client didn't create self session")

                        resolve(r)
                    else:
                        # ERROR response from openvidu-server. Resolve HTTP status
                        reject(Error(res.status.toString()))

                ).catch(error =>
                if error.response:
                    # The request was made and the server responded with a status code (not 2xx)
                    reject(Error(error.response.status.toString()))
                elif error.request:
                    # The request was made but no response was received `error.request` is an instance of XMLHttpRequest
                    # in the browser and an instance of http.ClientRequest in node.js
                    console.error(error.request)
                else:
                    # Something happened in setting up the request that triggered an Error
                    console.error('Error', error.message)

            )
        )


    """
    Gets an existing [[Recording]]

    @param recordingId The `id` property of the [[Recording]] you want to retrieve

    @returns A Promise that is resolved to the [[Recording]] if it successfully stopped and rejected with an Error object if not. This Error object has as `message` property with the following values:
    - `404`: no recording exists for the passed `recordingId`
    """
    def getRecording(recordingId: str)
        return Promise<Recording>((resolve, reject) =>

            requests.get(
                'https:#' + self.hostname + ':' + self.port + OpenVidu.API_RECORDINGS + '/' + recordingId,

                    headers:
                        'Authorization': self.basicAuth,
                        'Content-Type': 'application/x-www-form-urlencoded'



                .then(res =>
                    if res.status == 200:
                        # SUCCESS response from openvidu-server (Recording in JSON format). Resolve Recording
                        resolve(Recording(res.data))
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
                else:
                    # Something happened in setting up the request that triggered an Error
                    console.error('Error', error.message)

            )
        )


    """
    Lists all existing recordings

    @returns A Promise that is resolved to an array with all existing recordings
    """
    def listRecordings()
        return Promise<Recording[]>((resolve, reject) =>

            requests.get(
                'https:#' + self.hostname + ':' + self.port + OpenVidu.API_RECORDINGS,

                    headers:
                        Authorization: self.basicAuth



                .then(res =>
                    if res.status == 200:
                        # SUCCESS response from openvidu-server (JSON arrays of recordings in JSON format). Resolve list of recordings
                        recordingArray: Recording[] = []
                        responseItems = res.data.items
                        for (item of responseItems)
                            recordingArray.push(Recording(item))

                        # Order recordings by time of creation (newest first)
                        recordingArray.sort((r1, r2) => (r1.createdAt < r2.createdAt) ? 1 : ((r2.createdAt < r1.createdAt) ? -1 : 0))
                        resolve(recordingArray)
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
                else:
                    # Something happened in setting up the request that triggered an Error
                    console.error('Error', error.message)

            )
        )


    """
    Deletes a [[Recording]]. The recording must have status `stopped`, `ready` or `failed`

    @param recordingId

    @returns A Promise that is resolved if the Recording was successfully deleted and rejected with an Error object if not. This Error object has as `message` property with the following values:
    - `404`: no recording exists for the passed `recordingId`
    - `409`: the recording has `started` status. Stop it before deletion
    """
    def deleteRecording(recordingId: str)
        return Promise<Error>((resolve, reject) =>

            requests.delete(
                'https:#' + self.hostname + ':' + self.port + OpenVidu.API_RECORDINGS + '/' + recordingId,

                    headers:
                        'Authorization': self.basicAuth,
                        'Content-Type': 'application/x-www-form-urlencoded'



                .then(res =>
                    if res.status == 204:
                        # SUCCESS response from openvidu-server. Resolve undefined
                        resolve(undefined)
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
                else:
                    # Something happened in setting up the request that triggered an Error
                    console.error('Error', error.message)

            )
        )


    """
    Updates every property of every active Session with the current status they have in OpenVidu Server.
    After calling self method you can access the updated array of active sessions in [[activeSessions]]

    @returns A promise resolved to true if any Session status has changed with respect to the server, or to false if not.
    This applies to any property or sub-property of any of the sessions locally stored in OpenVidu Node Client
    """
    def fetch()
        return Promise<boolean>((resolve, reject) =>
            requests.get(
                'https:#' + self.hostname + ':' + self.port + OpenVidu.API_SESSIONS,

                    headers:
                        Authorization: self.basicAuth



                .then(res =>
                    if res.status == 200:

                        # Array to store fetched sessionIds and later remove closed sessions
                        fetchedSessionIds: str[] = []
                        # Boolean to store if any Session has changed
                        hasChanged = false = None

                        for session  in res.data.content:
                            fetchedSessionIds.push(session.sessionId)
                            sessionIndex = -1 = None
                            storedSession = self.activeSessions.find((s, index) =>
                                if s.sessionId == session.sessionId:
                                    sessionIndex = index
                                    return true
                                else:
                                    return false

                            )
                            if  not  not storedSession:
                                fetchedSession: Session = Session(self).resetSessionWithJson(session)
                                changed: boolean =  not storedSession.equalTo(fetchedSession)
                                if changed:
                                    storedSession = fetchedSession
                                    self.activeSessions[sessionIndex] = storedSession

                                console.log("Available session '" + storedSession.sessionId + "' info fetched. Any change: " + changed)
                                hasChanged = hasChanged || changed
                            else:
                                self.activeSessions.push(Session(self, session))
                                console.log("New session '" + session.sessionId + "' info fetched")
                                hasChanged = true

                        )
                        # Remove closed sessions from activeSessions array
                        self.activeSessions = self.activeSessions.filter(session =>
                            if fetchedSessionIds.includes(session.sessionId):
                                return true
                            else:
                                console.log("Removing closed session '" + session.sessionId + "'")
                                hasChanged = true
                                return false

                        )
                        console.log('Active sessions info fetched: ', fetchedSessionIds)
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
                    reject(error)
                else:
                    # Something happened in setting up the request that triggered an Error
                    console.error('Error', error.message)
                    reject(Error(error.message))

            )
        )


    """
    @hidden
    @returns A map paring every existing sessionId with true or false depending on whether it has changed or not
    """
    fetchWebRtc()

        # tslint:disable:no-string-literal
        addWebRtcStatsToConnections = (connection: Connection, connectionsExtendedInfo: any) =>
            connectionExtended = connectionsExtendedInfo.find(c => c.connectionId == connection.connectionId)
            if  not  not connectionExtended:
                publisherArray = []
                for pub  in connection.publishers:
                    publisherExtended = connectionExtended.publishers.find(p => p.streamId == pub.streamId)
                    pubAux = {}
                    # Standard properties
                    pubAux['streamId'] = pub.streamId
                    pubAux['createdAt'] = pub.createdAt
                    mediaOptions = {
                        "audioActive": pub.audioActive,
                        "videoActive": pub.videoActive,
                        "hasAudio": pub.hasAudio,
                        "hasVideo": pub.hasVideo,
                        "typeOfVideo": pub.typeOfVideo,
                        "frameRate": pub.frameRate,
                        "videoDimensions": pub.videoDimensions
                    }
                    pubAux['mediaOptions'] = mediaOptions
                    newPublisher = Publisher(pubAux)
                    # WebRtc properties
                    newPublisher['webRtc'] = {
                        "kms": {
                            "events": publisherExtended.events,
                            "localCandidate": publisherExtended.localCandidate,
                            "remoteCandidate": publisherExtended.remoteCandidate,
                            "receivedCandidates": publisherExtended.receivedCandidates,
                            "webrtcEndpointName": publisherExtended.webrtcEndpointName,
                            "localSdp": publisherExtended.localSdp,
                            "remoteSdp": publisherExtended.remoteSdp
                        }
                    
                    newPublisher['localCandidatePair'] = parseRemoteCandidatePair(newPublisher['webRtc'].kms.remoteCandidate)
                    if  not  not publisherExtended.serverStats:
                        newPublisher['webRtc'].kms.serverStats = publisherExtended.serverStats

                    publisherArray.push(newPublisher)
                )
                subscriberArray = []
                for sub  in connection.subscribers:
                    subscriberExtended = connectionExtended.subscribers.find(s => s.streamId == sub)
                    subAux = {}
                    # Standard properties
                    subAux['streamId'] = sub
                    subAux['publisher'] = subscriberExtended.publisher
                    # WebRtc properties
                    subAux['createdAt'] = subscriberExtended.createdAt
                    subAux['webRtc'] = {
                        "kms": {
                            "events": subscriberExtended.events,
                            "localCandidate": subscriberExtended.localCandidate,
                            "remoteCandidate": subscriberExtended.remoteCandidate,
                            "receivedCandidates": subscriberExtended.receivedCandidates,
                            "webrtcEndpointName": subscriberExtended.webrtcEndpointName,
                            "localSdp": subscriberExtended.localSdp,
                            "remoteSdp": subscriberExtended.remoteSdp
                        }
                    
                    subAux['localCandidatePair'] = parseRemoteCandidatePair(subAux['webRtc'].kms.remoteCandidate)
                    if  not  not subscriberExtended.serverStats:
                        subAux['webRtc'].kms.serverStats = subscriberExtended.serverStats

                    subscriberArray.push(subAux)
                )
                connection.publishers = publisherArray
                connection.subscribers = subscriberArray

        

        parseRemoteCandidatePair = (candidateStr: str) =>
            if  not candidateStr:
                return 'ERROR: No remote candidate available'

            array = candidateStr.split(/\s+/)
            return
                portNumber: array[5],
                ipAddress: array[4],
                transport: array[2].toLowerCase(),
                candidateType: array[7],
                priority: array[3],
                raw: candidateStr
            
        

        return Promise< changes: boolean, sessionChanges >((resolve, reject) =>
            requests.get(
                'https:#' + self.hostname + ':' + self.port + OpenVidu.API_SESSIONS + '?webRtcStats=true',

                    headers:
                        Authorization: self.basicAuth



                .then(res =>
                    if res.status == 200:

                        # Array to store fetched sessionIds and later remove closed sessions
                        fetchedSessionIds: str[] = []
                        # Global changes
                        globalChanges = false = None
                        # Collection of sessionIds telling whether each one of them has changed or not
                        sessionChanges = {}

                        for session  in res.data.content:
                            fetchedSessionIds.push(session.sessionId)
                            sessionIndex = -1 = None
                            storedSession = self.activeSessions.find((s, index) =>
                                if s.sessionId == session.sessionId:
                                    sessionIndex = index
                                    return true
                                else:
                                    return false

                            )
                            if  not  not storedSession:
                                fetchedSession: Session = Session(self).resetSessionWithJson(session)
                                for connection  in fetchedSession.activeConnections:
                                    addWebRtcStatsToConnections(connection, session.connections.content)
                                )

                                changed =  not storedSession.equalTo(fetchedSession) = None
                                if  not changed)  # Check if server webrtc information has changed in any Publisher object (Session.equalTo does not check Publisher.webRtc auxiliary object:
                                    for (connection, index1)  in fetchedSession.activeConnections:
                                        for (index2 = 0; (index2 < connection['publishers'].length &&  not changed) = None index2++)
                                            changed = changed || JSON.stringify(connection['publishers'][index2]['webRtc'])  not == JSON.stringify(storedSession.activeConnections[index1]['publishers'][index2]['webRtc'])

                                    )


                                if changed:
                                    storedSession = fetchedSession
                                    self.activeSessions[sessionIndex] = storedSession

                                console.log("Available session '" + storedSession.sessionId + "' info fetched. Any change: " + changed)
                                sessionChanges[storedSession.sessionId] = changed
                                globalChanges = globalChanges || changed
                            else:
                                newSession = Session(self, session)
                                for connection  in newSession.activeConnections:
                                    addWebRtcStatsToConnections(connection, session.connections.content)
                                )
                                self.activeSessions.push(newSession)
                                console.log("New session '" + session.sessionId + "' info fetched")
                                sessionChanges[session.sessionId] = true
                                globalChanges = true

                        )
                        # Remove closed sessions from activeSessions array
                        self.activeSessions = self.activeSessions.filter(session =>
                            if fetchedSessionIds.includes(session.sessionId):
                                return true
                            else:
                                console.log("Removing closed session '" + session.sessionId + "'")
                                sessionChanges[session.sessionId] = true
                                globalChanges = true
                                return false

                        )
                        console.log('Active sessions info fetched: ', fetchedSessionIds)
                        resolve(changes: globalChanges, sessionChanges)
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
                else:
                    # Something happened in setting up the request that triggered an Error
                    console.error('Error', error.message)

            )
        )


    # tslint:enable:no-string-literal

    getBasicAuth(secret: str): str
        return 'Basic ' + self.Buffer('OPENVIDUAPP:' + secret).toString('base64')


    setHostnameAndPort(): void
        urlSplitted = self.urlOpenViduServer.split(':')
        if urlSplitted.length == 3:  # URL has format: http:# + hostname + :port
            self.hostname = self.urlOpenViduServer.split(':')[1].replace(/\#g, '')
            self.port = parseInt(self.urlOpenViduServer.split(':')[2].replace(/\#g, ''))
        elif urlSplitted.length == 2:  # URL has format: hostname + :port
            self.hostname = self.urlOpenViduServer.split(':')[0].replace(/\#g, '')
            self.port = parseInt(self.urlOpenViduServer.split(':')[1].replace(/\#g, ''))
        else:
            console.error("URL format incorrect: it must contain hostname and port (current value: '" + self.urlOpenViduServer + "')")



