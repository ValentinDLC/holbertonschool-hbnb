```mermaid
classDiagram
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity

    User "1" --> "*" Place : owns
    Place "1" *-- "*" Review : contains
    Place "*" --> "*" Amenity : has
    User "1" --> "*" Review : write

    class BaseModel{
       # id : UUID4
       # create_date : Date
       # update_date : Date
       + create()
       + update()
       + delete()
    }
    class User{
       - first_name : String
       - last_name : String
       - email : String
       - password : String
       - is_admin : Boolean
       + verify_password()
       + verify_email()
       + is_admin()
    }
    class Place{
       - owner_id: UUID4
       - title : String
       - description : String
       - price : Float
       - latitude : Float
       - longitude : Float
       + list()
       + get_Price()
       + set_Price()
       + get_Location()
       + set_Location()
       + is_available()
       + add_amenity()
       + remove_amenity()

    }
    class Review{
       - place_id : UUID4
       - user_id : UUID4
       - rating : Integer
       - comment : String
       + listed_by_place()
       + listed_by_user()
       + listed_by_date()
    }
    class Amenity{
       - place_id : UUID4
       - name : String
       - description : String
       + list()
    }