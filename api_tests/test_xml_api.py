import xml.etree.ElementTree as ET


def test_xml_response(playwright):
    request = playwright.request.new_context()

    response = request.get("https://httpbin.org/xml")

    assert response.status == 200
    assert "application/xml" in response.headers["content-type"]

    root = ET.fromstring(response.text())

    assert root.tag == "slideshow"
    assert root.attrib["title"] == "Sample Slide Show"

    slides = root.findall("slide")
    titles = root.findall(".//title")
    all_type_slides = root.findall(".//slide[@type='all']")

    assert len(slides) == 2
    assert slides[0].attrib["type"] == "all"
    assert slides[0].find("title").text == "Wake up to WonderWidgets!"

    assert len(titles) >= 1
    assert titles[0].text == "Wake up to WonderWidgets!"

    assert len(all_type_slides) == 2

    request.dispose()


def test_xml_with_namespace():
    xml_data = """
    <catalog xmlns="http://shop.example.com">
        <product>
            <name>Laptop</name>
        </product>
        <product>
            <name>Monitor</name>
        </product>
    </catalog>
    """

    root = ET.fromstring(xml_data)

    namespaces = {
        "shop": "http://shop.example.com"
    }

    products = root.findall(".//shop:product", namespaces)

    assert len(products) == 2

    first_product_name = products[0].find("shop:name", namespaces)

    assert first_product_name.text == "Laptop"


def test_xml_namespace_with_attributes():
    xml_data = """
    <catalog xmlns="http://shop.example.com">
        <product id="101" category="electronics">
            <name>Laptop</name>
            <price>3999.99</price>
        </product>
        <product id="102" category="electronics">
            <name>Monitor</name>
            <price>1299.99</price>
        </product>
    </catalog>
    """

    root = ET.fromstring(xml_data)

    namespaces = {
        "shop": "http://shop.example.com"
    }

    products = root.findall(".//shop:product", namespaces)

    first_product = products[0]

    assert first_product.attrib["id"] == "101"
    assert first_product.attrib["category"] == "electronics"

    name = first_product.find("shop:name", namespaces)
    price = first_product.find("shop:price", namespaces)

    assert name.text == "Laptop"
    assert float(price.text) == 3999.99
