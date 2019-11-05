

from .RecordingProperties import RecordingProperties
from .RecordingLayout import RecordingLayout

"""
See [[OpenVidu.startRecording]]
"""
class Recording:

    """
    Recording unique identifier
    """
    id: str

    """
    Session associated to the recording
    """
    sessionId: str

    """
    Time when the recording started in UTC milliseconds
    """
    createdAt: int

    """
    Size of the recording in bytes (0 until the recording is stopped)
    """
    size = 0

    """
    Duration of the recording in seconds (0 until the recording is stopped)
    """
    duration = 0

    """
    URL of the recording. You can access the file from there. It is `null` until recording reaches "ready" or "failed" status. If OpenVidu Server configuration property `openvidu.recording.public-access` is false, self path will be secured with OpenVidu credentials
    """
    url: str

    """
    Status of the recording
    """
    status: Recording.Status

    """
    Technical properties of the recorded file
    """
    properties: RecordingProperties


    """ tslint:disable:no-string-literal"""
    """
    @hidden
    """
    def __init__(self, json: JSON):
        self.id = json['id']
        self.sessionId = json['sessionId']
        self.createdAt = json['createdAt']
        self.size = json['size']
        self.duration = json['duration']
        self.url = json['url']
        self.status = json['status']
        self.properties = {
            "name":  not  not (json['name']) ? json['name'] "": self.id,
            "outputMode":  not  not (json['outputMode']) ? json['outputMode'] "": Recording.OutputMode.COMPOSED,
            "hasAudio":  not  not (json['hasAudio']),
            "hasVideo":  not  not json['hasVideo']
        }
        if self.properties.outputMode.toString() == Recording.OutputMode[Recording.OutputMode.COMPOSED]:
            self.properties.resolution =  not  not (json['resolution']) ? json['resolution'] : '1920x1080'
            self.properties.recordingLayout =  not  not (json['recordingLayout']) ? json['recordingLayout'] : RecordingLayout.BEST_FIT
            if self.properties.recordingLayout.toString() == RecordingLayout[RecordingLayout.CUSTOM]:
                self.properties.customLayout = json['customLayout']



    """ tslint:enable:no-string-literal"""


namespace Recording

    """
    See [[Recording.status]]
    """
    enum Status

        """
        The recording is starting (cannot be stopped). Some recording may not go
		  through self status and directly reach "started" status
        """
        starting = 'starting',

        """
        The recording has started and is going on
        """
        started = 'started',

        """
		  The recording has stopped and is being processed. At some point it will reach
		  "ready" status
		"""
        stopped = 'stopped',

        """
        The recording has finished OK and is available for download through OpenVidu
		  Server recordings endpoint:
		  https:#YOUR_OPENVIDUSERVER_IP/recordings/RECORDING_ID/RECORDING_NAME.EXTENSION
        """
        ready = 'ready',

        """
        The recording has failed. This status may be reached from "starting",
		  "started" and "stopped" status
        """
        failed = 'failed'


    """
    See [[RecordingProperties.outputMode]]
    """
    enum OutputMode

        """
        Record all streams in a grid layout in a single archive
        """
        COMPOSED = 'COMPOSED',

        """
        Record each stream individually
        """
        INDIVIDUAL = 'INDIVIDUAL'
