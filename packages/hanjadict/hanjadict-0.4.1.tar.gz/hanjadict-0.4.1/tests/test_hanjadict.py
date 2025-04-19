from src import hanjadict


def test_lookup():
    assert hanjadict.lookup("雪") == "눈 설"
    assert hanjadict.lookup("山") == "메 산"
    assert hanjadict.lookup("xyz") is None
    assert hanjadict.lookup("") is None


def test_is_hanja():
    assert hanjadict.is_hanja("雪") is True
    assert hanjadict.is_hanja("한글") is False
    assert hanjadict.is_hanja("") is False


def test_pronunciation_formats():
    # Normal format
    assert hanjadict.pronunciation("雪") == "설"  # 눈 설

    # With parentheses
    assert hanjadict.pronunciation("䴫") == "령"  # 영양 령(영)

    # With slash
    assert hanjadict.pronunciation("燕") == "연"  # 제비 연/잔치 연

    # With comma
    assert hanjadict.pronunciation("㴕") == "집"  # 샘솟을 집, 샘솟을 설

    # Invalid input
    assert hanjadict.pronunciation("xyz") is None
    assert hanjadict.pronunciation("") is None


def test_all_pronunciations():
    failures = []

    for char, hun_eum in hanjadict.table_data.items():
        pron = hanjadict.pronunciation(char)

        # Check that pronunciation is not None and at least 1 character
        if pron is None or len(pron) < 1:
            failures.append(
                f"Character '{char}' ({hun_eum}) returned invalid pronunciation"
            )
            continue

        if pron not in hun_eum:
            failures.append(
                f"Character '{char}' ({hun_eum}): '{pron}' not in '{hun_eum}'"
            )

    # If there are any failures, fail the test with details
    assert not failures, (
        f"Pronunciation failures ({len(failures)}):\n"
        + "\n".join(failures[:20])
        + (
            f"\n... and {len(failures) - 20} more failures"
            if len(failures) > 20
            else ""
        )
    )
