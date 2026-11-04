import xml.etree.ElementTree as ET


def test_xml_response_has_expected_structure(httpbin_request_context):
    response = httpbin_request_context.get("/xml")

    assert response.status == 200
    content_type = response.headers.get("content-type", "")
    assert "xml" in content_type

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


def test_xml_elements_can_be_found_with_namespace():
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


def test_xml_catalog_with_namespace_has_expected_products():
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

    expected_products = [
        {
            "id": "101",
            "category": "electronics",
            "name": "Laptop",
            "price": 3999.99
        },
        {
            "id": "102",
            "category": "electronics",
            "name": "Monitor",
            "price": 1299.99
        }
    ]

    assert len(products) == len(expected_products)

    for product, expected_product in zip(products, expected_products):
        assert product.attrib["id"] == expected_product["id"]
        assert product.attrib["category"] == expected_product["category"]

        name = product.find("shop:name", namespaces)
        price = product.find("shop:price", namespaces)

        assert name is not None
        assert price is not None

        assert name.text is not None
        assert price.text is not None

        assert name.text == expected_product["name"]
        assert float(price.text) == expected_product["price"]