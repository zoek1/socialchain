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
    comments = Relationship('Comment', 'COMENTARIO')

    def to_json(self, user=None):
        return {
            "timestamp": str(self.timestamp),
            "tx_hash": self.tx_hash,
            "type": self.type,
            "tag": self.tag,
            "address_from": self.address_from.all()[0].address if len(self.address_from) else "",
            "address_to": self.address_to.all()[0].address if len(self.address_to) else "",
            "like": self.like.is_connected(user) if user else False,
            "share": self.share.is_connected(user) if user else False,
        }


# Transaction, Deposit, Withdraw
class Transaction(Action):
    fee = StringProperty()
    hash = StringProperty()
    network = StringProperty()
    success = BooleanProperty()
    actions = JSONProperty()

    def to_json(self, user=None):
        json = super().to_json(user)
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

    def to_json(self, user=None):
        json = super().to_json(user)
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

    def to_json(self, user=None):
        json = super().to_json(user)
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

    def to_json(self, user=None):
        json = super().to_json(user)
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

    def to_json(self, user=None):
        json = super().to_json(user)
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

    def to_json(self, user=None):
        json = super().to_json(user)
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

    def to_json(self, user=None):
        json = super().to_json(user)
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

    def to_json(self, user=None):
        json = super().to_json(user)
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

    def to_json(self, user=None):
        json = super().to_json(user)
        json['hash'] = self.hash
        json['network'] = self.network
        json['success'] = self.success
        json['actions'] = self.actions
        return json


class Address(StructuredNode):
    follow = RelationshipTo('Address', 'FOLLOW')
    address = StringProperty(unique_index=True, required=True)
    action_from = RelationshipTo('Action', 'FROM')
    action_to = RelationshipFrom('Action', 'TO')
    posts = Relationship('Comment', 'COMMENTER')


    def total_activity(self):
        results, columns = self.cypher(
            "MATCH (a) WHERE id(a)=$self MATCH (a)-[]-(action:Action) RETURN DISTINCT count(action)")

        return results[0][0]

    def total_timeline(self):
        results, columns = self.cypher(
            "MATCH (a) WHERE id(a)=$self MATCH (a)-[:FOLLOW]->(user:Address)-[]-(action:Action) RETURN DISTINCT count(action)")

        return results[0][0]

    def activity(self, page=1, count=150):
        #print(self.address)
        #actions = Action.nodes.filter(add)
        #print(dir(actions))

        #return actions
        skip = (page - 1) * count
        results, columns = self.cypher(
            f"""MATCH (a) WHERE id(a)=$self 
                MATCH (a)-[]-(action:Action) 
                RETURN DISTINCT action 
                ORDER BY action.timestamp DESC
                SKIP {skip} 
                LIMIT {count}""")

        return [get_class(row[0]).inflate(row[0]).to_json(self) for row in results]

    def timeline(self, page=1, count=150):
        skip = (page - 1) * count
        results, columns = self.cypher(
            f"""MATCH (a) WHERE id(a)=$self
                MATCH (a)-[:FOLLOW]->(user:Address)-[]-(action:Action) 
                RETURN DISTINCT action 
                ORDER BY action.timestamp DESC
                SKIP {skip} 
                LIMIT {count}""")

        return [get_class(row[0]).inflate(row[0]).to_json(self) for row in results]


class Post(Action):
    text = StringProperty()

    def to_json(self, user=None):
        json = super().to_json(user)
        json['text'] = self.text

        return json


class Comment(StructuredNode):
    @classmethod
    def category(cls):
        pass

    id = UniqueIdProperty()
    timestamp = DateTimeProperty(default_now=True)
    text = StringProperty()
    commenter = Relationship('Address', 'COMMENTER')
    action = Relationship('Action', 'COMENTARIO')

    def to_json(self):
        return {
            "id": self.id,
            "timestamp": str(self.timestamp),
            "text": self.text,
            "commenter": self.commenter.all()[0].address if len(self.commenter.all()) else "",
            "action": self.action.all()[0].tx_hash if len(self.action) else "",
        }


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

