from src.classes.frequency import Frequency
from src.classes.alphabet import Alphabet
from src.classes.my_sql_manager import MySqlManager
from src.classes.neural_network import NeuralNetworkMethod
from src.classes.app import App
from src.classes.spider import Spider

from src.database.database import engine, session_factory


my_sql_manager = MySqlManager(engine=engine, session_factory=session_factory)
spider = Spider(my_sql_manager=my_sql_manager)
frequency = Frequency(my_sql_manager, top_words_count=100)
alphabet = Alphabet()
neural_network = NeuralNetworkMethod()


app = App(mysql_manager=my_sql_manager, frequency=frequency, alphabet=alphabet, neural_network=neural_network,
          spider=spider)
# app._parse()
# app._create_language_profiles()

