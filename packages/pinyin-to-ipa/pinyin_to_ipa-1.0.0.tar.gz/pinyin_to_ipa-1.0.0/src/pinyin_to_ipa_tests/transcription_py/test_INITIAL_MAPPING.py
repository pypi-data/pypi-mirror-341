from pypinyin.style._constants import _INITIALS, _INITIALS_NOT_STRICT

from pinyin_to_ipa.transcription import INITIAL_MAPPING


def test_contains_not_all_initials() -> None:
  missing_initials = set(_INITIALS_NOT_STRICT) - INITIAL_MAPPING.keys()
  missing_initials_that_are_expected = {"w", "y"}
  assert missing_initials == missing_initials_that_are_expected


def test_equals_to_all_strict_initials() -> None:
  missing_initials = set(_INITIALS) - INITIAL_MAPPING.keys()
  additional_initials = INITIAL_MAPPING.keys() - set(_INITIALS)
  assert len(missing_initials) == 0
  assert len(additional_initials) == 0
