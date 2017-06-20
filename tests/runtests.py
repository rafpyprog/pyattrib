import shutil
import os
import pytest
from pyattrib import *


TEST_DIR = os.path.join(os.getcwd(), 'test_dir')
WORKING_DIR = os.getcwd()

def log(data):
    with open('D:\\Projetos\\Pessoal\\pyattrib\\tests\\log.txt', 'a') as f:
        f.write(str(data) + '\n')


def create_file_with_attribute(filename, attribute):
    open(filename, 'w').close()
    os.system('attrib +{} {}'.format(attribute, filename))


def clean_test_dir():
    os.system('attrib -S -H -A -R {}'.format(TEST_DIR))

    for root, dirs, files in os.walk(TEST_DIR):
        for f in files:
            path = os.path.join(root, f)
            os.system('attrib -S -H -A -R {}'.format(path))
            os.remove(path)

    shutil.rmtree(TEST_DIR)


def populate_test_dir():
    os.chdir(TEST_DIR)
    create_file_with_attribute(os.path.join(TEST_DIR, 'archive'), 'a')
    create_file_with_attribute('hidden', 'h')
    create_file_with_attribute('read_only', 'r')
    create_file_with_attribute('system', 's')

    level1 = os.path.join(TEST_DIR, 'level1')
    os.mkdir(level1)

    open(os.path.join(level1, 'file1'), 'w').close()



''' Test Setup '''
def setup_function():
    ''' Creates a clean test directory for testing attributes '''
    try:
        os.mkdir(TEST_DIR)
    except (FileExistsError, PermissionError):
        clean_test_dir()
        os.mkdir(TEST_DIR)

''' Tear Down '''
def teardown_function():
    os.chdir(WORKING_DIR)
    # Deletes the test directory
    clean_test_dir()


@pytest.fixture
def attrib():
    from pyattrib import Attrib
    attrib = Attrib(TEST_DIR)
    return attrib

''' Tests '''
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


def test_raise_on_clear_invalid_attribute(attrib):
    invalid_attribute = 'invalid'
    with pytest.raises(ValueError):
        attrib.clear_attributes(invalid_attribute)


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


def test_attributes_without_path_return_dict():
    # Should return a dict with information from files in the current folder
    # if not recursive

    # save the actual working dir
    working_dir = os.getcwd()

    # Go to the test dir and populate with files
    os.chdir(TEST_DIR)
    create_file_with_attribute('archive', 'a')
    create_file_with_attribute('hidden', 'h')
    create_file_with_attribute('read_only', 'r')
    create_file_with_attribute('system', 's')

    # run attrib
    attrib = Attrib()
    assert isinstance(attrib.attributes, dict)


def test_attributes_without_path_return_dict_correct_lenght():

    # save the actual working dir
    working_dir = os.getcwd()

    # Go to the test dir and populate with files
    os.chdir(TEST_DIR)
    create_file_with_attribute('archive', 'a')
    create_file_with_attribute('hidden', 'h')
    create_file_with_attribute('read_only', 'r')
    create_file_with_attribute('system', 's')

    # run attrib
    attrib = Attrib()
    assert len(attrib.attributes) == 4


def test_attributes_without_path_return_correct_values():
    # save the actual working dir
    working_dir = os.getcwd()

    # Go to the test dir and populate with files
    populate_test_dir()

    # run attrib and get values
    attrib = Attrib()
    attributes = attrib.attributes

    # all files have an A attribute when created
    filename = os.path.join(TEST_DIR, 'archive')
    assert attributes[filename] == ['A']

    filename = os.path.join(TEST_DIR, 'hidden')
    assert attributes[filename] == ['A', ATTR_HIDDEN]

    filename = os.path.join(TEST_DIR, 'read_only')
    assert attributes[filename] == ['A', ATTR_READ_ONLY]

    filename = os.path.join(TEST_DIR, 'system')
    assert attributes[filename] == ['A', ATTR_SYSTEM_FILE]

    # make some changes
    os.system('attrib -a archive')
    attrib = Attrib()
    attributes = attrib.attributes
    filename = os.path.join(TEST_DIR, 'archive')
    assert attributes[filename] == []


def test_attributes_recursive_true():
    working_dir = os.getcwd()
    populate_test_dir()

    attrib = Attrib(recursive=True)
    attr = attrib.attributes
    print(attr)
    assert len(attr) == 5


def test_attributes_recursive_true_apply_directory_true():
    working_dir = os.getcwd()
    populate_test_dir()

    attrib = Attrib(recursive=True, apply_directories=True)
    attr = attrib.attributes
    print(attr)
    assert len(attr) == 6

    # assert there is one dir
    dir_count = sum(os.path.isdir(i) for i in attr)
    assert dir_count == 1


def test_set_attributes_recursive():
    os.chdir(TEST_DIR)
    open('file1.txt', 'w').close()
    #subdir
    foo = os.path.join(TEST_DIR, 'foo')
    os.mkdir(foo)

    file2 = os.path.join(foo, 'file2')
    open(os.path.join(foo, 'file2'), 'w').close()
    a = Attrib(recursive=True)

    a.set_attributes(ATTR_HIDDEN)
    assert len(a.attributes) == 2

    test_file2 = Attrib(file2)
    assert test_file2.attributes == ['A', ATTR_HIDDEN]

    test_file1 = Attrib(os.path.join(TEST_DIR, 'file1.txt'))
    assert test_file1.attributes == ['A', ATTR_HIDDEN]


def test_clear_all_attributes_recursive():
    os.chdir(TEST_DIR)
    open('file1.txt', 'w').close()
    #subdir
    foo = os.path.join(TEST_DIR, 'foo')
    os.mkdir(foo)

    file2 = os.path.join(foo, 'file2')
    open(os.path.join(foo, 'file2'), 'w').close()
    a = Attrib(recursive=True)

    a.set_attributes(ATTR_HIDDEN)
    assert len(a.attributes) == 2

    test_file2 = Attrib(file2)
    assert test_file2.attributes == ['A', ATTR_HIDDEN]

    test_file1 = Attrib(os.path.join(TEST_DIR, 'file1.txt'))
    assert test_file1.attributes == ['A', ATTR_HIDDEN]

    a.clear_all()
    assert test_file1.attributes == []
    assert test_file2.attributes == []
