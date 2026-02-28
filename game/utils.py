
def validate_pos(pos):
    assert type(pos) in [tuple, list] and len(pos) == 2, 'Wrong pos'
    assert all(value >= 0 and value < 8 for value in pos)
