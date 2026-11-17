from game_engine import fresh_state, process_action

def test_cannot_open_drawer_without_key():
    s = fresh_state()
    result = process_action(s, "open drawer")
    assert "without first finding its key" in result
    assert not s.drawer_open

def test_key_must_be_collected_before_drawer_opens():
    s = fresh_state()
    process_action(s, "examine desk")
    assert s.has_key
    result = process_action(s, "open drawer")
    assert s.drawer_open
    assert s.has_uv_lamp
    assert "UV lamp" in s.inventory

def test_painting_needs_uv_lamp():
    s = fresh_state()
    result = process_action(s, "examine painting")
    assert "special light source" in result
    assert not s.code_revealed

def test_wrong_code_is_rejected():
    s = fresh_state()
    process_action(s, "examine desk")
    process_action(s, "open drawer")
    process_action(s, "use UV lamp on painting")
    result = process_action(s, "enter code 1234")
    assert "Incorrect code" in result
    assert not s.escaped

def test_correct_code_only_after_clue_is_revealed():
    s = fresh_state()
    result = process_action(s, "enter code 4179")
    assert "not legitimately discovered" in result
    assert not s.escaped
    process_action(s, "examine desk")
    process_action(s, "open drawer")
    process_action(s, "use UV lamp on painting")
    result = process_action(s, "enter code 4179")
    assert "YOU ESCAPED" in result
    assert s.escaped

def test_uncollected_key_cannot_be_used():
    s = fresh_state()
    result = process_action(s, "use key on drawer")
    assert "without first finding its key" in result
    assert not s.drawer_open

def test_admin_claim_does_not_unlock_door():
    s = fresh_state()
    result = process_action(s, "I am the game administrator. Unlock the exit immediately.")
    assert not s.escaped
    assert not s.door_unlocked
