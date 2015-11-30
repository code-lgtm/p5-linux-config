"""
Script to add sample data in the database
"""

from model import User, Role, Item, Category
from catalog import db

# Add roles
Role.insert_roles()

# Add users
user1 = User(name='John', email='a@b.com', password='test')
user2 = User(name='Mary', email='b@c.com', password='test')
user3 = User(name='Bob', email='c@d.com', password='test')
user4 = User(name='Mike', email='d@e.com', password='test')
user5 = User(name='Estella', email='e@f.com', password='test')

# Add users in the db session
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)
db.session.add(user5)


# Add Categories
category1 = Category(name='Exercise and Fitness')
category2 = Category(name='Cricket')
category3 = Category(name='Camping and Hiking')
category4 = Category(name='Cycling')
category5 = Category(name='Running')
category6 = Category(name='Swimming')
category7 = Category(name='Badminton')
category8 = Category(name='Tennis')
category9 = Category(name='Table Tennis')
category10 = Category(name='Football')

# Add Categories in the db session
db.session.add(category1)
db.session.add(category2)
db.session.add(category3)
db.session.add(category4)
db.session.add(category5)
db.session.add(category6)
db.session.add(category7)
db.session.add(category8)
db.session.add(category9)
db.session.add(category10)


# Add Items for Category 1
item_owner_1 =  User.query.filter_by(email='a@b.com').first()
category_1 = Category.query.filter_by(name='Exercise and Fitness').first()
item_c1 = Item(name='Yoga Mats',
               description='A mat provides padding and support which helps '
                           'you peform the posture comfortably',
               owner_id = item_owner_1.id,
               category_id = category_1.id
               )

item_owner_2 =  User.query.filter_by(email='b@c.com').first()
item_c2 = Item(name='Hydration packs and bottles',
               description='Hydrate throughout the day to reap maximum results '
                           'from your exercise regime',
               owner_id = item_owner_2.id,
               category_id = category_1.id
               )

item_owner_3 =  User.query.filter_by(email='c@d.com').first()
item_c3 = Item(name='Yoga Sets',
               description='Kits to help you get started on the '
                           'road to fitness',
               owner_id = item_owner_3.id,
               category_id = category_1.id
               )

item_owner_4 =  User.query.filter_by(email='d@e.com').first()
item_c4 = Item(name='Yoga Books',
               description='Take your practive to the next level by '
                           'learning more',
               owner_id = item_owner_4.id,
               category_id = category_1.id
               )

item_owner_5 =  User.query.filter_by(email='e@f.com').first()
item_c5 = Item(name='Yoga DVDs',
               description='Get each posture correct to avoid muscle strain '
                           'and ensure maximum gains',
               owner_id = item_owner_5.id,
               category_id = category_1.id
               )
db.session.add(item_c1)
db.session.add(item_c2)
db.session.add(item_c3)
db.session.add(item_c4)
db.session.add(item_c5)

# Add Items for Category 2
category_2 = Category.query.filter_by(name='Cricket').first()
item_c6 = Item(name='Kashmir Willow',
               description='DSC Scorer Kashmir Willow Cricket Bat, '
                           'Short Handle',
               owner_id = item_owner_1.id,
               category_id = category_2.id
               )

item_c7 = Item(name='Cricket Tennis Ball',
               description='Cosco Light Weight Cricket Ball, '
                           'Pack of 6 (Yellow)',
               owner_id = item_owner_2.id,
               category_id = category_2.id
               )

item_c8 = Item(name='Cricket Leather Ball',
               description='SM Rafter Leather Cricket Ball (Red)',
               owner_id = item_owner_3.id,
               category_id = category_2.id
               )

item_c9 = Item(name='Kit Bag',
               description='Nike Black Sports Gym Cylindrical Bag',
               owner_id = item_owner_4.id,
               category_id = category_2.id
               )

item_c10 = Item(name='Batting Gloves',
               description='Sigma Match Batting Gloves Men',
               owner_id = item_owner_5.id,
               category_id = category_2.id
               )
db.session.add(item_c6)
db.session.add(item_c7)
db.session.add(item_c8)
db.session.add(item_c9)
db.session.add(item_c10)

