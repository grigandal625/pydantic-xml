import datetime as dt
import pathlib
from typing import Generic, TypeVar

from pydantic import HttpUrl

from pydantic_xml import BaseXmlModel, element

AuthType = TypeVar('AuthType')


class SoapHeader(
    BaseXmlModel, Generic[AuthType],
    tag='Header',
    ns='soap',
):
    auth: AuthType


class SoapMethod(BaseXmlModel):
    pass


MethodType = TypeVar('MethodType', bound=SoapMethod)


class SoapBody(
    BaseXmlModel, Generic[MethodType],
    tag='Body',
    ns='soap',
):
    call: MethodType


HeaderType = TypeVar('HeaderType', bound=SoapHeader)
BodyType = TypeVar('BodyType', bound=SoapBody)


class SoapEnvelope(
    BaseXmlModel,
    Generic[HeaderType, BodyType],
    tag='Envelope',
    ns='soap',
    nsmap={
        'soap': 'http://www.w3.org/2003/05/soap-envelope/',
    },
):
    header: HeaderType
    body: BodyType


class BasicAuth(
    BaseXmlModel,
    tag='BasicAuth',
    ns='auth',
    nsmap={
        'auth': 'http://www.company.com/auth',
    },
):
    user: str = element(tag='Username')
    password: str = element(tag='Password')


class CreateCompanyMethod(
    SoapMethod,
    tag='CreateCompany',
    ns='co',
    nsmap={
        'co': 'https://www.company.com/co',
    },
):
    trade_name: str = element(tag='TradeName')
    founded: dt.date = element(tag='Founded')
    website: HttpUrl = element(tag='WebSite')


CreateCompanyRequest = SoapEnvelope[
    SoapHeader[
        BasicAuth
    ],
    SoapBody[
        CreateCompanyMethod
    ],
]

xml_doc = pathlib.Path('./doc.xml').read_text()

request = CreateCompanyRequest.from_xml(xml_doc)

json_doc = pathlib.Path('./doc.json').read_text()
assert request == CreateCompanyRequest.model_validate_json(json_doc)
