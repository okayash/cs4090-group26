from data_access import create_user, delete_user, get_attraction_details, list_attractions, update_user_interests

class User:

    '''

    Store user information

    '''
    def __init__(self, username, first_name, last_name, email, 
                 age, home_city=None, interests=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.age = age
        self.home_city = home_city
        self.interests = interests

    def add_interest(self, interest):
        if interest not in self.interests:
            self.interests.append(interest)


class Attractions:

    '''

    Holds attraction information

    '''
    def __init__(self, id, name, type,
                 city, tags, price, rating):
        self.id = id
        self.name = name
        self.type = type
        self.city = city
        self.tags = tags
        self.price = price
        self.rating = rating

class UserVisit:

    '''

    Holds an individual user visit to an attraction

    '''
    def __init__(self, id, user_id, attraction_id, date, rating):
        self.id = id
        self.user_id = user_id
        self.attraction_id = attraction_id
        self.date = date
        self.rating = rating

class RecommendationResult:

    def __init__(self, user_id, attractions):
        self.user_id = user_id
        self.attractions = attractions or []

# Services ( delete this later)

class UserServices:
    def CreateUser():
        create_user()
        print('Account Successfully Created!')
    
    def DeleteUser():
        delete_user()
        print("Account Deleted!")

    def UpdateUser():
        
        print("Account Details Updated Successfully!")
    
    def AddUserInterests():
        update_user_interests()
        print("Interests Added")

class AttractionServices:
    def SearchAttractions():
        # ...
        # searching logic here
        list_attractions()
        print("Done.")

    def RecommendationService():
        # ...
        print("Done")    


    


