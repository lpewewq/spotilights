from bisect import bisect_right


class AttributeFromKeysMixIn:
    def __init__(self, obj) -> None:
        self.progress = None
        for key in obj.keys():
            setattr(self, key, obj.get(key))

    @staticmethod
    def _format_seconds(value):
        minutes, seconds = divmod(value, 60)
        seconds, mseconds = divmod(seconds * 1000, 1000)
        return f"{int(minutes):02d}:{int(seconds):02d}:{int(mseconds):03d}"

    def __repr__(self) -> str:
        base_info = ""
        if hasattr(self, "start"):
            base_info = f"{self._format_seconds(self.start)} - {self._format_seconds(self.start + self.duration)}"
        return f"<{self.__class__.__name__} {base_info}>"

    def is_current(self, time):
        if self.start <= time < self.start + self.duration:
            self.progress = (time - self.start) / self.duration
            return True
        self.progress = None
        return False


class Track(AttributeFromKeysMixIn):
    def __init__(self, track) -> None:
        super().__init__(track)


class Section(AttributeFromKeysMixIn):
    def __init__(self, section) -> None:
        super().__init__(section)


class Bar(AttributeFromKeysMixIn):
    def __init__(self, bar) -> None:
        super().__init__(bar)


class Beat(AttributeFromKeysMixIn):
    def __init__(self, beat) -> None:
        super().__init__(beat)


class Tatum(AttributeFromKeysMixIn):
    def __init__(self, tatum) -> None:
        super().__init__(tatum)


class Segment(AttributeFromKeysMixIn):
    def __init__(self, segment) -> None:
        super().__init__(segment)


class AnalysisProvider:
    def __init__(self, audio_analysis) -> None:
        track = audio_analysis.get("track", None)
        if track is not None:
            self.track = Track(track)
        else:
            self.track = None
        self._load_from_analysis(audio_analysis, "sections", Section)
        self._load_from_analysis(audio_analysis, "bars", Bar)
        self._load_from_analysis(audio_analysis, "beats", Beat)
        self._load_from_analysis(audio_analysis, "tatums", Tatum)
        self._load_from_analysis(audio_analysis, "segments", Segment)

    def get_current_section(self, time):
        return self._get_current("sections", time)

    def get_current_bar(self, time):
        return self._get_current("bars", time)

    def get_current_beat(self, time):
        return self._get_current("beats", time)

    def get_current_tatum(self, time):
        return self._get_current("tatums", time)

    def get_current_segment(self, time):
        return self._get_current("segments", time)

    def _load_from_analysis(self, audio_analysis, key, cls):
        values = audio_analysis.get(key, None)
        if values is not None and len(values) > 0:
            setattr(self, key, [cls(v) for v in values])
        else:
            setattr(self, key, [])
        setattr(self, key + "_index", None)

    def _get_current(self, key, time):
        index_key = key + "_index"
        index = getattr(self, index_key)
        sequence = getattr(self, key)
        new_index = self._get_current_index(index, sequence, time)
        setattr(self, index_key, new_index)
        if new_index is not None:
            return sequence[new_index], new_index != index
        return None, new_index != index

    @staticmethod
    def _get_current_index(index, sequence, time):
        hi = len(sequence)
        lo = 0

        if index is not None:
            # check if still current
            current = sequence[index]
            if current.is_current(time):
                return index

            # check if next is current
            if current.start + current.duration <= time:
                if index + 1 < len(sequence):
                    index += 1
                    if sequence[index].is_current(time):
                        return index
                lo = index
            else:
                hi = index

        # otherwise binary search current
        index = bisect_right([s.start for s in sequence], time, hi=hi, lo=lo) - 1

        if index < 0 or index >= len(sequence):
            return None

        if sequence[index].is_current(time):
            return index

        # there is no current
        return None
