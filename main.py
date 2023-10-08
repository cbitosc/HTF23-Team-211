from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder

Builder.load_string('''
<RV>:
    viewclass: 'SelectableLabel'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')

class SelectableLabel(Label):
    pass

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []

class GroceryApp(App):
    def build(self):
        b = BoxLayout(orientation='vertical', padding=[10, 10, 10, 10], spacing=10)

        # Instructions
        instructions = Label(text='Instructions: 1) Add items 2) Select store 3) Compare Prices')
        b.add_widget(instructions)

        # Title
        title_label = Label(text='Smart Grocery App', font_size='20sp', size_hint_y=None, height=50)
        b.add_widget(title_label)

        # Shopping List
        shopping_label = Label(text='Smart Shopping List')
        b.add_widget(shopping_label)
        self.text_input = TextInput(hint_text="Enter item...", multiline=False, size_hint_y=None, height=30)
        b.add_widget(self.text_input)
        self.rv = RV()
        b.add_widget(self.rv)
        button = Button(text="Add", size_hint_y=None, height=50)
        button.bind(on_press=self.add_item)
        b.add_widget(button)

        # Store Finder
        store_label = Label(text='Store Finder')
        b.add_widget(store_label)
        self.store_spinner = Spinner(text='Choose Store', values=('Ratnadeep', 'Reliance', 'Local Vendor'), size_hint_y=None, height=50)
        b.add_widget(self.store_spinner)

        # Price Comparison
        price_label = Label(text='Price Comparison')
        b.add_widget(price_label)
        self.price_output = Label(text='', size_hint_y=None, height=50)
        b.add_widget(self.price_output)
        self.compare_button = Button(text="Compare Prices", size_hint_y=None, height=50)
        self.compare_button.bind(on_press=self.compare_prices)
        b.add_widget(self.compare_button)

        return b

    def add_item(self, instance):
        item = self.text_input.text.strip()
        if item:
            new_data = self.rv.data.copy()
            new_data.append({'text': item})
            self.rv.data = new_data
            self.text_input.text = ''

    def compare_prices(self, instance):
        store = self.store_spinner.text
        if store == 'Choose Store':
            self.price_output.text = 'Please choose a store.'
            return

        items_to_compare = [d['text'].strip() for d in self.rv.data]
        print(f"Comparing these items: {items_to_compare}")  # Debugging statement

        prices = {
            'Ratnadeep': {'Apple': 120, 'Banana': 50, 'Milk': 44, 'Bread': 30},
            'Reliance': {'Apple': 110, 'Banana': 60, 'Milk': 43, 'Bread': 32},
            'Local Vendor': {'Apple': 130, 'Banana': 40, 'Milk': 45, 'Bread': 28},
        }

        price_info = []
        for item in items_to_compare:
            item_price = prices[store].get(item, None)
            if item_price:
                price_info.append(f"{item}: ₹{item_price}")
            else:
                price_info.append(f"{item} not available in {store}")

        self.price_output.text = f"Prices at {store}:\n" + "\n".join(price_info)

if __name__ == '__main__':
    GroceryApp().run()
