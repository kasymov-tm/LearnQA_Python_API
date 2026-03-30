
import pytest
import requests


user_agents_data = [
    {
        "user_agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "expected": {
            "device": "Android",
            "browser": "No",
            "platform": "mobile"
        }
    },
    {
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
        "expected": {
            "device": "iOS",
            "browser": "Chrome",
            "platform": "mobile"
        }
    },
    {
        "user_agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "expected": {
            "device": "Unknown",
            "browser": "Unknown",
            "platform": "Googlebot"
        }
    },
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
        "expected": {
            "device": "No",
            "browser": "Chrome",
            "platform": "web"
        }
    },
    {
        "user_agent": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "expected": {
            "browser": "No",
            "device": "iPhone",
            "platform": "Mobile"
        }
    }
]

@pytest.mark.parametrize("test_case", user_agents_data)
def test_user_agent_check(test_case):
    user_agent = test_case["user_agent"]
    expected = test_case["expected"]


    response = requests.get(
        "https://playground.learnqa.ru/ajax/api/user_agent_check",
        headers={"User-Agent": user_agent}
    )


    result = response.json()


    print(f"\nТестируем User Agent: {user_agent}")
    print(f"Ожидаемый результат: {expected}")
    print(f"Фактический результат: {result}")


    assert "device" in result, "В ответе отсутствует поле 'device'"
    assert "browser" in result, "В ответе отсутствует поле 'browser'"
    assert "platform" in result, "В ответе отсутствует поле 'platform'"


    assert result["device"] == expected["device"], (
        f"Неверное значение 'device': ожидается {expected['device']}, получено {result['device']}"
    )
    assert result["browser"] == expected["browser"], (
        f"Неверное значение 'browser': ожидается {expected['browser']}, получено {result['browser']}"
    )
    assert result["platform"] == expected["platform"], (
        f"Неверное значение 'platform': ожидается {expected['platform']}, получено {result['platform']}"
    )