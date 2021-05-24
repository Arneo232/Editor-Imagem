from os import path
from PIL import Image, ImageEnhance
from upscale import upscale_image, UPSCALE_MODEL, upscale_image_3_channels, UPSCALE_MODEL_3

from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

import os

class Editor():
	img = None
	img_formato = None
	img_local = None
	img_nome = None
	img_ext = None

	def resetar(self):
		self.img = None
		self.img_formato = None
		self.img_local = None
		self.img_nome = None
		self.img_ext = None

	def carregar_imagem(self, imagem):
		try:
			self.img = Image.open(imagem)
			self.img_formato = self.img.format
			self.img_local = path.dirname(path.realpath(imagem))
			self.img_nome, self.img_ext = path.splitext(path.basename(imagem))
			print('Imagem carregada!')
			return True
		except:
			print('Falha ao carregar imagem.')
			return False

	def girar_imagem(self, sentido='horario', angulo=90):
		if (sentido == 'horario'):
			self.img = self.img.rotate(angulo * -1, expand=True)
		elif (sentido == 'anti_horario'):
			self.img = self.img.rotate(angulo, expand=True)

	def remover_cor_imagem(self):
		conversor = ImageEnhance.Color(self.img)
		self.img = conversor.enhance(0)

	def upscale_imagem(self):
		self.img = upscale_image(UPSCALE_MODEL, self.img)

	def upscale_image_3_channels(self):
		self.img = upscale_image_3_channels(UPSCALE_MODEL_3, self.img)


	def salvar(self,path):
		self.img.save(path, self.img_formato)

ed = Editor()
