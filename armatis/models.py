# -*- coding: utf-8 -*-


class Company(object):
    def __init__(self, name=None, code=None, phone=None, digit=None):
        # Company's name
        self.name = name
        # Codename
        self.code = code
        # The digit of the invoice number
        if digit is None:
            digit = []
        self.digit = digit
        # Phone number of the service center
        self.phone = phone

    def __repr__(self):
        return '[%s] %s (%s)' % (
            self.code,
            self.name,
            self.phone
        )


class Track(object):
    def __init__(self, time=None, location=None, status=None,
                 phone1=None, phone2=None):
        # Time
        self.time = time
        # Location
        self.location = location
        # Status
        self.status = status
        # Phone number 1
        self.phone1 = phone1
        # Phone number 2
        self.phone2 = phone2

    def __repr__(self):
        return '[%s] %s - %s / %s / %s' % (
            self.time,
            self.status,
            self.location,
            self.phone1,
            self.phone2
        )


class Tracker(object):
    def __init__(self):
        self._tracks = []

    @property
    def tracks(self):
        return self._tracks

    def add_track(self, new_track):
        if not isinstance(new_track, Track):
            raise TypeError('The new_track must be Track!')
        self._tracks.append(new_track)

    def track_by_status(self, status):
        """
        Find the tracking information matching the status

        :param str status: The status to find the tracking information
        :return: The tracking information matching the status
        """
        tracks = list(filter(lambda x: x.status == status, self._tracks))
        if len(tracks) > 0:
            return tracks[-1]
        raise LookupError("Can't find the track by status %s" % status)

    def __iter__(self):
        return iter(self._tracks)


class Parcel(object):
    def __init__(self, sender=None, receiver=None, invoice_number=None,
                 address=None, note=None):
        # The sender's name
        self.sender = sender
        # The receiver's name
        self.receiver = receiver
        # Invoice number
        self.invoice_number = invoice_number
        # The receiver's address
        self.address = address
        # Note for the parcel
        self.note = note

    def __repr__(self):
        return '[%s] From: %s, To: %s, %s' % (
            self.invoice_number,
            self.sender,
            self.receiver,
            self.note
        )
