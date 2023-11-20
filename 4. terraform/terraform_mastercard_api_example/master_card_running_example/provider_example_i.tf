terraform {
  required_providers {
    restapi = {
      source = "Mastercard/restapi"
     
    }
  }
}


provider "restapi" {
  uri = "http://192.168.68.62:8080/"
  # headers = {
  #   X-Internal-Client = "abc123"
  #   Authorization = "Iamatoooken"
  # }

  debug                = true
  write_returns_object = true
  create_method = "POST"
  update_method = "PUT"
  destroy_method = "DELETE"
  read_method = "GET"

}

# data "restapi_object" "Foo" {
#   path = "/api/v1/objects/cars"
#   search_key = "first"
#   search_value = "Foo"
#   //data = "{ \"id\": \"55555\", \"first\": \"Foo\", \"last\": \"Bar\" }"
# }

resource "restapi_object" "Foo2" {
  path = "/api/v1/objects/cars"
  # create_method = "POST"
  # read_method = "GET"
  # update_method = "PUT"
  # destroy_method = "DELETE"
  data = "{ \"id\": \"55555\", \"make\": \"mazda\",  \"module\": \"mz3gt\", \"year\": \"2018\" }"
}

resource "restapi_object" "Foo3" {
  path = "/api/v1/objects/cars"
  data = "{ \"id\": \"6666\", \"make\": \"honda\",  \"module\": \"gsll\", \"year\": \"2020\" }"
}