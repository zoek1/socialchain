from datetime import datetime

from neomodel import StructuredRel, DateTimeProperty, StringProperty, BooleanProperty, JSONProperty, ArrayProperty, \
    StructuredNode, RelationshipTo, IntegerProperty, RelationshipFrom, Relationship, UniqueIdProperty


class Link(StructuredRel):
    timestamp = DateTimeProperty()
    hash = StringProperty()


class Action(StructuredNode):
    @classmethod
    def category(cls):
        pass

    timestamp = DateTimeProperty()
    tx_hash = StringProperty()
    type = StringProperty()
    tag = StringProperty()
    address_from = RelationshipFrom('Address', 'FROM')
    address_to = RelationshipTo('Address', 'TO')
    like = Relationship('Address', 'LIKE')
    share = Relationship('Address', 'SHARE')

    def to_json(self):
        return {
            "timestamp": str(self.timestamp),
            "tx_hash": self.tx_hash,
            "type": self.type,
            "tag": self.tag,
            "address_from": self.address_from.all()[0].address if len(self.address_from) else "",
            "address_to": self.address_to.all()[0].address if len(self.address_to) else "",
        }


# Transaction, Deposit, Withdraw
class Transaction(Action):
    fee = StringProperty()
    hash = StringProperty()
    network = StringProperty()
    success = BooleanProperty()
    actions = JSONProperty()

    def to_json(self):
        json = super().to_json()
        json['fee'] = self.fee
        json['hash'] = self.hash
        json['network'] = self.network
        json['success'] = self.success
        json['actions'] = self.actions

        return json


class Mint(Transaction):
    pass


class Burn(Transaction):
    pass


class Deposit(Transaction):
    pass


class Withdraw(Transaction):
    pass


# Swap
class Swap(Action):
    fee = StringProperty()
    hash = StringProperty()
    network = StringProperty()
    platform = StringProperty()
    success = BooleanProperty()
    actions = JSONProperty()

    def to_json(self):
        json = super().to_json()
        json['fee'] = self.fee
        json['hash'] = self.hash
        json['network'] = self.network
        json['platform'] = self.platform
        json['success'] = self.success
        json['actions'] = self.actions

        return json


class Liquidity(Action):
    fee = StringProperty()
    hash = StringProperty()
    network = StringProperty()
    platform = StringProperty()
    success = BooleanProperty()
    actions = JSONProperty()

    def to_json(self):
        json = super().to_json()
        json['fee'] = self.fee
        json['hash'] = self.hash
        json['network'] = self.network
        json['platform'] = self.platform
        json['success'] = self.success
        json['actions'] = self.actions
        return json


class Bridge(Action):
    fee = StringProperty()
    hash = StringProperty()
    network = StringProperty()
    platform = StringProperty()
    success = BooleanProperty()
    actions = JSONProperty()

    def to_json(self):
        json = super().to_json()
        json['fee'] = self.fee
        json['hash'] = self.hash
        json['network'] = self.network
        json['platform'] = self.platform
        json['success'] = self.success
        json['actions'] = self.actions
        return json


class MintCollective(Action):
    fee = StringProperty()
    hash = StringProperty()
    network = StringProperty()
    success = BooleanProperty()
    actions = JSONProperty()

    def to_json(self):
        json = super().to_json()
        json['fee'] = self.fee
        json['hash'] = self.hash
        json['network'] = self.network
        json['success'] = self.success
        json['actions'] = self.actions
        return json


class TransferCollective(Action):
    fee = StringProperty()
    hash = StringProperty()
    network = StringProperty()
    success = BooleanProperty()
    actions = JSONProperty()

    def to_json(self):
        json = super().to_json()
        json['fee'] = self.fee
        json['hash'] = self.hash
        json['network'] = self.network
        json['success'] = self.success
        json['actions'] = self.actions
        return json


class BurnCollective(Action):
    fee = StringProperty()
    hash = StringProperty()
    network = StringProperty()
    success = BooleanProperty()
    actions = JSONProperty()

    def to_json(self):
        json = super().to_json()
        json['fee'] = self.fee
        json['hash'] = self.hash
        json['network'] = self.network
        json['success'] = self.success
        json['actions'] = self.actions
        return json


class Donate(Action):
    fee = StringProperty()
    hash = StringProperty()
    network = StringProperty()
    success = BooleanProperty()
    actions = JSONProperty()

    def to_json(self):
        json = super().to_json()
        json['fee'] = self.fee
        json['hash'] = self.hash
        json['network'] = self.network
        json['success'] = self.success
        json['actions'] = self.actions
        return json


class Vote(Action):
    hash = StringProperty()
    network = StringProperty()
    success = BooleanProperty()
    actions = JSONProperty()

    def to_json(self):
        json = super().to_json()
        json['hash'] = self.hash
        json['network'] = self.network
        json['success'] = self.success
        json['actions'] = self.actions
        return json


class Address(StructuredNode):
    follow = RelationshipTo('Address', 'FOLLOW')
    address = StringProperty(unique_index=True, required=True)

    def timeline(self):
        results, columns = self.cypher(
            "MATCH (a) WHERE id(a)=$self MATCH (a)-[:FOLLOW]->(user:Address)-[:FROM]->(action:Action) RETURN action ORDER BY action.timestamp DESC LIMIT 150")

        return [get_class(row[0]).inflate(row[0]).to_json() for row in results]


class Post(Action):
    text = StringProperty()


class Comment(StructuredNode):
    id = UniqueIdProperty()
    timestamp = DateTimeProperty(default_now=True)
    text = StringProperty()
    commenter = Relationship('Address', 'COMMENT')
    action = Relationship('Action', 'COMMENT')
    read = BooleanProperty(default=False)


def get_class(row):
    keys = list(row.labels)
    keys.remove('Action')
    return mapClass[keys[0]]


mapClass = {
    'Transaction': Transaction,
    'Address': Address,
    'Mint': Mint,
    'Burn': Burn,
    'Deposit': Deposit,
    'Withdraw': Withdraw,
    "Swap": Swap,
    "Liquidity": Liquidity,
    "Bridge": Bridge,
    "TransferCollective": TransferCollective,
    "MintCollective": MintCollective,
    "BurnCollective": BurnCollective,
    "Donate": Donate,
    "Vote": Vote,
    "Post": Post
}

