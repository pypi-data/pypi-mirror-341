# 具体测试类实现
from common.WSBaseApi import BaseApiTest
import pytest

@pytest.mark.gateway
class TestGateway(BaseApiTest):pass


@pytest.mark.aqua
class TestAqua(BaseApiTest):pass