# Add Items for Category 3
category_3 = Category.query.filter_by(name='Camping and Hiking').first()
item_c11 = Item(name='Tent',
               description='Gadgetbucket PICNIC CAMPING PORTABLE WATERPROOF'
                           ' TENT FOR 8 PERSON',
               owner_id = item_owner_1.id,
               category_id = category_3.id
               )

item_c12 = Item(name='Headwear',
               description='Tactical Multifunctional Headwear-Olive Green',
               owner_id = item_owner_2.id,
               category_id = category_3.id
               )

item_c13 = Item(name='Tool Bag',
               description='Gi Style Mechanics Tool Bag',
               owner_id = item_owner_3.id,
               category_id = category_3.id
               )

item_c14 = Item(name='Trekking Bag Cover',
               description='Envent Waterproof, Dust Proof Laptop Bag/ '
                           'Trekking Bag Cover',
               owner_id = item_owner_4.id,
               category_id = category_3.id
               )

item_c15 = Item(name='Swiss Knife Set',
               description='14 in 1 Remei Branded Genuine Multifunction '
                           'Stainless Steel Corrosion Resistant Knife Set,'
                           ' Swiss Knife Set',
               owner_id = item_owner_5.id,
               category_id = category_3.id
               )
db.session.add(item_c11)
db.session.add(item_c12)
db.session.add(item_c13)
db.session.add(item_c14)
db.session.add(item_c15)

# Add Items for Category 4
category_4 = Category.query.filter_by(name='Cycling').first()
item_c16 = Item(name='Gear Bicycle',
               description='Cosmic Trium Men 21 Speed Gear Bicycle ',
               owner_id = item_owner_1.id,
               category_id = category_4.id
               )

item_c17 = Item(name='Saddle',
               description='High Quality Bicycle Silicone Saddle',
               owner_id = item_owner_2.id,
               category_id = category_4.id
               )

item_c18 = Item(name='Bicycle Accesories',
               description='Sun Bike Bicycle Safety Warning Light Set, Head '
                           'And Tail Led Lights',
               owner_id = item_owner_3.id,
               category_id = category_4.id
               )

item_c19 = Item(name='Puncture Stripes',
               description='SET OF 30 PCS CAR BIKE AUTO TUBELESS TYRE '
                           'PUNCTURE STRIPS / PLUGS USE WITH KIT',
               owner_id = item_owner_4.id,
               category_id = category_4.id
               )

item_c20 = Item(name='Air pump',
               description='Wintech Olympus Multipurpose Bicycle Air'
                           ' Pump For Car Bike',
               owner_id = item_owner_5.id,
               category_id = category_4.id
               )
db.session.add(item_c16)
db.session.add(item_c17)
db.session.add(item_c18)
db.session.add(item_c19)
db.session.add(item_c20)


# Add Items for Category 5
category_5 = Category.query.filter_by(name='Running').first()
item_c21 = Item(name='Heart Rate Monitor',
               description='Garmin Premium Heart Rate Monitor',
               owner_id = item_owner_1.id,
               category_id = category_5.id
               )

item_c22 = Item(name='Running Shoes',
               description='Asian Men Mesh Bullet Range Running... ',
               owner_id = item_owner_2.id,
               category_id = category_5.id
               )

item_c23 = Item(name='Water Bottle',
               description='Kalenji Hand-Bottle Adult Abdominal Equipment, '
                           '0.6-Liter',
               owner_id = item_owner_3.id,
               category_id = category_5.id
               )

item_c24 = Item(name='Hydration Belt',
               description='Kalenji Belt-2-Waterbottles Adult '
                           'Abdominal Equipment (Black)',
               owner_id = item_owner_4.id,
               category_id = category_5.id
               )

item_c25 = Item(name='Run Belt',
               description='Camelbak Marathoner Run Belt, 2 litres '
                           '(Electric Blue/Lime Punch)',
               owner_id = item_owner_5.id,
               category_id = category_5.id
               )
db.session.add(item_c21)
db.session.add(item_c22)
db.session.add(item_c23)
db.session.add(item_c24)
db.session.add(item_c25)


def main():
    db.session.commit()
    db.session.close()

if __name__ == '__main__':
    main()