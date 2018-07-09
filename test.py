import property


def test_property():
    properties = property.parse('config/db.properties')
    print(properties.get('host'))


if __name__ == '__main__':
    test_property()
