from aegis.lab import PROMPT_INJECTION_BASIC


def test_prompt_injection_basic_has_known_canary():
    scenario = PROMPT_INJECTION_BASIC

    assert scenario.id == "LAB-PI-001"
    assert scenario.canary == "AEGIS_CANARY_7H92K"
    assert scenario.canary in scenario.system_prompt