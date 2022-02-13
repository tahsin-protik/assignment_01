import unittest
from urllib import response
from .. import create_app
from ..models.user import User
from ..utils.db import db
import copy


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app=create_app(config="testing")
        self.appctx=self.app.app_context()
        self.appctx.push()
        self.client=self.app.test_client()
        with self.app.app_context():
            db.create_all()


    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app=None
        self.client =None
    
    complete_user={
        "username": "dummy",
        "first_name": "Dummy",
        "last_name" : "Dummy",
        "user_type": "Parent",
        "street": "Dummy",
        "city": "Dummy",
        "state": "Dummy",
        "zip_code": "Dummy",
    }


    def test_1_create_user_success(self):
        #succesful parent account creation
        data=copy.copy(self.complete_user)
        response=self.client.post('/create',json=data)
        assert response.status_code == 200
        response_data= response.json
        assert response_data["message"] == "User Created"
        assert response_data["payload"]["username"] == data["username"]


    def test_2_update_user_success(self):
        data=copy.copy(self.complete_user)
        response=self.client.post('/create', json=data)
        data['first_name']="Updated Dummy"
        response=self.client.post('/update', json=data)
        assert response.status_code == 200
        response_data= response.json
        assert response_data["message"] == "User Updated"
        assert response_data["payload"]["first_name"] == data["first_name"]

    def test_11_update_user_one_field_success(self):
        data=copy.copy(self.complete_user)
        response=self.client.post('/create', json=data)
        data={"username": "dummy", "first_name": "Updated Dummy"}
        response=self.client.post('/update', json=data)
        assert response.status_code == 200
        response_data= response.json
        assert response_data["message"] == "User Updated"
        assert response_data["payload"]["first_name"] == data["first_name"]
        assert response_data["payload"]["last_name"] == self.complete_user["last_name"]
    
    def test_3_update_user_failed(self):
        data=copy.copy(self.complete_user)
        response=self.client.post('/update', json=data)
        # assert response.status_code == 400
        response_data= response.json
        assert response_data["message"] == "User Doesn't Exist"
    
    def test_4_delete_user_success(self):
        data=copy.copy(self.complete_user)
        response=self.client.post('/create', json=data)
        response=self.client.delete('/delete/'+data["username"], json=data)
        assert response.status_code == 200
        response_data= response.json
        assert response_data["message"] == "User Deleted"
    
    def test_5_delete_user_failed(self):
        data=copy.copy(self.complete_user)
        response=self.client.delete('/delete/'+data["username"], json=data)
        assert response.status_code == 404
        response_data= response.json
        assert response_data["message"] == "User Not Found"

    def test_6_create_user_child(self):
         data=copy.copy(self.complete_user)
         response = self.client.post('/create', json=data)
         data['username']="child_dummy"
         data["user_type"]="Child"
         data["parent"]="dummy"
         del data["city"]
         del data["street"]
         del data["zip_code"]
         del data["state"]
         response = self.client.post('/create', json=data)
         response_data= response.json
         assert response.status_code==200
         assert response_data["message"] == "User Created"
         assert response_data["payload"]["username"] == data["username"]

    def test_7_create_user_child_without_parent(self):
        data=copy.copy(self.complete_user)
        data['username']="child_dummy"
        data["user_type"]="Child"
        del data["city"]
        del data["street"]
        del data["zip_code"]
        del data["state"]
        response = self.client.post('/create', json=data)
        response_data= response.json
        assert response.status_code== 400
        assert response_data["message"] == "Child User Should Have Parent"

    def test_8_create_user_child_with_invalid_parent(self):
        data=copy.copy(self.complete_user)
        data['username']="child_dummy"
        data["user_type"]="Child"
        data["parent"]="dummy3456325"
        del data["city"]
        del data["street"]
        del data["zip_code"]
        del data["state"]
        response = self.client.post('/create', json=data)
        response_data= response.json
        assert response.status_code== 400
        assert response_data["message"] == "Parent Not Valid"
    
    def test_9_create_user_parent_with_parent(self):
        data=copy.copy(self.complete_user)
        data["parent"]="dummy"
        response=self.client.post('/create',json=data)
        assert response.status_code == 400
        response_data= response.json
        assert response_data["message"] == "Parent User Shouldn't Have Parent"
    def test_10_create_user_username_exist(self):
        data=copy.copy(self.complete_user)
        response=self.client.post('/create',json=data)
        response=self.client.post('/create',json=data)
        assert response.status_code == 400
        response_data= response.json
        assert response_data["message"] == "Username Already Exists"
