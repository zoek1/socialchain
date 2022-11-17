from dateutil import parser
import requests

from .model import Transaction, Address, Mint, Burn, Deposit, Withdraw, Swap, Liquidity, Bridge, TransferCollective, MintCollective, BurnCollective, Donate, Vote, Post, Comment

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


def get_class(row):
    keys = list(row.labels)
    keys.remove('Action')
    return mapClass[keys[0]]


def get_address_or_create(cls, address):
    _to = cls.nodes.get_or_none(address=address)
    if not _to:
        _to = cls(address=address).save()
    return _to


def get_user_activity(address):
    url = f"https://pregod.rss3.dev/v1/notes/{address}?limit=500&include_poap=false&count_only=false&query_status=false"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    activity_json = response.json()
    if not activity_json.get("result", None):
        return

    for note in activity_json["result"]:
        note_type = note['type']
        tag = note["tag"]
        timestamp = parser.parse(note["timestamp"])
        _from = get_address_or_create(Address, note['address_from'])

        if tag == "transaction" and note_type == "transfer":
            _to = get_address_or_create(Address, note['address_to'])
            action = Transaction.nodes.get_or_none(timestamp=timestamp, type=note_type, tag=tag)
            if not action:
                action = Transaction(timestamp=timestamp,
                                     tx_hash=note["hash"],
                                     type=note_type,
                                     tag=tag,
                                     fee=note["fee"],
                                     network=note["network"],
                                     success=note["success"],
                                     actions=note["actions"]
                                     ).save()
                rel = action.address_to.connect(_to)
                rel = action.address_from.connect(_from)
        elif tag == "transaction" and note_type == "mint":
            timestamp = parser.parse(note["timestamp"])
            _to = get_address_or_create(Address, note['address_to'])
            action = Mint.nodes.get_or_none(timestamp=timestamp, type=note_type, tag=tag)
            if not action:
                action = Mint(timestamp=timestamp,
                              tx_hash=note["hash"],
                              type=note_type,
                              tag=tag,
                              fee=note["fee"],
                              network=note["network"],
                              success=note["success"],
                              actions=note["actions"]
                              ).save()
                rel = action.address_to.connect(_to)
                rel = action.address_from.connect(_from)
        elif tag == "transaction" and note_type == "burn":
            timestamp = parser.parse(note["timestamp"])
            _to = get_address_or_create(Address, note['address_to'])
            action = Burn.nodes.get_or_none(timestamp=timestamp, type=note_type, tag=tag)
            if not action:
                action = Burn(timestamp=timestamp,
                              tx_hash=note["hash"],
                              type=note_type,
                              tag=tag,
                              fee=note["fee"],
                              network=note["network"],
                              success=note["success"],
                              actions=note["actions"]
                              ).save()
                rel = action.address_to.connect(_to)
                rel = action.address_from.connect(_from)
        elif note_type == "deposit":
            timestamp = parser.parse(note["timestamp"])
            _to = get_address_or_create(Address, note['address_to'])
            action = Deposit.nodes.get_or_none(timestamp=timestamp, type=note_type, tag=tag)
            if not action:
                action = Deposit(timestamp=timestamp,
                                 tx_hash=note["hash"],
                                 type=note_type,
                                 tag=tag,
                                 fee=note["fee"],
                                 network=note["network"],
                                 success=note["success"],
                                 actions=note["actions"]
                                 ).save()
                rel = action.address_to.connect(_to)
                rel = action.address_from.connect(_from)
        elif note_type == "withdraw":
            timestamp = parser.parse(note["timestamp"])
            _to = get_address_or_create(Address, note['address_to'])
            action = Withdraw.nodes.get_or_none(timestamp=timestamp, type=note_type, tag=tag)
            if not action:
                action = Withdraw(timestamp=timestamp,
                                  tx_hash=note["hash"],
                                  type=note_type,
                                  tag=tag,
                                  fee=note["fee"],
                                  network=note["network"],
                                  success=note["success"],
                                  actions=note["actions"]
                                  ).save()
                rel = action.address_to.connect(_to)
                rel = action.address_from.connect(_from)
        elif note_type == "swap":
            timestamp = parser.parse(note["timestamp"])
            _to = get_address_or_create(Address, note['address_to'])
            action = Swap.nodes.get_or_none(timestamp=timestamp, type=note_type, tag=tag)
            if not action:
                action = Swap(timestamp=timestamp,
                              tx_hash=note["hash"],
                              type=note_type,
                              tag=tag,
                              fee=note["fee"],
                              network=note["network"],
                              platform=note["platform"],
                              success=note["success"],
                              actions=note["actions"]
                              ).save()
                rel = action.address_to.connect(_to)
                rel = action.address_from.connect(_from)
        elif note_type == "liquidity":
            timestamp = parser.parse(note["timestamp"])
            _to = get_address_or_create(Address, note['address_to'])
            action = Liquidity.nodes.get_or_none(timestamp=timestamp, type=note_type, tag=tag)
            if not action:
                action = Liquidity(timestamp=timestamp,
                                   tx_hash=note["hash"],
                                   type=note_type,
                                   tag=tag,
                                   fee=note["fee"],
                                   network=note["network"],
                                   platform=note["platform"],
                                   success=note["success"],
                                   actions=note["actions"]
                                   ).save()
                rel = action.address_to.connect(_to)
                rel = action.address_from.connect(_from)
        elif note_type == "bridge":
            timestamp = parser.parse(note["timestamp"])
            _to = get_address_or_create(Address, note['address_to'])
            action = Bridge.nodes.get_or_none(timestamp=timestamp, type=note_type, tag=tag)
            if not action:
                action = Bridge(timestamp=timestamp,
                                tx_hash=note["hash"],
                                type=note_type,
                                tag=tag,
                                fee=note["fee"],
                                network=note["network"],
                                platform=note["platform"],
                                success=note["success"],
                                actions=note["actions"]
                                ).save()
                rel = action.address_to.connect(_to)
                rel = action.address_from.connect(_from)
        elif tag == "collectible" and note_type == "transfer":
            timestamp = parser.parse(note["timestamp"])
            _to = get_address_or_create(Address, note['address_to'])
            action = TransferCollective.nodes.get_or_none(timestamp=timestamp, type=note_type, tag=tag)
            if not action:
                action = TransferCollective(timestamp=timestamp,
                                            tx_hash=note["hash"],
                                            type=note_type,
                                            tag=tag,
                                            fee=note["fee"],
                                            network=note["network"],
                                            success=note["success"],
                                            actions=note["actions"]
                                            ).save()
                rel = action.address_to.connect(_to)
                rel = action.address_from.connect(_from)
        elif tag == "collectible" and note_type == "mint":
            timestamp = parser.parse(note["timestamp"])
            _to = get_address_or_create(Address, note['address_to'])
            action = MintCollective.nodes.get_or_none(timestamp=timestamp, type=note_type, tag=tag)
            if not action:
                action = MintCollective(timestamp=timestamp,
                                        tx_hash=note["hash"],
                                        type=note_type,
                                        tag=tag,
                                        fee=note["fee"],
                                        network=note["network"],
                                        success=note["success"],
                                        actions=note["actions"]
                                        ).save()
                rel = action.address_to.connect(_to)
                rel = action.address_from.connect(_from)
        elif tag == "collectible" and note_type == "burn":
            timestamp = parser.parse(note["timestamp"])
            _to = get_address_or_create(Address, note['address_to'])
            action = BurnCollective.nodes.get_or_none(timestamp=timestamp, type=note_type, tag=tag)
            if not action:
                action = BurnCollective(timestamp=timestamp,
                                        tx_hash=note["hash"],
                                        type=note_type,
                                        tag=tag,
                                        fee=note["fee"],
                                        network=note["network"],
                                        success=note["success"],
                                        actions=note["actions"]
                                        ).save()

                rel = action.address_to.connect(_to)
                rel = action.address_from.connect(_from)
        elif note_type == "post":
            # post.append(note)
            pass
        elif note_type == "revise":
            # revise.append(note)
            pass
        elif note_type == "share":
            # share.append(note)
            pass
        elif note_type == "profile":
            # profile.append(note)
            pass
        elif note_type == "follow":
            # follow.append(note)
            pass
        elif note_type == "unfollow":
            # unfollow.append(note)
            pass
        elif note_type == "launch":
            # launch.append(note)
            pass
        elif note_type == "donate":
            timestamp = parser.parse(note["timestamp"])
            _to = get_address_or_create(Address, note['address_to'])
            action = BurnCollective.nodes.get_or_none(timestamp=timestamp, type=note_type, tag=tag)
            if not action:
                action = Donate(timestamp=timestamp,
                                tx_hash=note["hash"],
                                type=note_type,
                                tag=tag,
                                fee=note["fee"],
                                network=note["network"],
                                success=note["success"],
                                actions=note["actions"]
                                ).save()
                rel = action.address_to.connect(_to)
                rel = action.address_from.connect(_from)
        elif note_type == "propose":
            # propose.append(note)
            pass
        elif note_type == "vote":
            timestamp = parser.parse(note["timestamp"])
            action = Vote.nodes.get_or_none(timestamp=timestamp, type=note_type, tag=tag)
            if not action:
                action = Vote(timestamp=timestamp,
                              tx_hash=note["hash"],
                              type=note_type,
                              tag=tag,
                              network=note["network"],
                              success=note["success"],
                              actions=note["actions"]
                              ).save()

                rel = action.address_from.connect(_from)
        else:
            print(note)