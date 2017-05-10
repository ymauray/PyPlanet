"""
Dev app component.
"""
from pyplanet.contrib.command import Command


class DevComponent:
	def __init__(self, app):
		"""
		Developer tools component

		:param app: App config instance
		:type app: pyplanet.apps.core.pyplanet.app.PyPlanetConfig
		"""
		self.app = app

	async def on_init(self):
		pass

	async def on_start(self):
		await self.app.instance.permission_manager.register(
			'execute_calls', 'Can execute calls to server.', app=self.app, min_level=3
		)

		await self.app.instance.command_manager.register(
			Command('call', self.admin_call, perms='core.pyplanet:execute_calls', admin=True)
				.add_param('method', type=str)
				.add_param('args', type=str, nargs='*', required=False),
		)

	async def admin_call(self, player, data, **kwargs):
		method = data.method
		args = data.args
		if not isinstance(args, list):
			args = list()

		result = await self.app.instance.gbx.execute(method, *args)
		message = '$z$s$fff» $ff0Result: {}'.format(result)
		await self.app.instance.gbx.execute(
			'ChatSendServerMessageToLogin',
			message,
			player.login,
		)