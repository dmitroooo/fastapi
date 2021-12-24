from locust import task, FastHttpUser

class MyUser(FastHttpUser):
    @task
    def index(self):
        response = self.client.get("/product")

 #   @task
  #  def post(self):
  #      response = self.client.get("/post")

    #@task
    #def indexlink(self):
    #    response = self.client.get("/")
        #response = self.client.post("/group", json={"name": "NameGroup", "description": "description bla bla bla"})
        #       response = self.client.post("/group", json={"name": "NameGroup", "description": "description bla bla bla"})
        #       response = self.client.post("/users", json={"username": "locust", "password": "locust", "first_name": "locust", "last_name": "locust", "gender": "M",})