


"""
See [[Connection.publishers]]
*
This is a backend representation of a published media stream (see [OpenVidu Browser Stream class](/api/openvidu-browser/classes/stream.html))
"""
class Publisher:

    """
    Unique identifier of the [Stream](/api/openvidu-browser/classes/stream.html) associated to self Publisher.
    Each Publisher is paired with only one Stream, so you can identify each Publisher by its
    [`Stream.streamId`](/api/openvidu-browser/classes/stream.html#streamid)
    """
    streamId: str

    """
    Timestamp when self Publisher started publishing, in UTC milliseconds (ms since Jan 1, 1970, 00:00:00 UTC)
    """
    createdAt: int

    """
    See properties of [Stream](/api/openvidu-browser/classes/stream.html) object in OpenVidu Browser library to find out more
    """
    hasAudio: boolean

    """
    See properties of [Stream](/api/openvidu-browser/classes/stream.html) object in OpenVidu Browser library to find out more
    """
    hasVideo: boolean

    """
    See properties of [Stream](/api/openvidu-browser/classes/stream.html) object in OpenVidu Browser library to find out more
    """
    audioActive: boolean

    """
    See properties of [Stream](/api/openvidu-browser/classes/stream.html) object in OpenVidu Browser library to find out more
    """
    videoActive: boolean

    """
    See properties of [Stream](/api/openvidu-browser/classes/stream.html) object in OpenVidu Browser library to find out more
    """
    frameRate: int

    """
    See properties of [Stream](/api/openvidu-browser/classes/stream.html) object in OpenVidu Browser library to find out more
    """
    typeOfVideo: str

    """
    See properties of [Stream](/api/openvidu-browser/classes/stream.html) object in OpenVidu Browser library to find out more
    """
    videoDimensions: str

    """
    @hidden
    """
    def __init__(self, json):
        self.streamId = json.streamId
        self.createdAt = json.createdAt
        self.hasAudio = json.mediaOptions.hasAudio
        self.hasVideo = json.mediaOptions.hasVideo
        self.audioActive = json.mediaOptions.audioActive
        self.videoActive = json.mediaOptions.videoActive
        self.frameRate = json.mediaOptions.frameRate
        self.typeOfVideo = json.mediaOptions.typeOfVideo
        self.videoDimensions = json.mediaOptions.videoDimensions


    """
    @hidden
    """
    def __eq__(self, other: Publisher): boolean:
        return (
            self.streamId == other.streamId and
            self.createdAt == other.createdAt and
            self.hasAudio == other.hasAudio and
            self.hasVideo == other.hasVideo and
            self.audioActive == other.audioActive and
            self.videoActive == other.videoActive and
            self.frameRate == other.frameRate and
            self.typeOfVideo == other.typeOfVideo and
            self.videoDimensions == other.videoDimensions
        )

