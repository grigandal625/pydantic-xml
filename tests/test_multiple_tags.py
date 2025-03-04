from typing import List

from pydantic_xml import BaseXmlModel, element


def test_model_multiple_tags():

    class TestModel(BaseXmlModel, tag=['model', 'other_tag']):
        element1: str = element()
        element2: str = element()

    xml = '''
    <model>
        <element1>test</element1>
        <element2>test</element2>
    </model>
    '''

    actual_obj = TestModel.from_xml(xml)
    assert actual_obj.element1 == 'test'
    assert actual_obj.element2 == 'test'

    actual_xml_tree = actual_obj.to_xml_tree()
    assert actual_xml_tree.tag == 'model'

    xml = '''
    <other_tag>
        <element1>test</element1>
        <element2>test</element2>
    </other_tag>
    '''

    actual_obj = TestModel.from_xml(xml)
    assert actual_obj.element1 == 'test'
    assert actual_obj.element2 == 'test'

    actual_xml_tree = actual_obj.to_xml_tree()
    assert actual_xml_tree.tag == 'other_tag'


def test_element_multiple_tag():

    class InnerModel(BaseXmlModel):
        text: str

    class TestSimpleModel(BaseXmlModel, tag='model'):
        element1: InnerModel = element(tag=['element1', 'other_element'])

    xml = '''
    <model>
        <element1>text</element1>
    </model>
    '''

    actual_obj = TestSimpleModel.from_xml(xml)
    assert actual_obj.element1.text == 'text'

    actual_xml_tree = actual_obj.to_xml_tree()
    assert actual_xml_tree.tag == 'model'
    assert len(actual_xml_tree) == 1
    assert actual_xml_tree[0].tag == 'element1'
    assert actual_xml_tree[0].text == 'text'

    xml = '''
    <model>
        <other_element>text</other_element>
    </model>
    '''
    actual_obj = TestSimpleModel.from_xml(xml)
    assert actual_obj.element1.text == 'text'

    actual_xml_tree = actual_obj.to_xml_tree()
    assert actual_xml_tree.tag == 'model'
    assert len(actual_xml_tree) == 1
    assert actual_xml_tree[0].tag == 'other_element'
    assert actual_xml_tree[0].text == 'text'

    class TestModel(BaseXmlModel, tag='model'):
        element1: List[InnerModel] = element(tag=['element1', 'other_element'])

    xml = '''
    <model>
        <element1>text</element1>
        <element1>text2</element1>
        <other_element>another_text</other_element>
    </model>
    '''
    actual_obj = TestModel.from_xml(xml)
    assert len(actual_obj.element1) == 3
    assert actual_obj.element1[0].text == 'text'
    assert actual_obj.element1[1].text == 'text2'
    assert actual_obj.element1[2].text == 'another_text'

    actual_xml_tree = actual_obj.to_xml_tree()
    assert actual_xml_tree.tag == 'model'
    assert len(actual_xml_tree) == 3
    assert actual_xml_tree[0].tag == 'element1'
    assert actual_xml_tree[1].tag == 'element1'
    assert actual_xml_tree[2].tag == 'other_element'

    class TestComplexModel(BaseXmlModel, tag=['model', 'root']):
        element1: List[InnerModel] = element(tag=['element1', 'other_element'])

    xml = '''
    <root>
        <element1>text</element1>
        <element1>text2</element1>
        <other_element>another_text</other_element>
    </root>
    '''
    actual_obj = TestComplexModel.from_xml(xml)
    assert len(actual_obj.element1) == 3
    assert actual_obj.element1[0].text == 'text'
    assert actual_obj.element1[1].text == 'text2'
    assert actual_obj.element1[2].text == 'another_text'

    actual_xml_tree = actual_obj.to_xml_tree()
    assert actual_xml_tree.tag == 'root'
    assert len(actual_xml_tree) == 3
    assert actual_xml_tree[0].tag == 'element1'
    assert actual_xml_tree[1].tag == 'element1'
    assert actual_xml_tree[2].tag == 'other_element'

    xml = '''
    <model>
        <element1>text</element1>
        <element1>text2</element1>
        <other_element>another_text</other_element>
    </model>
    '''

    actual_obj = TestComplexModel.from_xml(xml)
    assert len(actual_obj.element1) == 3
    assert actual_obj.element1[0].text == 'text'
    assert actual_obj.element1[1].text == 'text2'
    assert actual_obj.element1[2].text == 'another_text'

    actual_xml_tree = actual_obj.to_xml_tree()
    assert actual_xml_tree.tag == 'model'
    assert len(actual_xml_tree) == 3
    assert actual_xml_tree[0].tag == 'element1'
    assert actual_xml_tree[1].tag == 'element1'
    assert actual_xml_tree[2].tag == 'other_element'
