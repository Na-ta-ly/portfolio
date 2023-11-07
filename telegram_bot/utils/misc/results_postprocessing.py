from typing import Dict


def get_pilots_list(dictionary: Dict, reverse: bool = False) -> str:
    """Transforms dict with pilots and their points into string, sorting by points"""
    response = _get_pilots_dict(dictionary)
    response = dict(sorted(response.items(), key=lambda item: float(item[1]), reverse=not reverse))
    results = []
    for pilot, points in response.items():
        results.append(''.join([pilot, ' has ',
                                str(points), ' points']))
    return '\n'.join(results)


def _get_pilots_dict(dictionary: Dict) -> Dict:
    """Builds dict from pilots and their points"""
    response = dictionary.get("response", 0)
    results = dict()
    if response != 0:
        for item in response:
            results[str(item.get("driver", 0).get("name", 0))] = \
                item.get("points", 0) if item.get("points", 0) is not None else 0
    return results
