
import threading
import time

class BaseComponent:
	def __init__(self, connection_parameters=None):
		print('Calling init at BaseComponent')
		self.connection_parameters = connection_parameters
		self.registered_stanzas = []

	def start(self):
		print("Connected with parameters: {}".format(self.connection_parameters))

	def register_stanza(self, stanza):
		return self.registered_stanzas.append(stanza)


class InteractiveMethodsMixin:
	pass


class OutboundStanzasMixin:
	pass


class InboundStanzasMixin:
	pass


class StandardStanzasMixin:
	def __init__(self, standard_stanzas_list=None):
		print('Calling init at StandardStanzasMixin')
		self.standard_stanzas_dict = {
			'presence_probe': self.presence_probe,
			'presence_subscription': self.presence_subscription
		}

		self.standard_stanzas_list = standard_stanzas_list


		if self.standard_stanzas_list is not None:
			for stanza in self.standard_stanzas_list:
				self.register_stanza((stanza, self.standard_stanzas_dict[stanza]))
		else:
			for stanza, handler in self.standard_stanzas_dict.items():
				self.register_stanza((stanza, handler))

	def presence_probe(self, probe):
		print('Reiceived a probe')

	def presence_subscription(self, subscription):
		print('Received a subscription')


class PollQueueMixin:

	def __init__(self):
		thread = threading.Thread(target=self.run, args=())
		thread.deamon = True
		thread.start()

	def run(self):
		while True:
			print('Polling...')
			time.sleep(2)

class FullComponent(BaseComponent, StandardStanzasMixin, PollQueueMixin):
	def __init__(self, connection_parameters=None, standard_stanzas_list=None):
		print('Calling init at FullComponent')
		self.connection_parameters = connection_parameters
		self.standard_stanzas_list = standard_stanzas_list

		BaseComponent.__init__(self, self.connection_parameters)
		StandardStanzasMixin.__init__(self, self.standard_stanzas_list)
		PollQueueMixin.__init__(self)



if __name__ == '__main__':
	#component = BaseComponent(connection_parameters='muc.localhost')
	#component.start()
	component = FullComponent(connection_parameters='muc.localhost', standard_stanzas_list=['presence_probe'])
	component.start()	
	component.registered_stanzas