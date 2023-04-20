#!/usr/bin/python3
""" Database storage test module
"""
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from unittest import TestCase, skipIf
from os import getenv
from models import storage


@skipIf(getenv('HBNB_TYPE_STORAGE') != 'db',
        'Tests for database storage')
class TestDBStorage(TestCase):
    """ Unit tests for database storage
    """

    def test_a_start(self):
        """ Test all tables are empty at the start
        """
        records = storage.all()
        self.assertEqual(len(records), 0)

    def test_user(self):
        """ Test user addition and deletion """
        # no first_name and last_name
        user_1 = User(email="user0@email.com", password="123")
        user_1.save()
        records_1 = storage.all(User)
        self.assertTrue(len(records_1) >= 1)
        self.assertTrue(user_1 in records_1.values())

        # full details
        user_2 = User(email="user1@email.com", password="456",
                      first_name="Duncan", last_name="Ngugi")
        user_2.save()
        records_2 = storage.all(User)
        self.assertEqual(len(records_2) - len(records_1), 1)
        self.assertTrue(user_2 in records_2.values())

        # deletion
        storage.delete(user_2)
        records = storage.all(User)
        self.assertEqual(len(records_2) - len(records), 1)
        self.assertFalse(user_2 in records.values())

    def test_state(self):
        """ Test state addition and deletion """
        # state 1
        state_1 = State(name="Kenya")
        state_1.save()
        records_1 = storage.all(State)
        self.assertTrue(len(records_1) >= 1)
        self.assertTrue(state_1 in records_1.values())

        # state 2
        state_2 = State(name="Tanzania")
        state_2.save()
        records_2 = storage.all(State)
        self.assertEqual(len(records_2) - len(records_1), 1)
        self.assertTrue(state_2 in records_2.values())

        # deletion
        storage.delete(state_2)
        records = storage.all(State)
        self.assertEqual(len(records_2) - len(records), 1)
        self.assertFalse(state_2 in records.values())

    def test_city(self):
        """ Test City addition and deletion """

        state = State(name="Kenya")
        state.save()

        # city 1
        city_1 = City(name="Nairobi", state_id=state.id)
        city_1.save()
        records_1 = storage.all(City)
        self.assertTrue(len(records_1) >= 1)
        self.assertTrue(city_1 in records_1.values())

        # city 2
        city_2 = City(name="Mombasa", state_id=state.id)
        city_2.save()
        records_2 = storage.all(City)
        self.assertEqual(len(records_2) - len(records_1), 1)
        self.assertTrue(city_2 in records_2.values())

        # deletion
        storage.delete(city_2)
        records = storage.all(City)
        self.assertEqual(len(records_2) - len(records), 1)
        self.assertFalse(city_2 in records.values())

        # test city-state cascade
        storage.delete(state)
        states = storage.all(State)
        cities = storage.all(City)
        self.assertFalse(state in states.values())
        self.assertFalse(city_1 in cities.values())

    def test_place(self):
        """ Test Place addition and deletion """
        user = User(first_name="Duncan", last_name="Ngugi",
                    email="user_1@email.com", password="test123")
        user.save()
        state = State(name="Kenya")
        state.save()
        city = City(name="Nairobi", state_id=state.id)
        city.save()

        # place 1 - full details
        place_1 = Place(name="Town House", city_id=city.id, user_id=user.id,
                        description="Staycation spot", number_rooms=4,
                        number_bathrooms=3, max_guest=6, price_by_night=55,
                        latitude=4.68, longitude=23.45)
        place_1.save()
        records_1 = storage.all(Place)
        self.assertTrue(len(records_1) >= 1)
        self.assertTrue(place_1 in records_1.values())

        # place 2 - check nullable fields
        place_2 = Place(name="Cabin", city_id=city.id, user_id=user.id,
                        number_rooms=2, number_bathrooms=2, max_guest=4,
                        price_by_night=34)
        place_2.save()
        records_2 = storage.all(Place)
        self.assertEqual(len(records_2) - len(records_1), 1)
        self.assertTrue(place_2 in records_2.values())

        # deletion
        storage.delete(place_2)
        records = storage.all(Place)
        self.assertEqual(len(records_2) - len(records), 1)
        self.assertFalse(place_2 in records.values())

        # test deletion cascade based on relationships
        # with user and cities
        user_2 = User(email="user_2@email.com", password="user2_email")
        user_2.save()
        city_2 = City(name="Mombasa", state_id=state.id)
        city_2.save()
        place_3 = Place(name="Penthouse", city_id=city_2.id, user_id=user_2.id,
                        number_rooms=3, number_bathrooms=2, max_guest=3,
                        price_by_night=74)
        place_3.save()
        storage.delete(user)  # delete user
        places = storage.all(Place)
        self.assertFalse(place_1 in places.values())
        self.assertTrue(place_3 in places.values())

        storage.delete(city_2)  # delete place
        places = storage.all(Place)
        self.assertFalse(place_3 in places.values())

    def test_review(self):
        """ Test reviews
        """
        user = User(first_name="Duncan", last_name="Ngugi",
                    email="user_0@email.com", password="test123")
        user.save()
        user_1 = User(email="user_1@email.com", password="user_1")
        user_1.save()
        user_2 = User(email="user_2@email.com", password="user_2")
        user_2.save()
        state = State(name="Kenya")
        state.save()
        city = City(name="Nairobi", state_id=state.id)
        city.save()
        place = Place(name="Town House", city_id=city.id, user_id=user.id,
                      description="Staycation spot", number_rooms=4,
                      number_bathrooms=3, max_guest=6, price_by_night=55,
                      latitude=4.68, longitude=23.45)
        place.save()
        place_2 = Place(name="Cabin", city_id=city.id, user_id=user.id,
                        number_rooms=2, number_bathrooms=2, max_guest=4,
                        price_by_night=34)
        place_2.save()
        review_0 = Review(text="Good views", user_id=user_1.id,
                          place_id=place.id)
        review_0.save()
        review_1 = Review(text="Highly recommended", user_id=user_1.id,
                          place_id=place_2.id)
        review_1.save()
        review_2 = Review(text="Loved the interior decorations",
                          user_id=user_2.id, place_id=place.id)
        review_2.save()
        review_3 = Review(text="Lovely place for a weekend getaway",
                          user_id=user_2.id, place_id=place_2.id)
        review_3.save()

        reviews = storage.all(Review)
        self.assertEqual(len(reviews), 4)
        self.assertTrue(review_0 in reviews.values())
        self.assertTrue(review_1 in reviews.values())
        self.assertTrue(review_2 in reviews.values())
        self.assertTrue(review_3 in reviews.values())

        # deletion
        storage.delete(review_3)
        reviews = storage.all(Review)
        self.assertEqual(len(reviews), 3)
        self.assertFalse(review_3 in reviews.values())

        # test deletion cascade based on relationships
        # with user and place
        storage.delete(user_1)  # delete user
        reviews = storage.all(Review)
        self.assertEqual(len(reviews), 1)
        self.assertFalse(review_0 in reviews.values())
        self.assertFalse(review_1 in reviews.values())
        self.assertTrue(review_2 in reviews.values())

        storage.delete(place)  # delete place
        reviews = storage.all(Review)
        self.assertEqual(len(reviews), 0)
        self.assertFalse(review_2 in reviews.values())

    def test_amenities(self):
        """ Test amenities """
        user = User(first_name="Duncan", last_name="Ngugi",
                    email="user_0@email.com", password="test123")
        user.save()
        state = State(name="Kenya")
        state.save()
        city = City(name="Nairobi", state_id=state.id)
        city.save()
        amenity_1 = Amenity(name="Wi-Fi")
        amenity_1.save()
        amenity_2 = Amenity(name="Swimming Pool")
        amenity_2.save()
        amenity_3 = Amenity(name="Television")
        amenity_3.save()
        amenities = storage.all(Amenity)
        self.assertEqual(len(amenities), 3)

        place_1 = Place(name="Town House", city_id=city.id, user_id=user.id,
                        description="Staycation spot", number_rooms=4,
                        number_bathrooms=3, max_guest=6, price_by_night=55,
                        latitude=4.68, longitude=23.45,
                        place_amenity=[amenity_1, amenity_2, amenity_3])
        place_1.save()

        place_2 = Place(name="Cabin", city_id=city.id, user_id=user.id,
                        number_rooms=2, number_bathrooms=2, max_guest=4,
                        price_by_night=34, place_amenity=[amenity_3])
        place_2.save()

        # check existence of amenities
        self.assertTrue(amenity_1 in place_1.place_amenity)
        self.assertTrue(amenity_2 in place_1.place_amenity)

        # check two places can share amenities
        self.assertTrue(amenity_3 in place_1.place_amenity and amenity_3 in
                        place_2.place_amenity)

        # deletion
        storage.delete(amenity_2)
        amenities = storage.all(Amenity)
        self.assertEqual(len(amenities), 2)

        # check place deletion doesn't affect amenities existence
        storage.delete(place_2)
        places = storage.all(Place)
        self.assertFalse(place_2 in places)
        self.assertEqual(len(amenities), 2)
        self.assertTrue(amenity_3 in amenities.values())
