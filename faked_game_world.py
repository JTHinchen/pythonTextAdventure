import message

class GameWorld():

    def __init__(self):
        self.list_of_users = []

    def receive_message(self, new_message):
        list_of_messages = []
        for u in self.list_of_users:
            sending_message = message.Message("world",
                                              u,
                                              str(u) +
                                              ": New message sent by " +
                                              new_message.from_user_id +
                                              ": " +
                                              new_message.string_message)
            list_of_messages.append(sending_message)
        return list_of_messages

        

    def add_user(self, new_user_id):
        self.list_of_users.append(new_user_id)
    

    def remove_user(self, user_id):
        self.list_of_users.remove(user_id)
