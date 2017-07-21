import discord
from helpers import roll_dice, TurnQ, AdvJournal
import madlib


class DMBot(discord.Client):

    def __init__(self, logger):
        self.logger = logger
        super().__init__()
        self.turnq = TurnQ()
        self.journal = AdvJournal("journal.json")
        self.history = []
        self.commands = {"roll": self.roll,
                         "gen": self.madlib,
                         "turnq": self.turn_list,
                         "mnote": self.make_note,
                         "rnote": self.read_notes,
                         "sgen": self.save_genned,
                         "dgen": self.dump_genned}

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
        filename = "../dm_tools/generators/madlib/" + split_msg[1] + ".json"
        msg_out = madlib.main(filename)
        self.history.append(msg_out)
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

    async def make_note(self, msg, split_msg):
        text = " ".join(split_msg[1:])
        self.journal.make_note(text)
        await self.safe_send_message(msg.channel, "Okay, note saved")

    async def read_notes(self, msg, split_msg):
        num_lines = int(split_msg[1])
        msg_out = self.journal.read("notes", num_lines)
        await self.safe_send_message(msg.channel, str(msg_out))

    async def save_genned(self, msg, split_msg):
        last_genned = self.history[-1:][0]
        self.journal.write("generated", last_genned)
        await self.safe_send_message(msg.channel, "Okay, saved that")

    async def dump_genned(self, msg, split_msg):
        num_lines = int(split_msg[1])
        genned = self.journal.read("generated", num_lines)
        for item in genned:
            await self.safe_send_message(msg.channel, item)
