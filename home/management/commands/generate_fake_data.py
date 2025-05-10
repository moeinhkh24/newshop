from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from home.models import Product, Comment
from faker import Faker
import random
from django.core.files.base import ContentFile
import requests

fake = Faker()

class Command(BaseCommand):
    help = 'Generates fake data for the database'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=5, help='Number of users to create')
        parser.add_argument('--products', type=int, default=1, help='Number of products to create')
        parser.add_argument('--comments', type=int, default=200, help='Number of comments to create')

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Create users
        self.stdout.write('Creating users...')
        users = []
        for _ in range(options['users']):
            user = User.objects.create(
                phone_number=fake.numerify(text='09#########'),
                username=fake.user_name(),
                email=fake.email(),
                fullname=fake.name(),
                age=random.randint(18, 80),
                is_active=True
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))

        # Create products
        self.stdout.write('Creating products...')
        products = []
        for _ in range(options['products']):
            product = Product.objects.create(
                title=fake.catch_phrase(),
                image = self.get_random_image(),
                text=fake.paragraph(),
                price=random.randint(10000, 1000000),
                description=fake.text(),
                active=True
            )
            products.append(product)
        self.stdout.write(self.style.SUCCESS(f'Created {len(products)} products'))

        # Create comments
        self.stdout.write('Creating comments...')
        comments = []
        for _ in range(options['comments']):
            comment = Comment.objects.create(
                product=random.choice(products),
                author=random.choice(users),
                text=fake.paragraph(),
                stars=str(random.randint(1, 5)),
                status=random.choice([True, False])
            )
            comments.append(comment)
        self.stdout.write(self.style.SUCCESS(f'Created {len(comments)} comments'))

        self.stdout.write(self.style.SUCCESS('Successfully generated fake data')) 
        
    def get_random_image(self):
        """Random ImageField"""
        url = "https://picsum.photos/200/300"
        response = requests.get(url)
        return ContentFile(response.content, name=f"{fake.word()}.jpg")