from ${project_name}.validators import USER_PASSWORD_PATTERN as pattern


def test_user_password_pattern():
    assert pattern.match('Aa1')
    assert pattern.match('Aa1!')
    assert pattern.match('!Aa1')
    assert pattern.match('A@a1')
    assert pattern.match('Aa$1')
    assert pattern.match('Aa1%')
    assert pattern.match('Aa1^')
    assert pattern.match('Aa1(')
    assert pattern.match('Aa1)')
    assert pattern.match('(!Aa1')
    assert pattern.match('(@Aa1')
    assert pattern.match('(#Aa1')
    assert pattern.match('($Aa1')
    assert pattern.match('(^Aa1')
    assert pattern.match('(%Aa1')
    assert pattern.match('(&Aa1')
    assert pattern.match('(*Aa1')
    assert pattern.match('("Aa1')
    assert pattern.match('(>Aa1')
    assert pattern.match('(<Aa1')
    assert pattern.match('(?Aa1')
    assert pattern.match('(ABCabc123')

    assert not pattern.match('')
    assert not pattern.match('aaa')
    assert not pattern.match('AAAA')
    assert not pattern.match('123')
    assert not pattern.match('aaa111')
    assert not pattern.match('AAA111')
    assert not pattern.match('AAAaaa')
    assert not pattern.match('!@#$%^')
    assert not pattern.match('AAAaaa!@#$')
    assert not pattern.match('1@#$!@#%')
    assert not pattern.match('\=-0988')

