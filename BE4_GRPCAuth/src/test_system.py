import unittest
import urllib.request
import urllib.error
import json
import random

BASE_URL = "http://localhost:8000"

class TestMicroservices(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Генерируем случайный email для тестов, чтобы не было конфликтов при перезапусках
        cls.email = f"tester_{random.randint(10000, 99999)}@mail.com"
        cls.password = "secure_pass_123"
        cls.token = None

    def make_request(self, method, endpoint, data=None, token=None):
        url = BASE_URL + endpoint
        req = urllib.request.Request(url, method=method)
        req.add_header('Content-Type', 'application/json')
        if token:
            req.add_header('Authorization', f'Bearer {token}')
        
        body = None
        if data:
            body = json.dumps(data).encode('utf-8')
            
        try:
            with urllib.request.urlopen(req, data=body) as response:
                return response.status, json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode())
        except urllib.error.URLError as e:
            self.fail(f"Сервер недоступен по адресу {BASE_URL}. Ты запустил docker-compose up?")

    def test_1_middleware_blocks_unauthorized(self):
        """Проверка: Middleware не пускает без токена"""
        status, _ = self.make_request('GET', '/protected_route')
        self.assertEqual(status, 401, "Middleware должна возвращать 401")

    def test_2_register_user(self):
        """Проверка: Регистрация (хэширование bcrypt + сохранение в Postgres по gRPC)"""
        payload = {
            "email": self.email,
            "first_name": "John",
            "last_name": "Doe",
            "phone": "123",
            "password": self.password
        }
        status, response = self.make_request('POST', '/register', data=payload)
        self.assertEqual(status, 200, "Регистрация должна пройти успешно")
        self.assertIn("token", response, "Должен вернуться JWT токен")
        TestMicroservices.token = response["token"]

    def test_3_register_duplicate_fails(self):
        """Проверка: Повторная регистрация на тот же email выдает ошибку"""
        payload = {
            "email": self.email,
            "first_name": "John",
            "last_name": "Doe",
            "phone": "123",
            "password": "new_password"
        }
        status, _ = self.make_request('POST', '/register', data=payload)
        self.assertEqual(status, 400, "Должна быть ошибка 400 при дубликате")

    def test_4_login_success(self):
        """Проверка: Успешная аутентификация (проверка хэша пароля по gRPC)"""
        payload = {"email": self.email, "password": self.password}
        status, response = self.make_request('POST', '/auth', data=payload)
        self.assertEqual(status, 200, "Логин должен быть успешным")
        self.assertIn("token", response, "Должен вернуться JWT токен")
        
    def test_5_login_wrong_password(self):
        """Проверка: Ошибка аутентификации при неверном пароле"""
        payload = {"email": self.email, "password": "wrong_password"}
        status, _ = self.make_request('POST', '/auth', data=payload)
        self.assertEqual(status, 401, "Должна быть ошибка 401")

    def test_6_middleware_allows_authorized(self):
        """Проверка: Middleware пускает с правильным токеном (валидация JWT по gRPC)"""
        self.assertIsNotNone(self.token, "Токен должен был сохраниться с шага регистрации")
        status, response = self.make_request('GET', '/protected_route', token=self.token)
        self.assertEqual(status, 200, "Middleware должна пропустить запрос")
        self.assertEqual(response.get("message"), "You have accessed a protected route!")

    def test_7_reset_password(self):
        """Проверка: Ручка сброса пароля (заглушка вывода в консоль)"""
        payload = {"email": self.email}
        status, response = self.make_request('POST', '/reset', data=payload)
        self.assertEqual(status, 200, "Сброс пароля должен пройти успешно")
        self.assertIn("message", response)

if __name__ == '__main__':
    unittest.main(verbosity=2)
