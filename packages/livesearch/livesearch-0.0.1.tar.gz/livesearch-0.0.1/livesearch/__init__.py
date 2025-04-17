from typing import Any, List, Iterable
import re

DEFAULT_MATCH_CONFIDENCE = 100


class DetectorResult:
    def __init__(self, lookfor: str, item: Any, confidence: int):
        self.lookfor = lookfor
        self.item = item
        self.confidence = confidence

    @staticmethod
    def sort_detector_result_list(detector_result_list: List['DetectorResult']):
        return sorted(detector_result_list, key=lambda x: x.confidence, reverse=True)


class Detector:
    def get_results(self, lookfor: str, lookin: Iterable[str]) -> List[DetectorResult]:
        return []


class BeginningMatch(Detector):
    # If we match at the beginning, we double the confidence
    confidence = DEFAULT_MATCH_CONFIDENCE * 2

    def get_results(self, lookfor: str, lookin: Iterable[str]) -> List[DetectorResult]:
        pattern = re.compile(r'^' + lookfor, re.IGNORECASE)
        ret = []
        for look in lookin:
            if pattern.match(look):
                ret.append(DetectorResult(lookfor, look, confidence=self.confidence))
        return ret


class FullMatch(Detector):
    # A full match is just normal confidence
    confidence = DEFAULT_MATCH_CONFIDENCE
    
    def get_results(self, lookfor: str, lookin: Iterable[str]) -> List[DetectorResult]:
        pattern = re.compile(lookfor, re.IGNORECASE)
        ret = []
        for look in lookin:
            match = pattern.findall(look)
            print(match)
            if len(match) > 0:
                ret.append(DetectorResult(lookfor, look, confidence=self.confidence + (DEFAULT_MATCH_CONFIDENCE/10) * len(match)))
        return ret


class PartsMatch(Detector):
    # Parts matching is kinda lame, but it might work for some cases
    confidence = DEFAULT_MATCH_CONFIDENCE / 4
    def __init__(self, char_split: str = " "):
        self.char_split = char_split

    def get_results(self, lookfor: str, lookin: Iterable[str]) -> List[DetectorResult]:
        allSearch = lookfor.split(self.char_split)
        ret = []
        for item in lookin:
            item_confidence = 0
            for search in allSearch:
                pattern = re.compile(re.escape(search), re.IGNORECASE)
                if pattern.search(item):
                    item_confidence += self.confidence
            if item_confidence > 0:
                ret.append(DetectorResult(lookfor, item, confidence=item_confidence))
        return ret


def search_get_details(string: str, stringlist: Iterable[str]) -> List[DetectorResult]:
    detectors: List[Detector] = [
        BeginningMatch(),
        FullMatch(),
        PartsMatch(" ")
    ]
    results = []
    """Search for a string in an iterable and return the first match."""
    for detector in detectors:
        results.append(detector.get_results(string, stringlist))
    
    # Coelesce the results into a single list. Remove duplicates from detectors, and add confidence numbers together
    uniqueMatches: List[DetectorResult] = []
    for i in range(len(detectors)):
        currentList: List[DetectorResult] = results[i]
        for match in currentList:
            does_item_exist = False
            item_index = 0
            for item in uniqueMatches:
                if match.item == item.item:
                    does_item_exist = True
                    item_index = uniqueMatches.index(item)
                    break
            if does_item_exist:
                uniqueMatches[item_index].confidence += match.confidence
            else:
                uniqueMatches.append(match)

    # Sort the results by confidence
    uniqueMatches = DetectorResult.sort_detector_result_list(uniqueMatches)

    return uniqueMatches


def search(string : str, stringlist : List[str]) -> List[str]:
    results = search_get_details(string, stringlist)
    return [result.item for result in results]
