from faker import Faker
fake = Faker(['en_US', 'ru_RU'])
for _ in range(10):
    print(fake.name())
    print(fake.text(255))