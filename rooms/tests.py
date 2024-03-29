from rest_framework.test import APITestCase
from . import models
from users.models import User

class TestAmenities(APITestCase):
    
    NAME = "Amenity Test"
    DESC = "Amenity Test Description"
    URL = "/api/v1/rooms/amenities/"
    
    def setUp(self): # setUp 메소드는 테스트 메소드가 실행되기 전에 실행
        models.Amenity.objects.create(
            name = self.NAME,
            description = self.DESC,
        )
    
    def test_all_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()
        
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        
        self.assertIsInstance(data, list, "Response data is not list") 
        # get 메소드의 반환값이 list인지 확인, 어차피 test용 DB라 결과는 빈 리스트지만 그래도 리스트로 반환이 되기는 해야한다.
        
        self.assertEqual(len(data), 1, "Response data length is not 1") # setUp에 의해 1개 생성되어있다.
        self.assertEqual(data[0]["name"], self.NAME, "Amenity name is not same")
        self.assertEqual(data[0]["description"], self.DESC, "Amenity description is not same")
        
    def test_create_amenity(self):
        
        new_amenity_name = "New Amenity"
        new_amenity_desc = "New Amenity Description"
        
        response = self.client.post(
            self.URL,
            data = { # serializer에 정의된 필드들을 모두 넣어줘야 한다.
                "name": new_amenity_name,
                "description": new_amenity_desc,
            },
            format = "json", # json으로 보내는 것을 명시
        )
        data = response.json()
        
        self.assertEqual(
            response.status_code, 
            200, 
            "Status code is not 200"
        )
        
        self.assertEqual(
            data["name"],
            new_amenity_name,
            "Amenity name is not same"
        )
        
        self.assertEqual(
            data["description"],
            new_amenity_desc,
            "Amenity description is not same"
        )
        self.assertIn("name", data, "Name is not in response") # response에 name이 있는지 확인

class TestAmenity(APITestCase):
    
    NAME = "Amenity Test"
    DESC = "Amenity Test Description"
    
    def setUp(self):
        
        models.Amenity.objects.create(
            name = self.NAME,
            description = self.DESC,
        )
    
    def test_not_found(self):
        
        response = self.client.get("/api/v1/rooms/amenities/2")
        
        self.assertEqual(response.status_code, 404, "Status code is not 404")
        
    def test_get_amenity(self):
        
        response = self.client.get("/api/v1/rooms/amenities/2")
        
        self.assertEqual(response.status_code, 404, "Status code is not 404")
        
        response = self.client.get("/api/v1/rooms/amenities/1")
        
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        
        data = response.json()
        
        self.assertEqual(data["name"], self.NAME, "Amenity name is not same")
        
        self.assertEqual(data["description"], self.DESC, "Amenity description is not same")
        
    def test_update_amenity(self):
        
        update_name = "New Amenity"
        update_desc = "New Amenity Description"
        
        response = self.client.put(
            "/api/v1/rooms/amenities/1",
            data = {
                "name": update_name,
                "description": update_desc,
            },
            format = "json",
        )
        data = response.json()
        
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        self.assertEqual(data["name"], update_name, "Amenity name is not same")
        self.assertEqual(data["description"], update_desc, "Amenity description is not same")
        self.assertLessEqual(len(data["name"]), 150, "Name is too long")
        self.assertLessEqual(len(data["description"]), 150, "Description is too long")
        self.assertIn("name", data, "Name is not in response")
        
    def test_delte_amenity(self):
        
        response = self.client.delete("/api/v1/rooms/amenities/1")
        
        self.assertEqual(response.status_code, 204, "Status code is not 204")
        
        
class TestRooms(APITestCase):
    
    def setUp(self):
        
        # test용 user 생성 및 로그인 authentication 테스트
        user = User.objects.create(
            username = "test2",
        )
        user.set_password("1234")
        user.save()
        
        self.user = user # test용 user를 저장
    
    def test_create_room(self):
        
        self.client.force_login(
            self.user, # force_login은 user만 있으면 되고, login은 username과 password가 필요
        )
        
        response = self.client.post(
            "/api/v1/rooms/",
        )
        
        self.assertEqual(response.status_code, 400, "Status code is not 400")