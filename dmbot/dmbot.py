import discord
from helpers import roll_dice, TurnQ
import madlib


class DMBot(discord.Client):

    def __init__(self, logger):
        self.logger = logger
        super().__init__()
        self.turnq = TurnQ()
        self.commands = {"roll": self.roll,
                         "gen": self.madlib,
                         "turnq": self.turn_list}

    async def on_ready(self):
        self.logger.info("logged in as")
        self.logger.info(self.user.name)
        self.logger.info(self.user.id)
        self.logger.info('-------')

    async def on_message(self, message):

        if message.author == self.user:
            return
        self.logger.info("Received message: '{}'".format(message.content))
        await self.get_response(message)

    async def safe_send_message(self, dest, content):
        try:
            await self.send_typing(dest)
            self.logger.info("Sending '{}' to {}".format(content, str(dest)))
            await self.send_message(dest, content)
        except:
            self.logger.info("sending message failed")

    async def get_response(self, msg):
        """ parses the incoming message and responds appropriately """
        if not msg.content.startswith("~"):
            return
        split_msg = msg.content.split()
        cmd = split_msg[0][1:]
        try:
            await self.commands[cmd](msg, split_msg)
        except Exception as e:
            self.logger.error(e)

    async def roll(self, msg, split_msg):
        d_string = split_msg[1]
        r_list = roll_dice(d_string)
        msg_out = "Rolls: {} \n Total: {}".format(r_list, sum(r_list))
        await self.safe_send_message(msg.channel, msg_out)

    async def madlib(self, msg, split_msg):
        filename = "../generators/" + split_msg[1] + ".json"
        msg_out = madlib.main(filename)
        await self.safe_send_message(msg.channel, msg_out)

    async def turn_list(self, msg, split_msg):
        try:
            action = split_msg[1]
        except IndexError:
            msg_out = self.turnq.queue
            await self.safe_send_message(msg.channel, msg_out)
        if action == "new":
            self.turnq == TurnQ()
        if action == "add":
            c_name = split_msg[2]
            init = int(split_msg[3])
            self.turnq.add(c_name, init)
            msg_out = "Okay, added {} to the turn queue".format(c_name)
            await self.safe_send_message(msg.channel, msg_out)
        if action == "next":
            msg_out = self.turnq.next()
            await self.safe_send_message(msg.channel, msg_out)
        if action == "remove":
            c_name = split_msg[2]
            self.turnq.remove(c_name)
