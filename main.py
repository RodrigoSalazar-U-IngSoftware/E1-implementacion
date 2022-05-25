import random
from abc import ABC, ABCMeta, abstractmethod


class SingletonMeta(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Subject(ABC):
    @abstractmethod
    def add_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify_observers(self):
        pass


class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        pass


class Game(Subject, metaclass=SingletonMeta):
    REQUIRED_PLAYERS = 5

    def __init__(self):
        self.observers = []
        self.number = None

    def add_observer(self, observer):
        self.observers.append(observer)
        # If 5 players -> Start Game
        if len(self.observers) == self.REQUIRED_PLAYERS:
            self.execute_game()

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for obs in self.observers:
            obs.update(self)

    def execute_game(self):
        while True:
            self.number = random.randint(1, 100)
            print("Generate random number: {num}".format(num=self.number))
            self.notify_observers()


class Player(Observer):
    def __init__(self, strategy, name):
        self.name = name
        self._strategy = strategy

    def update(self, subject):
        if self._strategy.execute(subject.number):
            print("Player <{name}> Wins with Strategy <{strat}>".format(
                name=self.name, strat=type(self._strategy).__name__)
            )
            exit()

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy


class StrategyEvaluateRepetitions(ABC):
    @property
    @abstractmethod
    def repetitions(self):
        pass

    @abstractmethod
    def evaluate(self, data):
        pass

    def __init__(self):
        self.counter = 0

    def execute(self, data):
        if self.evaluate(data):
            self.counter += 1
        return self.counter >= self.repetitions


class StrategyFiveEven(StrategyEvaluateRepetitions):
    repetitions = 5

    def evaluate(self, data):
        return data % 2 == 0


class StrategyFiveOdd(StrategyEvaluateRepetitions):
    repetitions = 5

    def evaluate(self, data):
        return data % 2 == 1


class StrategyOnePrime(StrategyEvaluateRepetitions):
    repetitions = 1

    def evaluate(self, data):
        for i in range(2, data):
            if data % i == 0:
                return False
        return True


class StrategyThreeTenMul(StrategyEvaluateRepetitions):
    repetitions = 3

    def evaluate(self, data):
        return data % 10 == 0


class StrategyTwoTwentyFiveMul(StrategyEvaluateRepetitions):
    repetitions = 2

    def evaluate(self, data):
        return data % 25 == 0


if __name__ == '__main__':
    g = Game()
    p1 = Player(StrategyFiveEven(), "P1")
    p2 = Player(StrategyFiveOdd(), "P2")
    p3 = Player(StrategyOnePrime(), "P3")
    p4 = Player(StrategyThreeTenMul(), "P4")
    p5 = Player(StrategyTwoTwentyFiveMul(), "P5")

    g.add_observer(p1)
    g.add_observer(p2)
    g.add_observer(p3)
    g.add_observer(p4)
    g.add_observer(p5)  # Game Starts
