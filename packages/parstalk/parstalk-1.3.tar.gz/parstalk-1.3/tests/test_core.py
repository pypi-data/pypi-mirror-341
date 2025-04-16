from parstalk import farsi_to_finglish_with_vowels

def test_sample():
    assert farsi_to_finglish_with_vowels("سَلام") == "saalaam"
