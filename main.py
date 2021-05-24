import os
from io import BytesIO

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition

from editor import ed

Window.clearcolor = .92, .92, .92, 1

Builder.load_file('interface.kv')

class Geral():
	def mudar_tela(self, nome_tela, tipo_transicao='Slide', direcao='left'):
		if (tipo_transicao == 'Slide'):
			self.manager.transition = SlideTransition()
		else:
			self.manager.transition = NoTransition()
		self.manager.transition.direction = direcao
		self.manager.current = nome_tela

class TelaInicial(Screen, Geral):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Window.bind(on_dropfile=self.soltou)

	def alterar_mensagem(self, texto):
		lb = self.ids.mensagem
		lb.text = texto

	def soltou(self, window, caminho_arquivo):
		ca = caminho_arquivo.decode('utf-8')

		if (ed.carregar_imagem(ca) == False):
			self.alterar_mensagem('[b]Imagem Inválida[/b] tente novamente')
		else:
			tela_edicao = self.manager.get_screen('tela_edicao')
			tela_edicao.exibir_imagem()
			self.mudar_tela('tela_edicao')

class TelaEdicao(Screen, Geral):
	def exibir_imagem(self):
		area_imagem = self.ids.area_imagem
		area_imagem.clear_widgets()

		img_buffer = BytesIO()
		ed.img.save(img_buffer, format=ed.img_formato)
		img_buffer.seek(0)

		co = CoreImage(img_buffer, ext=ed.img_formato.lower())
		textura = co.texture

		img_buffer.close()

		img = Image()
		img.texture = textura

		area_imagem.add_widget(img)

	def bt_girar_anti_horario(self):
		ed.girar_imagem('anti_horario')
		self.exibir_imagem()

	def bt_girar_horario(self):
		ed.girar_imagem('horario')
		self.exibir_imagem()

	def bt_preto_e_branco(self):
		ed.remover_cor_imagem()
		self.exibir_imagem()

	def bt_upscale(self):
		ed.upscale_imagem()
		self.exibir_imagem()

	def bt_upscale_image_3_channels(self):
		ed.upscale_image_3_channels()
		self.exibir_imagem()

	def bt_cancelar(self):
		tela_inicial = self.manager.get_screen('tela_inicial')
		tela_inicial.alterar_mensagem('[b]Procure uma imagem[/b] e arraste ela aqui')
		self.mudar_tela('tela_inicial', 'No')
		ed.resetar()

	def bt_mostrar_salvar(self):
		self.mudar_tela('tela_salvar', 'No')

class TelaSaveDialog(Screen, Geral):
	def bt_salvar(self, path, filename):
		ed.salvar(os.path.join(path, filename))
		tela_inicial = self.manager.get_screen('tela_inicial')
		tela_inicial.alterar_mensagem('[b]Procure uma imagem[/b] e arraste ela aqui')
		self.mudar_tela('tela_inicial', 'No')
		ed.resetar()

	def bt_cancelar(self):
		tela_edicao = self.manager.get_screen('tela_edicao')
		tela_edicao.exibir_imagem()
		self.mudar_tela('tela_edicao')

sm = ScreenManager()
sm.add_widget(TelaInicial(name='tela_inicial'))
sm.add_widget(TelaEdicao(name='tela_edicao'))
sm.add_widget(TelaSaveDialog(name='tela_salvar'))


class Programa(App):
	title = 'Editor de Imagens'
	def build(self):
		return sm

if __name__ == '__main__':
	Programa().run()
