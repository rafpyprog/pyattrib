import os
import pytest
from pyattrib import *


TEST_DIR = os.path.join(os.getcwd(), 'test_dir')


@pytest.fixture
def attrib():
    from pyattrib import Attrib
    attrib = Attrib(TEST_DIR)
    return attrib


''' Test Setup '''
def setup_function():
    ''' Creates a clean test directory for testing attributes '''
    try:
        os.mkdir(TEST_DIR)
    except FileExistsError:
        os.system('attrib -S -H -A -R {}'.format(TEST_DIR))

        os.rmdir(TEST_DIR)
        os.mkdir(TEST_DIR)


def teardown_function():
    ''' Deletes the test directory '''
    os.system('attrib -S -H -A -R {}'.format(TEST_DIR))
    os.rmdir(TEST_DIR)


def tear_down():
    print('Tear down')
    os.rmdir(TEST_DIR)


''' Tests '''
def test_attrib_path_equal_path_arg(attrib):
    attrib.path == TEST_DIR


def test_direcory_without_attributes(attrib):
    assert attrib.attributes == []


def test_set_attribute_archive(attrib):
    attrib.set_attributes(ATTR_ARCHIVE)
    assert attrib.attributes == [ATTR_ARCHIVE]


def test_set_attribute_readonly(attrib):
    attrib.set_attributes(ATTR_READ_ONLY)
    assert attrib.attributes == [ATTR_READ_ONLY]


def test_set_attribute_hidden(attrib):
    attrib.set_attributes(ATTR_HIDDEN)
    assert attrib.attributes == [ATTR_HIDDEN]


def test_set_attribute_system_file(attrib):
    attrib.set_attributes(ATTR_SYSTEM_FILE)
    assert attrib.attributes == [ATTR_SYSTEM_FILE]


def test_set_multiple_attributes(attrib):
    mult_attributes = ['a', 's', 'h', 'r']
    attrib.set_attributes(*mult_attributes)
    assert attrib.attributes == ['A', 'S', 'H', 'R']


def test_set_empty_attributes(attrib):
    attrib.set_attributes()
    attr1 = attrib.attributes
    assert attrib.attributes == []
    attr2 = attrib.attributes
    assert attr1 == attr2


def test_clear_all_attributes(attrib):
    mult_attributes = ['a', 's', 'h', 'r']
    attrib.set_attributes(*mult_attributes)
    attrib.clear_all()
    assert attrib.attributes == []


def test_raise_value_erro_for_invalid_attribute(attrib):
    invalid_attribute = 'invalid'
    with pytest.raises(ValueError):
        attrib.set_attributes(invalid_attribute)


def test_clear_attribute(attrib):
    attribute = ATTR_HIDDEN
    attrib.set_attributes(attribute)
    attrib.clear_attributes(attribute)
    assert attrib.attributes == []


def test_clear_multiple_attributes(attrib):
    attributes = (ATTR_HIDDEN, ATTR_SYSTEM_FILE)
    attrib.set_attributes(*attributes)
    attrib.clear_attributes(*attributes)
    assert attrib.attributes == []

def test_is_hidden(attrib):
    assert attrib.is_hidden is False

    attrib.set_attributes(ATTR_HIDDEN)
    assert attrib.is_hidden is True


def test_is_archive(attrib):
    assert attrib.is_archive is False

    attrib.set_attributes(ATTR_ARCHIVE)
    assert attrib.is_archive is True


def test_is_read_only(attrib):
    assert attrib.is_read_only is False

    attrib.set_attributes(ATTR_READ_ONLY)
    assert attrib.is_read_only is True


def test_is_system_file(attrib):
    assert attrib.is_system_file is False

    attrib.set_attributes(ATTR_SYSTEM_FILE)
    assert attrib.is_system_file is True


def test_is_invalid_attribution(attrib):
    attrib.set_attributes(ATTR_SYSTEM_FILE)
    with pytest.raises(AttributeError):
        attrib.set_attributes(ATTR_HIDDEN)

def test_attributes_without_path():
    attrib = Attrib()
    assert attrib.attributes == []
