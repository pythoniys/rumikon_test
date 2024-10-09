from datetime import datetime, timedelta


class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def is_available(self, amount):
        return self.quantity >= amount

    def purchase(self, amount):
        if self.is_available(amount):
            self.quantity -= amount
        else:
            raise ValueError(f"Недостаточно товара {self.name} на складе")


class FoodProduct(Product):
    def __init__(self, name, price, quantity, proteins, fats, carbohydrates, calories):
        super().__init__(name, price, quantity)
        self.proteins = proteins
        self.fats = fats
        self.carbohydrates = carbohydrates
        self.calories = calories


class PerishableProduct(Product):
    def __init__(self, name, price, quantity, creation_date, shelf_life_days):
        super().__init__(name, price, quantity)
        self.creation_date = creation_date
        self.shelf_life_days = shelf_life_days

    def is_expired(self):
        expiration_date = self.creation_date + timedelta(days=self.shelf_life_days)
        return expiration_date <= datetime.now()

    def will_expire_in_less_than_24_hours(self):
        expiration_date = self.creation_date + timedelta(days=self.shelf_life_days)
        return expiration_date <= datetime.now() + timedelta(hours=24)


class Vitamin(Product):
    def __init__(self, name, price, quantity, requires_prescription):
        super().__init__(name, price, quantity)
        self.requires_prescription = requires_prescription


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        if not product.is_available(quantity):
            raise ValueError(f"Товара {product.name} нет в наличии в нужном количестве.")
        if isinstance(product, PerishableProduct) and product.will_expire_in_less_than_24_hours():
            raise ValueError(f"Товар {product.name} испортится в течение 24 часов.")
        if isinstance(product, Vitamin) and product.requires_prescription:
            raise ValueError(f"Для покупки {product.name} требуется рецепт.")
        
        self.items.append((product, quantity))
        product.purchase(quantity)

    def calculate_total(self):
        return sum(product.price * quantity for product, quantity in self.items)

    def check_nutritional_limits(self, max_proteins, max_fats, max_carbohydrates, max_calories):
        total_proteins = total_fats = total_carbohydrates = total_calories = 0
        for product, quantity in self.items:
            if isinstance(product, FoodProduct):
                total_proteins += product.proteins * quantity
                total_fats += product.fats * quantity
                total_carbohydrates += product.carbohydrates * quantity
                total_calories += product.calories * quantity

        if total_proteins > max_proteins:
            raise ValueError(f"Превышено количество белков: {total_proteins} г (максимум: {max_proteins} г)")
        if total_fats > max_fats:
            raise ValueError(f"Превышено количество жиров: {total_fats} г (максимум: {max_fats} г)")
        if total_carbohydrates > max_carbohydrates:
            raise ValueError(f"Превышено количество углеводов: {total_carbohydrates} г (максимум: {max_carbohydrates} г)")
        if total_calories > max_calories:
            raise ValueError(f"Превышено количество калорий: {total_calories} ккал (максимум: {max_calories} ккал)")


class Warehouse:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def generate_purchase_list(self):
        purchase_list = [product for product in self.products if product.quantity == 0]
        return purchase_list

    def generate_disposal_list(self):
        disposal_list = [product for product in self.products if isinstance(product, PerishableProduct) and product.is_expired()]
        return disposal_list


banana = FoodProduct("Банан", 30, 100, 1.3, 0.3, 22, 96)
milk = PerishableProduct("Молоко", 50, 10, datetime(2024, 10, 7), 7)
vitamin_c = Vitamin("Витамин C", 200, 50, True)

cart = Cart()
warehouse = Warehouse()

warehouse.add_product(banana)
warehouse.add_product(milk)
warehouse.add_product(vitamin_c)

cart.add_item(banana, 2)
cart.add_item(milk, 1)  

cart.check_nutritional_limits(max_proteins=100, max_fats=50, max_carbohydrates=300, max_calories=2000)

print(f"Общая стоимость товаров: {cart.calculate_total()} руб.")

print("Список для закупки:", [product.name for product in warehouse.generate_purchase_list()])
print("Список для утилизации:", [product.name for product in warehouse.generate_disposal_list()])
